import json
import requests
from bs4 import BeautifulSoup, Tag
import os
import time

INPUT_PATH = 'c:/Users/MRINMOY/DataSetRefinement/mrinmoy/final/mayoclinic_links_with_id_unique_sorted.json'
MISSED_IDS_PATH = 'c:/Users/MRINMOY/DataSetRefinement/mrinmoy/final/missed_ones.json'
OUTPUT_PATH = 'c:/Users/MRINMOY/DataSetRefinement/mrinmoy/final/mayoclinic_scraped_sections_5_missing.json'
BATCH_SIZE = 100

TARGET_IDS = {53, 119, 123, 149, 1426}

SECTION_MAP = {
    "Symptoms": "Symptoms",
    "Causes": "Causes",
    "When to see a doctor": "When to see a doctor",
    "Risk factors": "Risk factors",
    "Complications": "Complications",
    "Prevention": "Prevention",
    "Preventions": "Prevention"
}

FLAT_PROPERTIES = [
    "Symptoms", "Causes", "When to see a doctor", "Risk factors", "Complications", "Prevention"
]

# --- Enhanced Section Extraction ---
def extract_nested_list(ul_tag):
    result = []
    for li in ul_tag.find_all('li', recursive=False):
        item = {}
        # Get all text nodes before any nested list
        texts = [t for t in li.contents if isinstance(t, str)]
        text = ' '.join(t.strip() for t in texts if t.strip())
        if text:
            item['text'] = text
        # Handle multiple nested lists in a single li
        children = []
        for sublist in li.find_all(['ul', 'ol'], recursive=False):
            children.extend(extract_nested_list(sublist))
        if children:
            item['children'] = children
        if item:
            result.append(item)
    return result

def extract_sections(soup):
    result = {}
    # Try to find <section aria-labelledby="symptoms"> etc. for each section
    for key in SECTION_MAP:
        aria_label = key.lower().replace(" ", "-")
        section = soup.find('section', attrs={'aria-labelledby': aria_label})
        if section:
            section_key = SECTION_MAP[key]
            section_content = {'paragraphs': [], 'lists': []}
            # Find all direct <p> and <ul>/<ol> descendants in order
            for child in section.find_all(['p', 'ul', 'ol'], recursive=True):
                if child.name == 'p':
                    txt = child.get_text(strip=True)
                    if txt:
                        section_content['paragraphs'].append(txt)
                elif child.name in ['ul', 'ol']:
                    nested = extract_nested_list(child)
                    if nested:
                        section_content['lists'].append(nested)
            if section_content['paragraphs'] or section_content['lists']:
                result[section_key] = section_content
            continue  # Go to next key if found
        # Fallback: use previous heading-based logic
        section_tags = soup.find_all(['h2', 'h3'])
        for idx, tag in enumerate(section_tags):
            section_title = tag.get_text(strip=True)
            for key in SECTION_MAP:
                if key.lower() in section_title.lower():
                    section_key = SECTION_MAP[key]
                    section_content = {'paragraphs': [], 'lists': []}
                    # Traverse all siblings after the heading until the next h2/h3
                    next_node = tag
                    while True:
                        next_node = next_node.next_sibling
                        if next_node is None:
                            break
                        if isinstance(next_node, str):
                            continue
                        if isinstance(next_node, Tag) and next_node.name in ['h2', 'h3']:
                            break
                        if isinstance(next_node, Tag):
                            if next_node.name == 'p':
                                txt = next_node.get_text(strip=True)
                                if txt:
                                    section_content['paragraphs'].append(txt)
                            elif next_node.name in ['ul', 'ol']:
                                nested = extract_nested_list(next_node)
                                if nested:
                                    section_content['lists'].append(nested)
                    if section_content['paragraphs'] or section_content['lists']:
                        result[section_key] = section_content
                    break
    return result

def flatten_section(section):
    if isinstance(section, list) and all(isinstance(x, str) for x in section):
        return section
    if isinstance(section, dict):
        result = []
        if 'paragraphs' in section and isinstance(section['paragraphs'], list):
            result.extend([s for s in section['paragraphs'] if isinstance(s, str)])
        if 'lists' in section and isinstance(section['lists'], list):
            def flatten_list(lst):
                flat = []
                for item in lst:
                    if isinstance(item, dict):
                        if 'text' in item:
                            flat.append(item['text'])
                        if 'children' in item:
                            flat.extend(flatten_list(item['children']))
                    elif isinstance(item, list):
                        flat.extend(flatten_list(item))
                    elif isinstance(item, str):
                        flat.append(item)
                return flat
            for l in section['lists']:
                result.extend(flatten_list(l))
        return result
    if isinstance(section, str):
        return [section]
    if isinstance(section, list):
        flat = []
        for item in section:
            if isinstance(item, str):
                flat.append(item)
            elif isinstance(item, dict):
                if 'text' in item:
                    flat.append(item['text'])
                if 'children' in item:
                    flat.extend(flatten_section(item['children']))
        return flat
    return []

def fallback_extract(soup):
    # Try to get all <p>, <ul>, <ol> under the main content
    content = {'Symptoms': [], 'Causes': [], 'When to see a doctor': [], 'Risk factors': [], 'Complications': [], 'Prevention': []}
    # Try to find the main content area
    main = soup.find('main') or soup.body
    if not main:
        main = soup
    all_text = []
    for tag in main.find_all(['p', 'ul', 'ol']):
        if tag.name == 'p':
            txt = tag.get_text(strip=True)
            if txt:
                all_text.append(txt)
        elif tag.name in ['ul', 'ol']:
            for li in tag.find_all('li'):
                txt = li.get_text(strip=True)
                if txt:
                    all_text.append(txt)
    # Heuristically assign to Symptoms, then Causes, etc.
    # Just put all in Symptoms if nothing else can be done
    if all_text:
        content['Symptoms'] = all_text
    return content

def save_batch(batch, output_path):
    if os.path.exists(output_path):
        with open(output_path, 'r', encoding='utf-8') as f:
            try:
                existing = json.load(f)
            except Exception:
                existing = []
    else:
        existing = []
    existing.extend(batch)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

# --- Main logic to process only missed IDs ---
def main():
    with open(INPUT_PATH, encoding='utf-8') as f:
        all_links = json.load(f)
    data = [entry for entry in all_links if entry['id'] in TARGET_IDS]
    batch = []
    for idx, entry in enumerate(data):
        id_ = entry.get('id')
        disease = entry.get('disease')
        href = entry.get('href')
        if not (id_ and disease and href):
            continue
        out_entry = {"id": id_, "disease": disease}
        try:
            resp = requests.get(href, timeout=15)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')
            sections = extract_sections(soup)
            # Flatten all required properties
            for prop in FLAT_PROPERTIES:
                if prop in sections:
                    out_entry[prop] = flatten_section(sections[prop])
                else:
                    out_entry[prop] = []
            # If all are empty, try fallback
            if not any(out_entry[prop] for prop in FLAT_PROPERTIES):
                fallback = fallback_extract(soup)
                for prop in FLAT_PROPERTIES:
                    if not out_entry[prop] and fallback[prop]:
                        out_entry[prop] = fallback[prop]
            print(f"[DEBUG] Scraped {disease} (id={id_}) with sections: {[k for k in FLAT_PROPERTIES if out_entry[k]]}")
        except Exception as e:
            print(f"[ERROR] Failed for {disease} (id={id_}): {e}")
            out_entry['error'] = str(e)
        batch.append(out_entry)
    # Sort by id
    batch.sort(key=lambda x: x.get('id', float('inf')))
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(batch, f, ensure_ascii=False, indent=2)
    print(f"[DEBUG] Saved {len(batch)} records to {OUTPUT_PATH} (sorted by id).")

if __name__ == "__main__":
    main()
