import requests
from bs4 import BeautifulSoup

base_url = "https://www.nhs.uk"
conditions_url = f"{base_url}/conditions/"

res = requests.get(conditions_url)
soup = BeautifulSoup(res.text, "html.parser")

disease_links = []
for a in soup.select("ul.nhsuk-list li a"):
    name = a.text.strip()
    link = base_url + a.get("href")
    disease_links.append((name, link))

print(f"✅ Found {len(disease_links)} conditions")
import time

disease_data = []

for name, link in disease_links[:10]:  # Limit for demo
    try:
        page = requests.get(link)
        psoup = BeautifulSoup(page.text, "html.parser")
        
        symptoms_text = ""
        for h2 in psoup.find_all("h2"):
            if "symptoms" in h2.text.lower():
                para = h2.find_next_sibling("p")
                if para:
                    symptoms_text = para.text.strip()
                break
        
        disease_data.append([name, symptoms_text])
    except Exception as e:
        disease_data.append([name, "Error"])

    time.sleep(1)  

print("✅ Symptoms extracted for sample pages")
import csv

with open("nhs_disease_symptoms.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Disease Name", "Symptoms"])
    writer.writerows(disease_data)

print("✅ Saved to nhs_disease_symptoms.csv")
