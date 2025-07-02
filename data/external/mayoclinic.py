import requests
from bs4 import BeautifulSoup
import string
import json

def extract_ul_li_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = []
    for ul in soup.find_all('ul'):
        for li in ul.find_all('li'):
            a = li.find('a', href=True)
            if a:
                results.append({
                    'link_text': a.get_text(strip=True),
                    'href': a['href']
                })
    return results

# Scrape all letters A-Z
def scrape_all_letters():
    base_url = 'https://www.mayoclinic.org/diseases-conditions/index?letter={}'

    all_links = []
    for letter in string.ascii_uppercase:
        url = base_url.format(letter)
        print(f"Scraping: {url}")
        links = extract_ul_li_links(url)
        all_links.extend(links)
    return all_links

# Example usage:
if __name__ == "__main__":
    all_links = scrape_all_letters()
    # Save to JSON file
    with open("mayoclinic_links.json", "w", encoding="utf-8") as f:
        json.dump(all_links, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(all_links)} links to mayoclinic_links.json")