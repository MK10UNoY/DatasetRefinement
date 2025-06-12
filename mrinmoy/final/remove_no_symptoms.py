import json

INPUT_PATH = 'c:/Users/MRINMOY/DataSetRefinement/mrinmoy/final/mayoclinic_scraped_sections.json'
OUTPUT_PATH = 'c:/Users/MRINMOY/DataSetRefinement/mrinmoy/final/mayoclinic_scraped_sections_with_symptoms.json'

with open(INPUT_PATH, encoding='utf-8') as f:
    data = json.load(f)

filtered = [obj for obj in data if 'Symptoms' in obj and obj['Symptoms']]

with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    json.dump(filtered, f, ensure_ascii=False, indent=2)

print(f"Filtered {len(data) - len(filtered)} records without 'Symptoms'. Saved {len(filtered)} records to {OUTPUT_PATH}.")
