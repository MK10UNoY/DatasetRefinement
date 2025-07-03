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

toolkit/       # Python package and CLI for data extraction, cleaning, and modeling

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

## Toolkit Functionality Guide

The `toolkit/` folder contains a Python package and a modern, interactive CLI for extracting, cleaning, and modeling medical data.

### How to Run the Toolkit CLI

From the project root, run:
```
python -m toolkit
```

### Main Menu Options
- **Extract data**: Extracts structured data from PDFs, JSON, CSV, or websites.
- **Clean data**: Cleans and flattens extracted data for analysis or modeling.
- **Train model**: Trains a machine learning model on cleaned data.
- **Exit**: Exits the toolkit.

### Extraction Options
- **PDF**: Extracts disease and symptom sections from a PDF file.
- **JSON**: Flattens and standardizes disease data from a JSON file.
- **CSV**: (Future) For extracting from CSVs.
- **Web**:
  - **Single website link**: Extracts all visible text from a single web page.
  - **Multiple website links from JSON file**: Extracts all visible text from a list of URLs provided in a JSON file.

### Example Usage

**Extract from PDF:**
- Select "Extract data" → "PDF"
- Enter the path to your PDF file
- Enter an output path (or leave blank for default)

**Extract from Web:**
- Select "Extract data" → "Web"
- Choose "Single website link" or "Multiple website links from JSON file"
- Enter the URL or path to the JSON file with URLs
- Enter an output path (or leave blank for default)

**Clean Data:**
- Select "Clean data"
- Enter the path to your extracted data file (JSON or CSV)
- Enter an output path (or leave blank for default)

**Train Model:**
- Select "Train model"
- Enter the path to your cleaned data file

### Output
- All outputs are saved in the `output/` folder by default if no path is provided.
- Output file names are auto-generated based on the input file and action.

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