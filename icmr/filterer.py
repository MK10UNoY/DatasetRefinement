import csv
import re

# Path to your CSV file
csv_file = 'icmr/cleaned_disease_symptoms.csv'

# Regular expression to match words (alphanumeric, including hyphens and apostrophes)
word_pattern = re.compile(r"\b[\w'-]+\b")

# Define a set of medically unimportant/common stopwords
stopwords = set([
    'include', 'includes', 'including', 'may', 'the', 'and', 'or', 'with', 'of', 'to', 'in', 'on', 'by', 'for', 'from', 'as', 'is', 'are', 'be', 'can', 'will', 'if', 'that', 'this', 'which', 'such', 'other', 'than', 'not', 'it', 'at', 'an', 'a', 'has', 'have', 'had', 'was', 'were', 'but', 'so', 'do', 'does', 'did', 'should', 'would', 'could', 'also', 'all', 'any', 'some', 'most', 'more', 'less', 'very', 'much', 'many', 'often', 'sometimes', 'usually', 'always', 'never', 'about', 'after', 'before', 'during', 'over', 'under', 'between', 'through', 'per', 'each', 'every', 'both', 'either', 'neither', 'one', 'two', 'three', 'first', 'second', 'third', 'new', 'old', 'same', 'different', 'type', 'kind', 'form', 'part', 'area', 'side', 'place', 'way', 'time', 'day', 'week', 'month', 'year', 'patient', 'doctor', 'health', 'care', 'provider', 'person', 'people', 'child', 'children', 'adult', 'adults', 'man', 'woman', 'men', 'women', 'boy', 'girl', 'boys', 'girls', 'someone', 'anyone', 'everyone', 'noone', 'body', 'bodies', 'thing', 'things', 'something', 'anything', 'everything', 'nothing', 'cause', 'causes', 'caused', 'due', 'result', 'results', 'resulting', 'lead', 'leads', 'leading', 'make', 'makes', 'made', 'get', 'gets', 'got', 'become', 'becomes', 'became', 'develop', 'develops', 'developed', 'developing', 'show', 'shows', 'showed', 'showing', 'appear', 'appears', 'appeared', 'appearing', 'seem', 'seems', 'seemed', 'seeming', 'look', 'looks', 'looked', 'looking', 'feel', 'feels', 'felt', 'feeling', 'experience', 'experiences', 'experienced', 'experiencing', 'occur', 'occurs', 'occurred', 'occurring', 'present', 'presents', 'presented', 'presenting', 'seen', 'see', 'sees', 'saw', 'seeing', 'found', 'find', 'finds', 'finding', 'give', 'gives', 'gave', 'given', 'take', 'takes', 'took', 'taken', 'use', 'uses', 'used', 'using', 'list', 'lists', 'listed', 'listing', 'example', 'examples', 'like', 'among', 'amongst', 'within', 'without', 'outside', 'inside', 'around', 'near', 'far', 'close', 'away', 'toward', 'towards', 'against', 'across', 'along', 'beside', 'beyond', 'except', 'following', 'past', 'since', 'till', 'until', 'upon', 'via', 'yet', 'still', 'already', 'just', 'even', 'ever', 'once', 'twice', 'thrice', 'again', 'further', 'moreover', 'however', 'therefore', 'thus', 'hence', 'otherwise', 'meanwhile', 'consequently', 'accordingly', 'besides', 'likewise', 'similarly', 'additionally', 'furthermore', 'nonetheless', 'nevertheless', 'regardless', 'instead', 'regarding', 'concerning', 'despite', 'although', 'though', 'whereas', 'while', 'unless', 'whether', 'nor'
])

# Read, clean, and write to a new CSV
with open(csv_file, 'r', encoding='latin1') as infile, \
     open('icmr/cleaned_disease_symptoms_filtered.csv', 'w', encoding='utf-8', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    for row in reader:
        if len(row) < 2:
            writer.writerow(row)
            continue
        symptoms_text = row[1]
        # Tokenize, remove stopwords, and reconstruct
        words = word_pattern.findall(symptoms_text.lower())
        filtered = [w for w in words if w not in stopwords]
        # Reconstruct the symptoms text (join with space, or use '; ' for better readability)
        cleaned_symptoms = ' '.join(filtered)
        new_row = [row[0], cleaned_symptoms] + row[2:]
        writer.writerow(new_row)