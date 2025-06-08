import json
import time
import requests
from bs4 import BeautifulSoup
import os

# Path to the input and output files
INPUT_PATH = os.path.join(os.path.dirname(__file__), 'mayoclinic_diagnosis_links_xpath2.json')
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), 'mayoclinic_diagnosis_links_xpath2_refilled.json')

# Helper function to extract diagnosis link from a Mayo Clinic disease page
def extract_diagnosis_link(url):
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            print(f"Failed to fetch {url}: {resp.status_code}")
            return None
        soup = BeautifulSoup(resp.text, 'html.parser')
        # Look for anchor tags with text containing 'Diagnosis' or href containing 'diagnosis-treatment'
        for a in soup.find_all('a', href=True):
            text = a.get_text(strip=True).lower()
            href = a['href']
            if ('diagnosis' in text or 'diagnosis' in href) and 'diagnosis-treatment' in href:
                # Make sure it's a full URL
                if href.startswith('http'):
                    return href
                else:
                    return 'https://www.mayoclinic.org' + href
        return None
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

def main():
    with open(INPUT_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    updated = 0
    for entry in data:
        if entry.get('diagnosis_link') is None:
            url = entry.get('url') or entry.get('disease_url')
            if not url:
                print(f"No URL for entry: {entry}")
                continue
            print(f"Scraping diagnosis link for: {url}")
            diagnosis_link = extract_diagnosis_link(url)
            if diagnosis_link:
                entry['diagnosis_link'] = diagnosis_link
                print(f"Found: {diagnosis_link}")
                updated += 1
            else:
                print(f"Diagnosis link not found for {url}")
            time.sleep(1)  # Be polite to the server

    print(f"Updated {updated} entries.")
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved updated data to {OUTPUT_PATH}")

if __name__ == '__main__':
    main()
