import requests
from bs4 import BeautifulSoup
import json

def extract_section(soup, section_titles):
    """Extracts paragraphs and list items under given section titles."""
    data = {}
    for title in section_titles:
        section = soup.find(lambda tag: tag.name in ['h2', 'h3'] and title.lower() in tag.get_text(strip=True).lower())
        if section:
            content = []
            for sib in section.find_next_siblings():
                if sib.name in ['h2', 'h3']:
                    break
                if sib.name == 'p':
                    content.append(sib.get_text(strip=True))
                if sib.name in ['ul', 'ol']:
                    for li in sib.find_all('li'):
                        content.append(li.get_text(strip=True))
            data[title] = content
    return data

def scrape_mayo_disease_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    disease = soup.find('h1').get_text(strip=True) if soup.find('h1') else ''
    
    # Extract Diagnosis & treatment link from header nav
    diag_link = ''
    nav = soup.find('nav', {'aria-label': 'Secondary'})
    if nav:
        a = nav.find('a', string=lambda s: s and 'diagnosis' in s.lower())
        if a and a.has_attr('href'):
            diag_link = a['href']
    
    # Extract main sections
    section_titles = [
        'Symptoms', 'Causes', 'When to see a doctor', 'Risk factors', 'Complications'
    ]
    sections = extract_section(soup, section_titles)
    
    # Add more sections as needed
    return {
        'disease': disease,
        'diagnosis_treatment_link': diag_link,
        **sections
    }
# To process multiple URLs, loop over your mayoclinic_links.json and save all results to a file.

if __name__ == "__main__":
    # Load all links from mayoclinic_links.json
    with open("mrinmoy/mayoclinic_links.json", "r", encoding="utf-8") as f:
        links_data = json.load(f)
    all_results = []
    diag_links = []
    failed_records = []
    for idx, entry in enumerate(links_data, 1):
        url = entry["href"]
        print(f"[{idx}/{len(links_data)}] Scraping: {url}")
        try:
            data = scrape_mayo_disease_page(url)
            all_results.append(data)
            # Store diagnosis link and disease name if available
            if data.get("diagnosis_treatment_link"):
                diag_links.append({
                    "disease": data.get("disease", ""),
                    "diagnosis_treatment_link": data["diagnosis_treatment_link"]
                })
            # If no useful data was extracted, consider as failed
            if not data.get("disease") and not any(data.get(k) for k in ["Symptoms", "Causes", "When to see a doctor", "Risk factors", "Complications"]):
                failed_records.append({"url": url})
            print(f"  -> Success: {data.get('disease', '')}")
        except Exception as e:
            print(f"  -> Error scraping {url}: {e}")
            failed_records.append({"url": url, "error": str(e)})
    # Save all results
    with open("mayoclinic_disease_data.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    # Save diagnosis links
    with open("mayoclinic_diagnosis_links.json", "w", encoding="utf-8") as f:
        json.dump(diag_links, f, indent=2, ensure_ascii=False)
    # Save failed records
    with open("mayoclinic_failed_records.json", "w", encoding="utf-8") as f:
        json.dump(failed_records, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(all_results)} disease entries, {len(diag_links)} diagnosis links, and {len(failed_records)} failed records.")