import json

INPUT_PATH = 'c:/Users/MRINMOY/DataSetRefinement/ultimate_scrap.json'
OUTPUT_PATH = 'c:/Users/MRINMOY/DataSetRefinement/ultimate_scrap_flattened.json'

def flatten_section(section):
    out = []
    if isinstance(section, dict):
        out.extend([s for s in section.get('paragraphs', []) if isinstance(s, str)])
        def flat_list(lst):
            for item in lst:
                if isinstance(item, str):
                    out.append(item)
                elif isinstance(item, dict):
                    if 'text' in item:
                        out.append(item['text'])
                    if 'children' in item:
                        flat_list(item['children'])
                elif isinstance(item, list):
                    flat_list(item)
        flat_list(section.get('lists', []))
    elif isinstance(section, list):
        for item in section:
            if isinstance(item, str):
                out.append(item)
            elif isinstance(item, dict):
                if 'text' in item:
                    out.append(item['text'])
                if 'children' in item:
                    out.extend(flatten_section(item['children']))
    elif isinstance(section, str):
        out.append(section)
    return [s.strip() for s in out if isinstance(s, str) and s.strip()]

with open(INPUT_PATH, encoding='utf-8') as f:
    data = json.load(f)

results = []
for obj in data:
    out = {}
    out['id'] = obj.get('id')
    out['title'] = obj.get('title') or obj.get('disease')
    alt_names = None
    if 'sections' in obj and 'Alternative Names' in obj['sections']:
        alt_names = obj['sections']['Alternative Names']
        if isinstance(alt_names, dict):
            alt_names = alt_names.get('paragraphs', [])
        elif not isinstance(alt_names, list):
            alt_names = [alt_names]
    out['alternate_names'] = alt_names if alt_names else []
    # Flatten everything in sections['Symptoms']
    symptoms = []
    if 'sections' in obj and 'Symptoms' in obj['sections']:
        symptoms = flatten_section(obj['sections']['Symptoms'])
    out['symptoms'] = symptoms
    results.append(out)

with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"Extracted and flattened {len(results)} records to {OUTPUT_PATH}")
