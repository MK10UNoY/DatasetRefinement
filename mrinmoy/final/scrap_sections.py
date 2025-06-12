import json
import requests
from bs4 import BeautifulSoup, Tag
import os
import time

INPUT_PATH = 'c:/Users/MRINMOY/DataSetRefinement/mrinmoy/final/mayoclinic_links_with_id_unique_sorted.json'
MISSED_IDS_PATH = 'c:/Users/MRINMOY/DataSetRefinement/mrinmoy/final/missed_ones.json'
OUTPUT_PATH = 'c:/Users/MRINMOY/DataSetRefinement/mrinmoy/final/mayoclinic_scraped_sections.json'
BATCH_SIZE = 100

SECTION_MAP = {
    "Symptoms": "Symptoms",
    "Causes": "Causes",
    "When to see a doctor": "When to see a doctor",
    "Risk factors": "Risk factors",
    "Complications": "Complications",
    "Prevention": "Prevention",
    "Preventions": "Prevention"
}

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
    with open(MISSED_IDS_PATH, encoding='utf-8') as f:
        missed_ids = set(entry['id'] for entry in json.load(f))
    # Filter only missed entries
    data = [entry for entry in all_links if entry['id'] in missed_ids]
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
            out_entry.update(sections)
            print(f"[DEBUG] Scraped {disease} (id={id_}) with sections: {list(sections.keys())}")
        except Exception as e:
            print(f"[ERROR] Failed for {disease} (id={id_}): {e}")
            out_entry['error'] = str(e)
        batch.append(out_entry)
        if len(batch) >= BATCH_SIZE:
            save_batch(batch, OUTPUT_PATH)
            print(f"[DEBUG] Saved batch of {BATCH_SIZE} records up to index {idx}")
            batch = []
            time.sleep(1)
    if batch:
        save_batch(batch, OUTPUT_PATH)
        print(f"[DEBUG] Saved final batch of {len(batch)} records.")

if __name__ == "__main__":
    main()
