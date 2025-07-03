import json
import re

# Optional: Only import if needed
try:
    import fitz  # PyMuPDF for PDF extraction
except ImportError:
    fitz = None

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    requests = None
    BeautifulSoup = None

def extract_from_pdf(pdf_path, output_path=None):
    """
    Extracts disease-related information from a PDF file.
    Args:
        pdf_path (str): Path to the PDF file.
        output_path (str, optional): If provided, saves the extracted data as JSON.
    Returns:
        dict: Extracted disease information.
    """
    if fitz is None:
        raise ImportError("PyMuPDF (fitz) is required for PDF extraction.")
    doc = fitz.open(pdf_path)
    text = "\n".join(page.get_text() for page in doc)
    sections = ["Symptoms", "Causes", "Risk factors", "Complications", "Prevention"]
    disease_info = {"disease": None}
    lines = text.split("\n")
    current_section = None
    data = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
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
    if lines:
        disease_info["disease"] = lines[0]
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(disease_info, f, indent=4)
    return disease_info

def flatten_section(section):
    """
    Flattens nested section data (from JSON or dict) into a list of strings.
    """
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

def extract_and_flatten_json(input_path, output_path=None):
    """
    Extracts and flattens disease data from a JSON file (e.g., web-scraped or pre-structured).
    Args:
        input_path (str): Path to the input JSON file.
        output_path (str, optional): If provided, saves the flattened data as JSON.
    Returns:
        list: List of flattened disease records.
    """
    with open(input_path, encoding='utf-8') as f:
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
        symptoms = []
        if 'sections' in obj and 'Symptoms' in obj['sections']:
            symptoms = flatten_section(obj['sections']['Symptoms'])
        out['symptoms'] = symptoms
        causes = []
        if 'sections' in obj and 'Causes' in obj['sections']:
            causes = flatten_section(obj['sections']['Causes'])
        out['causes'] = causes
        results.append(out)
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
    return results

def scrape_medlineplus_article(article_id):
    """
    Example web scraper for MedlinePlus articles by ID.
    Args:
        article_id (str): Six-digit article ID as a string.
    Returns:
        dict: Scraped article data, or None if not found/invalid.
    """
    if requests is None or BeautifulSoup is None:
        raise ImportError("requests and beautifulsoup4 are required for web scraping.")
    BASE_URL = "https://medlineplus.gov/ency/article/"
    HEADERS = {"User-Agent": "Mozilla/5.0"}
    url = f"{BASE_URL}{article_id}.htm"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.text, "html.parser")
    if soup.find("title") and "Page Not Found" in soup.find("title").text:
        return None
    data = {
        "id": article_id,
        "title": soup.find("h1").text.strip() if soup.find("h1") else "",
        "url": url,
        "summary": soup.select_one("#ency_summary p").text.strip() if soup.select_one("#ency_summary p") else "",
        "symptoms": [li.text.strip() for li in soup.select("ul li") if "symptom" in li.text.lower()],
        "causes": [p.text.strip() for p in soup.select("p") if "cause" in p.text.lower()],
        "treatments": [p.text.strip() for p in soup.select("p") if "treatment" in p.text.lower()]
    }
    return data

# You can add more scrapers for other sources as needed.

def extract_file(input_path, output_path):
    """
    Main entry point for the toolkit. Dispatches extraction based on file type.
    """
    if input_path.lower().endswith('.pdf'):
        return extract_from_pdf(input_path, output_path)
    elif input_path.lower().endswith('.json'):
        return extract_and_flatten_json(input_path, output_path)
    else:
        raise ValueError(f"Unsupported file type for extraction: {input_path}")

def extract_from_url(url, output_path=None):
    """
    Extracts all <p> text from a web page and saves as JSON if output_path is provided.
    Args:
        url (str): The website URL.
        output_path (str, optional): Path to save the extracted data as JSON.
    Returns:
        dict: Extracted data with url and paragraphs.
    """
    if requests is None or BeautifulSoup is None:
        raise ImportError("requests and beautifulsoup4 are required for web scraping.")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = {
        'url': url,
        'paragraphs': [p.get_text(strip=True) for p in soup.find_all('p')]
    }
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    return data 