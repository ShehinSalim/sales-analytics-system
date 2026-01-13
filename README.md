SALES ANALYTICS SYSTEM

This project is a Sales Data Analytics System built using Python.
It reads and cleans messy sales transaction data, validates and filters transactions,
fetches product data from the DummyJSON API, enriches sales records, performs analytics,
and generates a comprehensive report.


FOLDER STRUCTURE

sales-analytics-system/
├── README.md
├── main.py
├── requirements.txt
├── data/
│   ├── sales_data.txt
│   └── enriched_sales_data.txt (generated)
├── output/
│   └── sales_report.txt (generated)
└── utils/
    ├── file_handler.py
    ├── data_processor.py
    └── api_handler.py


REQUIREMENTS

- Python 3.x
- requests

Install dependencies:
pip install -r requirements.txt


HOW TO RUN THE PROJECT

Step 1: Open terminal in project folder:
cd sales-analytics-system

Step 2: Run the program:
python main.py


WHAT HAPPENS WHEN YOU RUN IT?

The system runs in this order:

1. Reads sales data file: data/sales_data.txt
2. Parses and cleans transactions
3. Displays filter options (region + amount range)
4. Validates transactions (removes invalid ones)
5. Performs all data analysis functions
6. Fetches product data from the API
7. Enriches sales transactions using API data
8. Saves enriched dataset to: data/enriched_sales_data.txt
9. Generates report to: output/sales_report.txt


OUTPUT FILES GENERATED

After a successful run, these files are created:
- data/enriched_sales_data.txt
- output/sales_report.txt


API USED

DummyJSON Products API
Base URL: https://dummyjson.com/products

Fetch all products (limit 100):
https://dummyjson.com/products?limit=100


NOTES

- The program handles encoding issues by trying multiple encodings.
- Invalid records are removed based on validation rules.
- API enrichment matches ProductIDs by extracting the numeric part (example: P101 → 101)
  and mapping it into the DummyJSON range (1–100) for successful enrichment.


AUTHOR

Created by: SHEHIN SALIM
