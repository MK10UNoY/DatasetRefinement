import json

# File paths
missed_index_path = "mrinmoy/missed_index.json"
unique_href_path = "mrinmoy/mayoclinic_links_with_id_unique_href.json"
output_path = "mrinmoy/missed_index_union.json"

# Load both files
with open(missed_index_path, "r", encoding="utf-8") as f:
    missed_index = json.load(f)

with open(unique_href_path, "r", encoding="utf-8") as f:
    unique_href = json.load(f)

# Build a lookup by href for both
union_lookup = {}

for entry in missed_index:
    href = entry.get("href")
    if href:
        union_lookup[href] = entry

for entry in unique_href:
    href = entry.get("href")
    if href and href not in union_lookup:
        union_lookup[href] = entry

# Create the union list
union_list = list(union_lookup.values())

# Save the union output
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(union_list, f, indent=2, ensure_ascii=False)

print(f"Union complete. {len(union_list)} unique entries saved to {output_path}")