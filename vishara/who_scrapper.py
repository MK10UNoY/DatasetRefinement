import requests
from bs4 import BeautifulSoup
import os
import json
import random
from time import sleep


BASE_URL = "https://www.who.int"
LIST_PAGE = "https://www.who.int/news-room/fact-sheets"
OUTPUT_DIR = "separated jsons/who_diseases"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}


import json

def get_disease_links():
    with open("separated jsons/who_disease_links.json", "r", encoding="utf-8") as f:
        return json.load(f)


def scrape_who_page(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"[ERROR] Failed to fetch {url}: {e}")
        return {}

    soup = BeautifulSoup(response.text, "html.parser")
    content = {}
    current_section = None

    SKIP_SECTIONS = ["WHO response", "Introduction", "References"]

    for tag in soup.find_all(['h2', 'p', 'ul']):
        if tag.name == 'h2':
            section_title = tag.get_text(strip=True)
            if section_title in SKIP_SECTIONS:
                current_section = None  # Don't record content under this section
            else:
                current_section = section_title
                content[current_section] = []
        elif current_section:
            if tag.name == 'p':
                text = tag.get_text(strip=True)
                if text:
                    content.setdefault(current_section, []).append(text)
            elif tag.name == 'ul':
                bullet_points = [li.get_text(strip=True) for li in tag.find_all('li')]
                if bullet_points:
                    content.setdefault(current_section, []).extend(bullet_points)

    return content



def save_disease_data(name, data):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, f"{name}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"[SUCCESS] Saved: {filepath}")


def main():
    disease_links = get_disease_links()

    for name, url in disease_links.items():
        print(f"\n[INFO] Scraping {name.title()}...")
        data = scrape_who_page(url)

        if not data:
            print(f"[WARN] Skipping {name}, no data scraped.")
            continue

        save_disease_data(name, data)
        sleep(random.uniform(2.5, 5.0))  # Respectful delay

if __name__ == "__main__":
    main()
