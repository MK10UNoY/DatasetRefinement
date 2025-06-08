import json
import requests
from bs4 import BeautifulSoup

def extract_diagnosis_link(soup):
    # Find all navs (in case there are multiple)
    for nav in soup.find_all('nav'):
        # Find all <a> tags in the nav
        for a in nav.find_all('a', href=True):
            text = a.get_text(strip=True).lower()
            href = a['href']
            if 'diagnosis' in text or '/diagnosis-treatment/' in href:
                return href
    return None
def main():
    with open('mrinmoy/mayoclinic_links_with_id.json', 'r', encoding='utf-8') as f:
        links = json.load(f)
    results = []
    for entry in links:
        url = entry.get('href')
        if not url:
            continue
        print(f"Scraping {url} (id={entry.get('id')})")
        try:
            resp = requests.get(url)
            soup = BeautifulSoup(resp.text, 'html.parser')
            diag_link = extract_diagnosis_link(soup)
            results.append({
                "id": entry.get("id"),
                "href": url,
                "diagnosis_link": diag_link
            })
            print(f"  -> Diagnosis link: {diag_link}")
        except Exception as e:
            print(f"  -> Error: {e}")
            results.append({
                "id": entry.get("id"),
                "href": url,
                "diagnosis_link": None,
                "error": str(e)
            })
    with open('mrinmoy/mayoclinic_diagnosis_links_xpath2.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(results)} records to mayoclinic_diagnosis_links_xpath2.json")

if __name__ == "__main__":
    main()