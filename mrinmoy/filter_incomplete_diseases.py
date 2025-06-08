import json

# Load the files
with open('c:/Users/MRINMOY/DataSetRefinement/mrinmoy/mayoclinic_links_with_id.json', encoding='utf-8') as f:
    links = json.load(f)

with open('c:/Users/MRINMOY/DataSetRefinement/mrinmoy/mayoclinic_disease_data_filtered.json', encoding='utf-8') as f:
    filtered = json.load(f)

# Build a set of disease names from the filtered data (case-insensitive)
filtered_diseases = set(entry['disease'].strip().lower() for entry in filtered if 'disease' in entry)

# Find links whose disease name is not in the filtered data
absent = []
for entry in links:
    disease = entry.get('link_text', '').strip().lower()
    if disease and disease not in filtered_diseases:
        absent.append({'id': entry['id'], 'href': entry['href']})

# Save result
with open('c:/Users/MRINMOY/DataSetRefinement/mrinmoy/links_absent_from_filtered.json', 'w', encoding='utf-8') as f:
    json.dump(absent, f, indent=2, ensure_ascii=False)

print(f"Absent links saved: {len(absent)}")