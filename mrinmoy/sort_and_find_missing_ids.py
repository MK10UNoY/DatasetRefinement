import json

# File paths
filtered_with_id_path = "c:/Users/MRINMOY/DataSetRefinement/mrinmoy/mayoclinic_disease_data_filtered_with_id.json"
links_with_id_path = "c:/Users/MRINMOY/DataSetRefinement/mrinmoy/mayoclinic_links_with_id.json"
sorted_output_path = "c:/Users/MRINMOY/DataSetRefinement/mrinmoy/mayoclinic_disease_data_filtered_with_id_sorted.json"
missing_ids_output_path = "c:/Users/MRINMOY/DataSetRefinement/mrinmoy/missing_ids_up_to_2321.json"

# Load filtered disease data with id
with open(filtered_with_id_path, encoding="utf-8") as f:
    disease_data = json.load(f)

# Load all links with id
with open(links_with_id_path, encoding="utf-8") as f:
    links_data = json.load(f)

# Sort disease data by id
sorted_disease_data = sorted(disease_data, key=lambda x: x.get("id", 9999999))

# Save sorted data
with open(sorted_output_path, "w", encoding="utf-8") as f:
    json.dump(sorted_disease_data, f, ensure_ascii=False, indent=2)

# Get all ids from links (up to 2321)
all_ids = set()
for entry in links_data:
    id_val = entry.get("id")
    if isinstance(id_val, int) and 1 <= id_val <= 2321:
        all_ids.add(id_val)

# Get ids present in filtered disease data
present_ids = set()
for entry in disease_data:
    id_val = entry.get("id")
    if isinstance(id_val, int):
        present_ids.add(id_val)

# Find missing ids
missing_ids = sorted(list(all_ids - present_ids))

# Save missing ids
with open(missing_ids_output_path, "w", encoding="utf-8") as f:
    json.dump(missing_ids, f, ensure_ascii=False, indent=2)

print(f"Sorted data saved to: {sorted_output_path}")
print(f"Missing ids (up to 2321) saved to: {missing_ids_output_path}")
