import json
import re

with open("ultimate_scrap.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Prepare containers for each category
symptoms_data = []
home_care_data = []
first_aid_data = []
prognosis_data = []
alt_names_data = []
advice_data = []

for entry in data:
    if "id" in entry and "title" in entry and "sections" in entry:
        eid = entry["id"]
        title = entry["title"]
        sections = entry["sections"]
        # Symptoms
        if "Symptoms" in sections:
            s = sections["Symptoms"]
            symptoms_data.append({
                "id": eid,
                "title": title,
                "paragraphs": s.get("paragraphs", []),
                "lists": s.get("lists", [])
            })
        # Home Care
        if "Home Care" in sections:
            s = sections["Home Care"]
            home_care_data.append({
                "id": eid,
                "title": title,
                "paragraphs": s.get("paragraphs", []),
                "lists": s.get("lists", [])
            })
        # First Aid (sometimes called 'First Aid', sometimes 'What to Expect at the Emergency Room')
        if "First Aid" in sections:
            s = sections["First Aid"]
            first_aid_data.append({
                "id": eid,
                "title": title,
                "paragraphs": s.get("paragraphs", []),
                "lists": s.get("lists", [])
            })
        if "What to Expect at the Emergency Room" in sections:
            s = sections["What to Expect at the Emergency Room"]
            first_aid_data.append({
                "id": eid,
                "title": title,
                "paragraphs": s.get("paragraphs", []),
                "lists": s.get("lists", [])
            })
        # Prognosis
        if "Outlook (Prognosis)" in sections:
            s = sections["Outlook (Prognosis)"]
            prognosis_data.append({
                "id": eid,
                "title": title,
                "paragraphs": s.get("paragraphs", []),
                "lists": s.get("lists", [])
            })
        # Alternative Names
        if "Alternative Names" in sections:
            s = sections["Alternative Names"]
            alt_names_data.append({
                "id": eid,
                "title": title,
                "paragraphs": s.get("paragraphs", []),
                "lists": s.get("lists", [])
            })
        # General advice (collect from 'Before Calling Emergency', 'Poison Control', etc.)
        for advice_section in ["Before Calling Emergency", "Poison Control"]:
            if advice_section in sections:
                s = sections[advice_section]
                advice_data.append({
                    "id": eid,
                    "title": title,
                    "section": advice_section,
                    "paragraphs": s.get("paragraphs", []),
                    "lists": s.get("lists", [])
                })

# Save each category to its own file
with open("symptoms_data.json", "w", encoding="utf-8") as f:
    json.dump(symptoms_data, f, indent=2, ensure_ascii=False)
with open("home_care_data.json", "w", encoding="utf-8") as f:
    json.dump(home_care_data, f, indent=2, ensure_ascii=False)
with open("first_aid_data.json", "w", encoding="utf-8") as f:
    json.dump(first_aid_data, f, indent=2, ensure_ascii=False)
with open("prognosis_data.json", "w", encoding="utf-8") as f:
    json.dump(prognosis_data, f, indent=2, ensure_ascii=False)
with open("alt_names_data.json", "w", encoding="utf-8") as f:
    json.dump(alt_names_data, f, indent=2, ensure_ascii=False)
with open("advice_data.json", "w", encoding="utf-8") as f:
    json.dump(advice_data, f, indent=2, ensure_ascii=False)