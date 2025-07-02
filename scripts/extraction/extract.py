import fitz  # PyMuPDF
import re
import json

def extract_text_from_pdf(pdf_path):
    """Extract text from a given PDF file."""
    doc = fitz.open(pdf_path)
    text = "\n".join(page.get_text() for page in doc)
    return text

def extract_disease_info(text):
    """Extract disease-related information from the given text."""
    sections = ["Symptoms", "Causes", "Risk factors", "Complications", "Prevention"]
    disease_info = {"disease": None}

    lines = text.split("\n")
    current_section = None
    data = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Check if the line matches any section header
        for section in sections:
            if re.match(f"^{section}", line, re.IGNORECASE):
                if current_section:
                    disease_info[current_section] = data
                current_section = section
                data = []
                break
        else:
            if current_section:
                data.append(line)

    if current_section:
        disease_info[current_section] = data

    # Extract disease name (assuming it's the first meaningful title)
    if lines:
        disease_info["disease"] = lines[0]

    return disease_info

def save_as_json(data, output_file):
    """Save extracted data as a JSON file."""
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    pdf_path = "./STW_Vol_3_2022.pdf"  # Update with the actual file path
    output_file = "extracted_disease_info.json"

    text = extract_text_from_pdf(pdf_path)
    extracted_data = extract_disease_info(text)
    save_as_json(extracted_data, output_file)

    print(f"Extracted information saved to {output_file}")
