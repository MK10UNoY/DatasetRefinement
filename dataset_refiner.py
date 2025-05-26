import json

def transform_article(article):
    sections = article["sections"]
    
    def get_text_list(section_name):
        sec = sections.get(section_name, {})
        paras = sec.get("paragraphs", [])
        lists = sec.get("lists", [])
        return paras + (lists[0] if lists else [])

    return {
        "id": article["id"],
        "title": article["title"],
        "url": article["url"],
        "alt_names": get_text_list("Alternative Names"),
        "causes": {
            "ingredients": get_text_list("Poisonous Ingredient"),
            "brands": get_text_list("Where Found")
        },
        "symptoms": {
            "list": get_text_list("Symptoms")
        },
        "home_care": get_text_list("Home Care"),
        "emergency_guidelines": {
            "info_needed": get_text_list("Before Calling Emergency"),
            "poison_control": get_text_list("Poison Control")
        },
        "clinical_treatments": {
            "summary": sections.get("What to Expect at the Emergency Room", {}).get("paragraphs", []),
            "procedures": (sections.get("What to Expect at the Emergency Room", {}).get("lists") or [[]])[0]
        },
        "prognosis": get_text_list("Outlook (Prognosis)"),
        "references": get_text_list("References"),
        "review_info": get_text_list([k for k in sections.keys() if k.lower().startswith("review date")][0]) if any(k.lower().startswith("review date") for k in sections) else [],
        "related_topics": article.get("mplus_wrap", "").split(",") if article.get("mplus_wrap") else []
    }

    sections = raw.get("sections", {})

    def extract_list(section_name):
        lists = sections.get(section_name, {}).get("lists", [])
        if not lists:
            print(f"[WARN] Empty list in section: {section_name}")
        return lists[0] if lists else []


    def extract_paragraphs(section_name):
        return sections.get(section_name, {}).get("paragraphs", [])

    def extract_symptoms():
        symptoms = {}
        para_labels = extract_paragraphs("Symptoms")
        lists = sections.get("Symptoms", {}).get("lists", [])

        for label, items in zip(para_labels[1:], lists):  # skip the first general line
            label = label.replace(":", "").strip()
            symptoms[label] = items
        return symptoms

    return {
        "id": raw.get("id"),
        "title": raw.get("title"),
        "url": raw.get("url"),
        "alt_names": extract_paragraphs("Alternative Names"),
        "causes": {
            "ingredients": extract_paragraphs("Poisonous Ingredient"),
            "brands": extract_list("Where Found")
        },
        "symptoms": extract_symptoms(),
        "home_care": extract_paragraphs("Home Care"),
        "emergency_guidelines": {
            "info_needed": extract_list("Before Calling Emergency"),
            "poison_control": extract_paragraphs("Poison Control")
        },
        "clinical_treatments": {
            "summary": extract_paragraphs("What to Expect at the Emergency Room"),
            "procedures": extract_list("What to Expect at the Emergency Room")
        },
        "prognosis": extract_paragraphs("Outlook (Prognosis)"),
        "references": extract_paragraphs("References"),
        "review_info": extract_paragraphs("Review Date 1/2/2023"),
        "related_topics": extract_list("Related MedlinePlus Health Topics")
    }

# Usage
with open("ultimate_scrap.json") as f:
    raw_data = json.load(f)

structured_data = [transform_article(article) for article in raw_data]

with open("structured_articles.json", "w") as f:
    json.dump(structured_data, f, indent=2)
