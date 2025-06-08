import json
import requests
from bs4 import BeautifulSoup

def extract_diagnosis_link(soup):
    # Robust: find any <a> with 'diagnosis' in text or '/diagnosis-treatment/' in href
    for nav in soup.find_all('nav'):
        for a in nav.find_all('a', href=True):
            text = a.get_text(strip=True).lower()
            href = a['href']
            if 'diagnosis' in text or '/diagnosis-treatment/' in href:
                return href
    return None

def main():
    with open('mrinmoy/mayoclinic_diagnosis_links_xpath2.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    updated = 0
    for entry in data:
        if entry.get('diagnosis_link') is None and entry.get('href'):
            url = entry['href']
            print(f"Scraping for missing diagnosis link: {url}")
            try:
                resp = requests.get(url)
                soup = BeautifulSoup(resp.text, 'html.parser')
                diag_link = extract_diagnosis_link(soup)
                entry['diagnosis_link'] = diag_link
                print(f"  -> Found: {diag_link}")
                updated += 1
            except Exception as e:
                print(f"  -> Error: {e}")
                entry['diagnosis_link'] = None
                entry['error'] = str(e)
    with open('mrinmoy/mayoclinic_diagnosis_links_xpath2_refilled.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Updated {updated} missing diagnosis links and saved to mayoclinic_diagnosis_links_xpath2_refilled.json")

if __name__ == "__main__":
    main()
