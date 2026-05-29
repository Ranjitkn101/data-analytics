Data Cleaning & Exploratory Data Analysis (EDA) Project
A production‑style mini‑project demonstrating data cleaning, validation, EDA, and automated testing using Python.
This project simulates a real‑world data quality workflow where raw operational data contains inconsistencies, missing values, and formatting issues.

python-data-cleaning-eda/
│── data/
│   ├── sales_raw.csv          # Raw input data (intentionally messy)
│   └── sales_clean.csv        # Output after cleaning
│
│── src/
│   ├── __init__.py
│   ├── clean.py               # Cleaning logic
│   ├── validate.py            # Validation rules
│   ├── eda.py                 # Summary + missing value analysis
│   └── utils.py               # Load/save helpers
│
│── tests/
│   ├── __init__.py
│   ├── test_clean.py          # Unit tests for cleaning
│   └── test_validate.py       # Unit tests for validation
│
│── notebook.ipynb             # Interactive EDA
│── README.md                  # Documentation

## Objective
The goal of this project is to:

Clean raw sales data containing bad formats, missing values, invalid dates, negative numbers, and duplicates

Apply validation rules to ensure data quality

Perform EDA to understand distributions, missing values, and summary statistics

Use unit tests to ensure cleaning logic is reliable and production‑ready

Demonstrate a modular, maintainable, testable Python project structure

## Raw Data Issues
The raw dataset (sales_raw.csv) intentionally includes:

Mixed date formats

Invalid dates (e.g., 2023-13-05)

Missing product names

Missing store IDs

Negative sales values

Non‑numeric quantities

Duplicate rows

Blank or NaN values

This simulates real‑world messy data commonly found in retail, finance, and operations datasets.

## Cleaning Logic
The cleaning pipeline performs:

Standardizing date formats

Removing invalid dates


## Usage & Workflow

### 1. Load Raw Data

```python
import pandas as pd
from src.clean import clean_sales
from src.validate import validate_sales
from src.eda import summary_stats, missing_values

df = pd.read_csv("data/sales_raw.csv")
df.head()
```

This loads the raw sales data containing intentional quality issues (mixed formats, missing values, invalid dates, etc.).

### 2. Inspect Raw Data

```python
df.info()
df.describe(include="all")
```

Review the data structure, data types, and summary statistics to understand the scope of cleaning needed.

### 3. Clean Data

```python
cleaned = clean_sales(df)
cleaned.head()
```

The `clean_sales()` function applies the cleaning pipeline:
- Standardizes date formats
- Removes invalid dates
- Fills missing product names with "Unknown"
- Fills missing store IDs with median
- Removes negative sales values
- Converts non-numeric quantities to numeric
- Removes duplicate rows

### 4. Validate Cleaned Data

```python
validate_sales(cleaned)
print("Validation passed — cleaned dataset is valid.")
```

Validation rules ensure:
- No missing critical values
- All dates are valid
- All sales values are non-negative
- All quantities are numeric and positive

### 5. Exploratory Data Analysis (EDA)

```python
summary_stats(cleaned)
missing_values(cleaned)
```

**Output Example:**
```
Summary Statistics:
  sales (mean): 500.23
  sales (median): 475.50
  quantity (mean): 5.12
  
Missing Values: 0 (data is now clean!)
```

### 6. Visualization Examples

#### Sales Distribution
```python
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(8,5))
sns.histplot(cleaned["sales"], kde=True)
plt.title("Sales Distribution")
plt.show()
```

#### Daily Sales Over Time
```python
if "date" in cleaned.columns:
    cleaned["date"] = pd.to_datetime(cleaned["date"])
    daily = cleaned.groupby("date")["sales"].sum()
    
    plt.figure(figsize=(12, 5))
    daily.plot()
    plt.title("Daily Sales Over Time")
    plt.ylabel("Sales")
    plt.xlabel("Date")
    plt.grid(True)
    plt.show()
```

#### Sales by Product
```python
if "product" in cleaned.columns:
    cleaned.groupby("product")["sales"].sum().sort_values().plot(kind="bar", figsize=(10,5))
    plt.title("Sales by Product")
    plt.ylabel("Total Sales")
    plt.show()
```

### 7. Save Cleaned Data

```python
cleaned.to_csv("data/sales_clean.csv", index=False)
print("Saved cleaned dataset to data/sales_clean.csv")
```

## Running Tests

From terminal:

```bash
# Activate virtual environment
(Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (& .\venv\Scripts\Activate.ps1)

# Run cleaning pipeline
python run_cleaning.py
# Output: Cleaning pipeline completed successfully.

# Run unit tests
pytest -v
# Output:
# tests/test_clean.py::test_clean_sales PASSED       [ 50%]
# tests/test_validate.py::test_validate_sales PASSED  [100%]
# ========================== 2 passed in 0.60s ==========================
```

## Notebook Execution

The interactive notebook (`notebook.ipynb`) demonstrates the full workflow with visualizations and detailed output. Run it using Jupyter:

```bash
jupyter notebook
```

The notebook includes:
- Data loading and inspection
- Cleaning pipeline execution
- Validation checks
- EDA summary statistics
- Distribution analysis (histograms, boxplots)
- Time series visualization (daily sales trends)
- Product-level sales breakdown

## terminal execution 

(venv) PS C:\D_Drive_Study\data_analysts\Feature\data-analytics\python-data-cleaning-eda> python run_cleaning.py
Cleaning pipeline completed successfully.
(venv) PS C:\D_Drive_Study\data_analysts\Feature\data-analytics\python-data-cleaning-eda> pytest -v
========================== test session starts ==========================
platform win32 -- Python 3.10.11, pytest-9.0.3, pluggy-1.6.0 -- C:\D_Drive_Study\data_analysts\Feature\data-analytics\python-data-cleaning-eda\venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\D_Drive_Study\data_analysts\Feature\data-analytics\python-data-cleaning-eda
collected 2 items                                                        

tests/test_clean.py::test_clean_sales PASSED                       [ 50%]
tests/test_validate.py::test_validate_sales PASSED                 [100%]

