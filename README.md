# DataSetRefinement

## Project Overview

This project collects, cleans, and organizes medical data about diseases and symptoms from multiple sources. The goal is to create high-quality, structured datasets for research, machine learning, and healthcare applications.

---

## Folder Structure

```
data/
  raw/         # Original, unprocessed data (PDFs, CSVs, JSONs)
  processed/   # Cleaned and structured datasets
  external/    # Data from external sources (Harvard, WHO, NHS, etc.)

notebooks/     # Jupyter notebooks for EDA and analysis

scripts/
  extraction/  # Scripts for extracting data from sources
  cleaning/    # Scripts for cleaning and flattening data
  modeling/    # Scripts for training and evaluating ML models

utils/         # Helper functions and utilities

outputs/       # Model outputs, logs, and results

README.md
requirements.txt
.gitignore
```

---

## Key Features

- **Data Extraction:** Scripts to extract disease and symptom data from PDFs, websites, and other sources.
- **Data Cleaning:** Removes noise and irrelevant words, standardizes and flattens data.
- **Data Structuring:** Organizes data into clear categories (symptoms, causes, prognosis, etc.).
- **ML Ready:** Prepares datasets for machine learning, including synthetic data generation and model training scripts.
- **EDA Friendly:** Cleaned datasets are ready for exploratory data analysis and visualization.

---

## Getting Started

1. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

2. **Run extraction and cleaning scripts:**
   - See `scripts/extraction/` and `scripts/cleaning/` for details.

3. **Explore the data:**
   - Use the notebooks in `notebooks/` for EDA and analysis.

4. **Train models:**
   - Use scripts in `scripts/modeling/` to train and evaluate ML models.

---

## Who Should Use This

- Data scientists and researchers working on disease-symptom relationships.
- Developers building healthcare or diagnostic tools.
- Anyone needing clean, structured medical datasets for analysis or machine learning.

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

---

## License

Specify your license here. 