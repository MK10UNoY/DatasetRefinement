import json

INPUT_PATH = 'c:/Users/MRINMOY/DataSetRefinement/mrinmoy/final/mayoclinic_scraped_sections_with_symptoms.json'
OUTPUT_PATH = 'c:/Users/MRINMOY/DataSetRefinement/mrinmoy/final/mayoclinic_scraped_sections_with_all_flat.json'

PROPERTIES = [
    'Symptoms', 'Causes', 'When to see a doctor', 'Risk factors', 'Complications', 'Prevention'
]

# Simple flatten: paragraphs + all nested list text, filter out empty/irrelevant lines
BAD_PHRASES = set([
    'menu', 'request appointment', 'find a doctor', 'locations', 'contact us', 'privacy policy',
    'terms & conditions', 'notice of privacy practices', 'notice of nondiscrimination', 'site map',
    'facebook', 'youtube', 'linkedin', 'instagram', 'english', 'español', 'العربية', '简体中文',
    'patient care & health information', 'diseases & conditions', 'doctors & departments', 'care at mayo clinic',
    'policy', 'ad choices', 'advertising', 'newsletter', 'press', 'login', 'sign up', 'about this site',
    'appointments', 'financial services', 'international locations', 'media requests', 'news network', 'refer a patient',
    'executive health program', 'international business collaborations', 'facilities & real estate', 'supplier information',
    'student & faculty portal', 'degree programs', 'admissions requirements', 'research faculty', 'laboratories',
    'x', '©', 'copyright', 'all rights reserved', 'mayo foundation', 'mayo clinic does not endorse', 'advertising revenue',
    'check out these best-sellers', 'make a gift now', 'explore careers', 'sign up for free e-newsletters', 'about this site',
    'health information policy', 'medicare accountable care organization', 'media requests', 'price transparency',
    'askmayoexpert', 'clinical trials', 'mayo clinic alumni association', 'continuing medical education', 'video center',
    'journals & publications', 'mayo clinic health letter', 'books', 'press', 'newsletter', 'login', 'sign up', 'contact us',
    'opportunities', 'ad choices', 'advertising', 'newsletter', 'press', 'login', 'sign up', 'about this site',
    'appointments', 'financial services', 'international locations', 'media requests', 'news network', 'refer a patient',
    'executive health program', 'international business collaborations', 'facilities & real estate', 'supplier information',
    'student & faculty portal', 'degree programs', 'admissions requirements', 'research faculty', 'laboratories',
    'x', 'youtube', 'facebook', 'linkedin', 'instagram', 'terms & conditions', 'privacy policy', 'notice of privacy practices',
    'notice of nondiscrimination', 'accessibility statement', 'advertising & sponsorship policy', 'site map', 'manage cookies',
    'english', 'español', 'العربية', '简体中文', '© 1998-2025 mayo foundation for medical education and research (mfmer). all rights reserved.'
])

def flatten_section(section):
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
    # Filter: remove empty, too short, or obviously irrelevant lines
    filtered = [s.strip() for s in out if isinstance(s, str) and len(s.strip()) > 2 and not any(bad in s.lower() for bad in BAD_PHRASES)]
    return filtered

with open(INPUT_PATH, encoding='utf-8') as f:
    data = json.load(f)

for obj in data:
    for prop in PROPERTIES:
        if prop in obj:
            obj[prop] = flatten_section(obj[prop])

# Remove objects where all properties are empty
filtered = []
for obj in data:
    if any(obj.get(prop) for prop in PROPERTIES):
        filtered.append(obj)

filtered.sort(key=lambda x: x.get('id', float('inf')))

with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    json.dump(filtered, f, ensure_ascii=False, indent=2)

print(f"Flattened and filtered {PROPERTIES} for {len(filtered)} records. Saved to {OUTPUT_PATH} (sorted by id).")
