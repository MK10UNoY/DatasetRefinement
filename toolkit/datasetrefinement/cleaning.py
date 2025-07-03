import csv
import re
import json

# Define a set of medically unimportant/common stopwords
STOPWORDS = set([
    'include', 'includes', 'including', 'may', 'the', 'and', 'or', 'with', 'of', 'to', 'in', 'on', 'by', 'for', 'from', 'as', 'is', 'are', 'be', 'can', 'will', 'if', 'that', 'this', 'which', 'such', 'other', 'than', 'not', 'it', 'at', 'an', 'a', 'has', 'have', 'had', 'was', 'were', 'but', 'so', 'do', 'does', 'did', 'should', 'would', 'could', 'also', 'all', 'any', 'some', 'most', 'more', 'less', 'very', 'much', 'many', 'often', 'sometimes', 'usually', 'always', 'never', 'about', 'after', 'before', 'during', 'over', 'under', 'between', 'through', 'per', 'each', 'every', 'both', 'either', 'neither', 'one', 'two', 'three', 'first', 'second', 'third', 'new', 'old', 'same', 'different', 'type', 'kind', 'form', 'part', 'area', 'side', 'place', 'way', 'time', 'day', 'week', 'month', 'year', 'patient', 'doctor', 'health', 'care', 'provider', 'person', 'people', 'child', 'children', 'adult', 'adults', 'man', 'woman', 'men', 'women', 'boy', 'girl', 'boys', 'girls', 'someone', 'anyone', 'everyone', 'noone', 'body', 'bodies', 'thing', 'things', 'something', 'anything', 'everything', 'nothing', 'cause', 'causes', 'caused', 'due', 'result', 'results', 'resulting', 'lead', 'leads', 'leading', 'make', 'makes', 'made', 'get', 'gets', 'got', 'become', 'becomes', 'became', 'develop', 'develops', 'developed', 'developing', 'show', 'shows', 'showed', 'showing', 'appear', 'appears', 'appeared', 'appearing', 'seem', 'seems', 'seemed', 'seeming', 'look', 'looks', 'looked', 'looking', 'feel', 'feels', 'felt', 'feeling', 'experience', 'experiences', 'experienced', 'experiencing', 'occur', 'occurs', 'occurred', 'occurring', 'present', 'presents', 'presented', 'presenting', 'seen', 'see', 'sees', 'saw', 'seeing', 'found', 'find', 'finds', 'finding', 'give', 'gives', 'gave', 'given', 'take', 'takes', 'took', 'taken', 'use', 'uses', 'used', 'using', 'list', 'lists', 'listed', 'listing', 'example', 'examples', 'like', 'among', 'amongst', 'within', 'without', 'outside', 'inside', 'around', 'near', 'far', 'close', 'away', 'toward', 'towards', 'against', 'across', 'along', 'beside', 'beyond', 'except', 'following', 'past', 'since', 'till', 'until', 'upon', 'via', 'yet', 'still', 'already', 'just', 'even', 'ever', 'once', 'twice', 'thrice', 'again', 'further', 'moreover', 'however', 'therefore', 'thus', 'hence', 'otherwise', 'meanwhile', 'consequently', 'accordingly', 'besides', 'likewise', 'similarly', 'additionally', 'furthermore', 'nonetheless', 'nevertheless', 'regardless', 'instead', 'regarding', 'concerning', 'despite', 'although', 'though', 'whereas', 'while', 'unless', 'whether', 'nor'
])

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

WORD_PATTERN = re.compile(r"\b[\w'-]+\b")


def clean_csv(input_path, output_path):
    """
    Cleans a CSV file by removing stopwords from the symptoms column (assumed to be column 2).
    """
    with open(input_path, 'r', encoding='latin1') as infile, \
         open(output_path, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        for row in reader:
            if len(row) < 2:
                writer.writerow(row)
                continue
            symptoms_text = row[1]
            words = WORD_PATTERN.findall(symptoms_text.lower())
            filtered = [w for w in words if w not in STOPWORDS]
            cleaned_symptoms = ' '.join(filtered)
            new_row = [row[0], cleaned_symptoms] + row[2:]
            writer.writerow(new_row)

def flatten_and_filter_json(input_path, output_path, properties=None):
    """
    Flattens and filters properties in a JSON file, removing irrelevant lines.
    Args:
        input_path (str): Path to the input JSON file.
        output_path (str): Path to save the cleaned JSON file.
        properties (list, optional): List of properties to flatten and filter.
    """
    if properties is None:
        properties = ['Symptoms', 'Causes', 'When to see a doctor', 'Risk factors', 'Complications', 'Prevention']
    with open(input_path, encoding='utf-8') as f:
        data = json.load(f)
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
    for obj in data:
        for prop in properties:
            if prop in obj:
                obj[prop] = flatten_section(obj[prop])
    # Remove objects where all properties are empty
    filtered = []
    for obj in data:
        if any(obj.get(prop) for prop in properties):
            filtered.append(obj)
    filtered.sort(key=lambda x: x.get('id', float('inf')))
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(filtered, f, ensure_ascii=False, indent=2)

def clean_file(input_path, output_path):
    """
    Main entry point for the toolkit. Dispatches cleaning based on file type.
    """
    if input_path.lower().endswith('.csv'):
        return clean_csv(input_path, output_path)
    elif input_path.lower().endswith('.json'):
        return flatten_and_filter_json(input_path, output_path)
    else:
        raise ValueError(f"Unsupported file type for cleaning: {input_path}") 