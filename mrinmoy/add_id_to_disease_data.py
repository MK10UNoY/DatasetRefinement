import json

# Load disease data
with open('mrinmoy/mayoclinic_disease_data_filtered.json', 'r', encoding='utf-8') as f:
    disease_data = json.load(f)

# Load links with id
def load_links():
    with open('mrinmoy/mayoclinic_links_with_id.json', 'r', encoding='utf-8') as f:
        links = json.load(f)
    # Create a mapping from disease name to id (case-insensitive)
    name_to_id = {}
    for entry in links:
        name_to_id[entry['link_text'].strip().lower()] = entry['id']
    return name_to_id

def add_ids_to_diseases(disease_data, name_to_id):
    for entry in disease_data:
        disease_name = entry.get('disease', '').strip().lower()
        if disease_name and disease_name in name_to_id:
            entry['id'] = name_to_id[disease_name]
    return disease_data

def main():
    name_to_id = load_links()
    updated_data = add_ids_to_diseases(disease_data, name_to_id)
    with open('mrinmoy/mayoclinic_disease_data_filtered_with_id.json', 'w', encoding='utf-8') as f:
        json.dump(updated_data, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
