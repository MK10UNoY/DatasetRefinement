import json
import random
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import classification_report

# Load data
with open('symptoms_vs_disease.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Build symptom vocabulary
all_symptoms = set()
for entry in data:
    all_symptoms.update([s.lower().strip() for s in entry['symptoms']])
all_symptoms = sorted(all_symptoms)
mlb = MultiLabelBinarizer(classes=all_symptoms)

# Data augmentation: generate synthetic cases
X, y = [], []
for entry in data:
    symptoms = [s.lower().strip() for s in entry['symptoms']]
    disease = entry['disease']
    # Generate N synthetic cases per disease
    for _ in range(20):
        n = random.randint(max(1, len(symptoms)//2), len(symptoms))
        sampled = random.sample(symptoms, n)
        # Optionally add noise
        if random.random() < 0.2:
            sampled += random.sample([s for s in all_symptoms if s not in symptoms], 1)
        X.append(sampled)
        y.append(disease)

X_bin = mlb.fit_transform(X)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X_bin, y, test_size=0.2, random_state=42)

# Train model
clf = RandomForestClassifier()
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))

# Predict function
def predict_disease(symptom_list):
    input_vec = mlb.transform([symptom_list])
    return clf.predict(input_vec)[0]

# Example usage
print(predict_disease(['fever', 'nausea', 'vomiting']))
