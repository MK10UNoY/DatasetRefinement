import json
import re

with open("ultimate_scrap.json", "r", encoding="utf-8") as f:
    data = json.load(f)

output = []
for entry in data:
    if "id" in entry and "title" in entry and "sections" in entry:
        disease = entry["title"]
        symptoms = []
        sections = entry["sections"]
        # Extract alternative names from the correct section
        alternative_names = []
        if "Alternative Names" in sections:
            alt_section = sections["Alternative Names"]
            if "paragraphs" in alt_section and alt_section["paragraphs"]:
                for p in alt_section["paragraphs"]:
                    # Split by semicolon and strip whitespace
                    alternative_names += [name.strip() for name in p.split(';') if name.strip()]
        if "Symptoms" in sections:
            s = sections["Symptoms"]
            # Always include all list items
            if "lists" in s and any(s["lists"]):
                for l in s["lists"]:
                    symptoms += l
                # Filter out paragraphs that are just headers
                if "paragraphs" in s:
                    for p in s["paragraphs"]:
                        if not re.search(r'include[s]?:$', p.strip(), re.IGNORECASE):
                            symptoms.append(p)
            elif "paragraphs" in s:
                symptoms += s["paragraphs"]
        # Only add if symptoms found
        if symptoms:
            output.append({
                "id": entry["id"],
                "disease": disease,
                "symptoms": symptoms,
                "alternative_names": alternative_names
            })

with open("symptoms_vs_disease.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

paragraphs_output = []
for entry in data:
    if "id" in entry and "title" in entry and "sections" in entry:
        entry_paragraphs = []
        sections = entry["sections"]
        for section in sections.values():
            if "paragraphs" in section and section["paragraphs"]:
                entry_paragraphs.extend(section["paragraphs"])
        if entry_paragraphs:
            paragraphs_output.append({
                "id": entry["id"],
                "title": entry["title"],
                "paragraphs": entry_paragraphs
            })

with open("all_entry_paragraphs.json", "w", encoding="utf-8") as f:
    json.dump(paragraphs_output, f, indent=2, ensure_ascii=False)

# Extract only the paragraphs from the Symptoms section for each entry
symptoms_paragraphs_output = []
for entry in data:
    if "id" in entry and "title" in entry and "sections" in entry:
        sections = entry["sections"]
        if "Symptoms" in sections:
            s = sections["Symptoms"]
            if "paragraphs" in s and s["paragraphs"]:
                symptoms_paragraphs_output.append({
                    "id": entry["id"],
                    "title": entry["title"],
                    "symptoms_paragraphs": s["paragraphs"]
                })

with open("symptoms_section_paragraphs.json", "w", encoding="utf-8") as f:
    json.dump(symptoms_paragraphs_output, f, indent=2, ensure_ascii=False)