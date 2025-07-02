# DataSetRefinement

## Problem Statement

Medical data about diseases and symptoms is scattered across many sources, often in unstructured or inconsistent formats. This makes it hard for researchers, developers, and healthcare professionals to analyze, compare, or use this information for building tools, conducting research, or training machine learning models. There is a need for a unified, clean, and structured dataset that brings together disease and symptom information from trusted sources, making it easy to use for data analysis and AI applications.

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
LICENSE
```

---

## Key Features

- **Unified Data Pipeline:** Extracts, cleans, and structures data from PDFs, websites, and CSVs into a single, easy-to-use format.
- **Noise Reduction:** Removes irrelevant words and standardizes terminology for better analysis.
- **Category Organization:** Data is organized into clear categories (symptoms, causes, prognosis, etc.) for easier exploration.
- **ML & EDA Ready:** Datasets are ready for machine learning, exploratory data analysis, and visualization.
- **Extensible:** Modular scripts make it easy to add new data sources or processing steps.

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

This project is licensed under the [MIT License](LICENSE). 