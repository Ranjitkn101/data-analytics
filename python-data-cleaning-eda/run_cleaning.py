from src.utils import load_csv, save_csv
from src.clean import clean_sales
from src.validate import validate_sales

def main():
    df = load_csv("data/sales_raw.csv")
    cleaned = clean_sales(df)
    validate_sales(cleaned)
    save_csv(cleaned, "data/sales_clean.csv")
    print("Cleaning pipeline completed successfully.")

if __name__ == "__main__":
    main()
