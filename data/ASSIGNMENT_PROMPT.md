Assignment Overview



You will build a Sales Data Analytics System that processes sales data, integrates with external APIs, performs analysis, and generates reports. This assignment tests your understanding of Python fundamentals including data structures, functions, file operations, API

integration, and error handling.



Submission Requirements



. GitHub Repository: Create a repository named sales-analytics-system



. Repository Structure:



sales-analytics-system/

-README.md

\- main.py

-utils/

-file\_handler.py

data\_processor.py

api\_handler.py

\- data/

-sales\_data.txt (provided)

output/

\- requirements.txt



. Include a detailed README.md explaining how to run your code

. Push all code to GitHub and submit the repository link



Problem Statement



You are a data analyst at an e-commerce company. Your manager has asked you to build a Python system that can:



1\. Read and clean messy sales transaction files

2\. Fetch real-time product information from an API

3\. Analyze sales patterns and customer behavior

4\. Generate comprehensive reports for business decisions



Dataset Provided



You will be provided with a file sales\_data.txt containing sales transactions with the following characteristics:



sales\_data.txt

File Format:



. Pipe-delimited ( | ) format

. Non-UTF-8 encoding (you'll need to handle encoding issues)

· Contains data quality issues:

o Some fields have comma-separated values within them

o Some rows may have missing or extra fields

o Some numeric values may have formatting issues (commas in numbers)

o Some records have invalid data (zero quantities, negative prices, wrong ID formats)

Sample Format:



TransactionID| Date| ProductID| ProductName| Quantity| UnitPrice| CustomerID| Region

T001|2024-12-01|P101|Laptop|2|45000|C001|North

T002|2024-12-01|P102|Mouse,Wireless|5|500|C002|South

T003|2024-12-02|P103|Keyboard|3|1,500|C003|East



Dataset Statistics:



. Total records in file: ~80 records

. Expected valid records after cleaning: ~70 records

. Expected invalid records: ~10 records

. Date range: December 2024



Note: The exact number of valid records depends on how you handle data quality issues during parsing and validation.



Data Cleaning Criteria



REMOVE These Records (Invalid):



. Missing CustomerID or Region -> Remove

. Quantity ≤ 0-> Remove

. UnitPrice ≤ 0-> Remove

. TransactionID not starting with 'T' -> Remove



Expected Invalid: ~10 records



CLEAN and KEEP These Records (Valid):

. Commas in ProductName (e.g., Mouse,Wireless ) -> Remove commas, Keep

. Commas in numbers (e.g., 1,500 ) -> Remove commas, convert to int/float, Keep

. Empty lines -> Skip

Expected Valid After Cleaning: ~70 records



Validation Output Required:



Your cleaning function must print:



Total records parsed: 80

Invalid records removed: 10

Valid records after cleaning: 70



Q:2

Part 1: Data File Handler \& Preprocessing (File I/O \& Error Handling)



Task 1.1: Read Sales Data with Encoding Handling



Create a function that reads the sales data file handling encoding issues.



File: utils/file\_handler.py



def read\_sales\_data(filename):



Reads sales data from file handling encoding issues



Returns: list of raw lines (strings)



Expected Output Format:

\['T001|2024-12-01|P101|Laptop|2|45000|C001|North', ... ]



Requirements:

\- Use 'with' statement

\- Handle different encodings (try 'utf-8', 'latin-1', 'cp1252')

\- Handle FileNotFoundError with appropriate error message

\- Skip the header row

\- Remove empty lines



Evaluation Criteria:



. V Successfully reads non-UTF-8 encoded file (5 points)

. V Returns list with exactly 50-100 transaction lines (3 points)

. V Proper error handling for FileNotFoundError (2 points)

Task 1.2: Parse and Clean Data



Create a function that parses raw data and handles data quality issues.



def parse\_transactions(raw\_lines):



Parses raw lines into clean list of dictionaries



Returns: list of dictionaries with keys:

\['TransactionID', 'Date', 'ProductID', 'ProductName',

'Quantity', 'UnitPrice', 'CustomerID', 'Region' ]



Expected Output Format:



'TransactionID': 'T001',

'Date': '2024-12-01',

'ProductID': 'P101',

'ProductName': 'Laptop',

'Quantity': 2,

'UnitPrice': 45000.0,

'CustomerID': 'C001',

'Region': 'North'



\# int type

\# float type



1



Requirements:

\- Split by pipe delimiter '|'

\- Handle commas within ProductName (remove or replace)

\- Remove commas from numeric fields and convert to proper types

\- Convert Quantity to int

\- Convert UnitPrice to float

\- Skip rows with incorrect number of fields



Evaluation Criteria:



. V Correctly parses all valid transactions (5 points)

. V Handles commas in ProductName field (3 points)

. V Handles commas in numeric fields (1,500-+ 1500) (3 points)

. V Correct data types (Quantity as int, UnitPrice as float) (4 points)



Task 1.3: Data Validation and Filtering



Create a function that validates and allows filtering of transactions.



def validate\_and\_filter(transactions, region=None, min\_amount=None, max\_amount=None):

&nbsp;   """

&nbsp;   Validates transactions and applies optional filters



&nbsp;   Parameters:

&nbsp;   - transactions: list of transaction dictionaries

&nbsp;   - region: filter by specific region (optional)

&nbsp;   - min\_amount: minimum transaction amount (Quantity \* UnitPrice) (optional)

&nbsp;   - max\_amount: maximum transaction amount (optional)



&nbsp;   Returns: tuple (valid\_transactions, invalid\_count, filter\_summary)



&nbsp;   Expected Output Format:

&nbsp;   (

&nbsp;       \[list of valid filtered transactions],

&nbsp;       5,  # count of invalid transactions

&nbsp;       {

&nbsp;           'total\_input': 100,

&nbsp;           'invalid': 5,

&nbsp;           'filtered\_by\_region': 20,

&nbsp;           'filtered\_by\_amount': 10,

&nbsp;           'final\_count': 65

&nbsp;       }

&nbsp;   )



&nbsp;   Validation Rules:

&nbsp;   - Quantity must be > 0

&nbsp;   - UnitPrice must be > 0

&nbsp;   - All required fields must be present

&nbsp;   - TransactionID must start with 'T'

&nbsp;   - ProductID must start with 'P'

&nbsp;   - CustomerID must start with 'C'



&nbsp;   Filter Display:

&nbsp;   - Print available regions to user before filtering

&nbsp;   - Print transaction amount range (min/max) to user

&nbsp;   - Show count of records after each filter applied

&nbsp;   """



Evaluation Criteria:



. V Validates all required conditions (4 points)

. V Filter functionality works correctly (3 points)

. V Displays available options to user (regions, amount range) (2 points)

. V Returns correct counts and summary (3 points)



Q:3



Part 2: Data Processing (Lists, Dictionaries \& Functions)



Task 2.1: Sales Summary Calculator



Create functions in utils/data\_processor.py :



a) Calculate Total Revenue



def calculate\_total\_revenue(transactions):

&nbsp;   """

&nbsp;   Calculates total revenue from all transactions



&nbsp;   Returns: float (total revenue)



&nbsp;   Expected Output: Single number representing sum of (Quantity \* UnitPrice)

&nbsp;   Example: 1545000.50

&nbsp;   """



Evaluation: Returns exact correct total (3 points)



b) Region-wise Sales Analysis



def region\_wise\_sales(transactions):

&nbsp;   """

&nbsp;   Analyzes sales by region



&nbsp;   Returns: dictionary with region statistics



&nbsp;   Expected Output Format:

&nbsp;   {

&nbsp;       'North': {

&nbsp;           'total\_sales': 450000.0,

&nbsp;           'transaction\_count': 15,

&nbsp;           'percentage': 29.13

&nbsp;       },

&nbsp;       'South': {...},

&nbsp;       ...

&nbsp;   }



&nbsp;   Requirements:

&nbsp;   - Calculate total sales per region

&nbsp;   - Count transactions per region

&nbsp;   - Calculate percentage of total sales

&nbsp;   - Sort by total\_sales in descending order

&nbsp;   """



Evaluation:



. V Correct totals per region (2 points)

. V Correct transaction counts (1 point)

. V Correct percentage calculations (1 point)



c) Top Selling Products



def top\_selling\_products(transactions, n=5):

&nbsp;   """

&nbsp;   Finds top n products by total quantity sold



&nbsp;   Returns: list of tuples



&nbsp;   Expected Output Format:

&nbsp;   \[

&nbsp;       ('Laptop', 45, 2250000.0),  # (ProductName, TotalQuantity, TotalRevenue)

&nbsp;       ('Mouse', 38, 19000.0),

&nbsp;       ...

&nbsp;   ]



&nbsp;   Requirements:

&nbsp;   - Aggregate by ProductName

&nbsp;   - Calculate total quantity sold

&nbsp;   - Calculate total revenue for each product

&nbsp;   - Sort by TotalQuantity descending

&nbsp;   - Return top n products

&nbsp;   """

Evaluation:



. V Correct aggregation (2 points)

. V Correct sorting (1 point)

. V Returns top n items (1 point)



d) Customer Purchase Analysis



def customer\_analysis(transactions):

&nbsp;   """

&nbsp;   Analyzes customer purchase patterns



&nbsp;   Returns: dictionary of customer statistics



&nbsp;   Expected Output Format:

&nbsp;   {

&nbsp;       'C001': {

&nbsp;           'total\_spent': 95000.0,

&nbsp;           'purchase\_count': 3,

&nbsp;           'avg\_order\_value': 31666.67,

&nbsp;           'products\_bought': \['Laptop', 'Mouse', 'Keyboard']

&nbsp;       },

&nbsp;       'C002': {...},

&nbsp;       ...

&nbsp;   }



&nbsp;   Requirements:

&nbsp;   - Calculate total amount spent per customer

&nbsp;   - Count number of purchases

&nbsp;   - Calculate average order value

&nbsp;   - List unique products bought

&nbsp;   - Sort by total\_spent descending

&nbsp;   """



Evaluation:



. VAll metrics calculated correctly (3 points)

. V Products list is unique (1 point)

. V Sorted correctly (1 point)



Evaluation:



. V All metrics calculated correctly (3 points)

. V Products list is unique (1 point)

. V Sorted correctly (1 point)



Task 2.2: Date-based Analysis



a) Daily Sales Trend



def daily\_sales\_trend(transactions):

&nbsp;   """

&nbsp;   Analyzes sales trends by date



&nbsp;   Returns: dictionary sorted by date



&nbsp;   Expected Output Format:

&nbsp;   {

&nbsp;       '2024-12-01': {

&nbsp;           'revenue': 125000.0,

&nbsp;           'transaction\_count': 8,

&nbsp;           'unique\_customers': 6

&nbsp;       },

&nbsp;       '2024-12-02': {...},

&nbsp;       ...

&nbsp;   }



&nbsp;   Requirements:

&nbsp;   - Group by date

&nbsp;   - Calculate daily revenue

&nbsp;   - Count daily transactions

&nbsp;   - Count unique customers per day

&nbsp;   - Sort chronologically

&nbsp;   """

Evaluation: All three metrics correct for each date (4 points)



b) Find Peak Sales Day



def find\_peak\_sales\_day(transactions):

&nbsp;   """

&nbsp;   Identifies the date with highest revenue



&nbsp;   Returns: tuple (date, revenue, transaction\_count)



&nbsp;   Expected Output Format:

&nbsp;   ('2024-12-15', 185000.0, 12)

&nbsp;   """



Evaluation: Returns correct date with metrics (3 points)



Task 2.3: Product Performance



a) Low Performing Products



def low\_performing\_products(transactions, threshold=10):

&nbsp;   """

&nbsp;   Identifies products with low sales



&nbsp;   Returns: list of tuples



&nbsp;   Expected Output Format:

&nbsp;   \[

&nbsp;       ('Webcam', 4, 12000.0),  # (ProductName, TotalQuantity, TotalRevenue)

&nbsp;       ('Headphones', 7, 10500.0),

&nbsp;       ...

&nbsp;   ]



&nbsp;   Requirements:

&nbsp;   - Find products with total quantity < threshold

&nbsp;   - Include total quantity and revenue

&nbsp;   - Sort by TotalQuantity ascending

&nbsp;   """



Evaluation: Correct identification and sorting (2 points)



Q: 4



Part 3: API Integration



Understanding the DummyJSON API



Base URL: https://dummyjson.com/products



How to use the API:



1\. Get ALL products (returns first 30 by default):



response = requests.get('https://dummyjson.com/products')

data = response.json()

\# data\['products'] contains list of all products

\# data\['total'] gives total count



2\. Get a SINGLE product by ID:

response = requests.get('https://dummyjson.com/products/1')

product = response.json()

\# Returns single product object



3\. Get specific number of products:

response = requests.get('https://dummyjson.com/products?limit=100')



4\. search products:

response = requests.get('https://dummyjson.com/products/search?q=phone')



Sample product Response:

{

&nbsp; "id": 1,

&nbsp; "title": "iPhone 9",

&nbsp; "description": "An apple mobile...",

&nbsp; "price": 549,

&nbsp; "category": "smartphones",

&nbsp; "brand": "Apple",

&nbsp; "rating": 4.69,

&nbsp; "stock": 94

}



Task 3.1: Fetch Product Details



Create functions in utils/api\_handler.py :



a) Fetch All Products



def fetch\_all\_products():

&nbsp;   """

&nbsp;   Fetches all products from DummyJSON API



&nbsp;   Returns: list of product dictionaries



&nbsp;   Expected Output Format:

&nbsp;   \[

&nbsp;       {

&nbsp;           'id': 1,

&nbsp;           'title': 'iPhone 9',

&nbsp;           'category': 'smartphones',

&nbsp;           'brand': 'Apple',

&nbsp;           'price': 549,

&nbsp;           'rating': 4.69

&nbsp;       },

&nbsp;       ...

&nbsp;   ]



&nbsp;   Requirements:

&nbsp;   - Fetch all available products (use limit=100)

&nbsp;   - Handle connection errors with try-except

&nbsp;   - Return empty list if API fails

&nbsp;   - Print status message (success/failure)

&nbsp;   """



Evaluation:



· V Successfully fetches products (3 points)

. Proper error handling (2 points)



b) Create Product Mapping



def create\_product\_mapping(api\_products):

&nbsp;   """

&nbsp;   Creates a mapping of product IDs to product info



&nbsp;   Parameters: api\_products from fetch\_all\_products()



&nbsp;   Returns: dictionary mapping product IDs to info



&nbsp;   Expected Output Format:

&nbsp;   {

&nbsp;       1: {'title': 'iPhone 9', 'category': 'smartphones', 'brand': 'Apple', 'rating': 4.69},

&nbsp;       2: {'title': 'iPhone X', 'category': 'smartphones', 'brand': 'Apple', 'rating': 4.44},

&nbsp;       ...

&nbsp;   }

&nbsp;   """

Evaluation: Correct dictionary structure (2 points)



Task 3.2: Enrich Sales Data



Important: This function should enrich your transaction data AND save it back to a new file.

def enrich\_sales\_data(transactions, product\_mapping):

&nbsp;   """

&nbsp;   Enriches transaction data with API product information



&nbsp;   Parameters:

&nbsp;   - transactions: list of transaction dictionaries

&nbsp;   - product\_mapping: dictionary from create\_product\_mapping()



&nbsp;   Returns: list of enriched transaction dictionaries



&nbsp;   Expected Output Format (each transaction):

&nbsp;   {

&nbsp;       'TransactionID': 'T001',

&nbsp;       'Date': '2024-12-01',

&nbsp;       'ProductID': 'P101',

&nbsp;       'ProductName': 'Laptop',

&nbsp;       'Quantity': 2,

&nbsp;       'UnitPrice': 45000.0,

&nbsp;       'CustomerID': 'C001',

&nbsp;       'Region': 'North',

&nbsp;       # NEW FIELDS ADDED FROM API:

&nbsp;       'API\_Category': 'laptops',

&nbsp;       'API\_Brand': 'Apple',

&nbsp;       'API\_Rating': 4.7,

&nbsp;       'API\_Match': True  # True if enrichment successful, False otherwise

&nbsp;   }



&nbsp;   Enrichment Logic:

&nbsp;   - Extract numeric ID from ProductID (P101 → 101, P5 → 5)

&nbsp;   - If ID exists in product\_mapping, add API fields

&nbsp;   - If ID doesn't exist, set API\_Match to False and other fields to None

&nbsp;   - Handle all errors gracefully



&nbsp;   File Output:

&nbsp;   - Save enriched data to 'data/enriched\_sales\_data.txt'

&nbsp;   - Use same pipe-delimited format

&nbsp;   - Include new columns in header

&nbsp;   """

Also create this helper function:



def save\_enriched\_data(enriched\_transactions, filename='data/enriched\_sales\_data.txt'):

&nbsp;   """

&nbsp;   Saves enriched transactions back to file



&nbsp;   Expected File Format:

&nbsp;   TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|API\_Category|API\_Brand|API\_Rating|API\_Match

&nbsp;   T001|2024-12-01|P101|Laptop|2|45000.0|C001|North|laptops|Apple|4.7|True

&nbsp;   ...



&nbsp;   Requirements:

&nbsp;   - Create output file with all original + new fields

&nbsp;   - Use pipe delimiter

&nbsp;   - Handle None values appropriately

&nbsp;   """



Evaluation:



. V Correctly extracts numeric IDs (2 points)

. V Enriches with API data (3 points)

. V Handles missing products (2 points)

. V Saves to file correctly (3 points)



Q:5



Part 4: Report Generation



Task 4.1: Generate Comprehensive Text Report



Create a function that writes a detailed report to output/sales\_report.txt :

def generate\_sales\_report(transactions, enriched\_transactions, output\_file='output/sales\_report.txt'):

&nbsp;   """

&nbsp;   Generates a comprehensive formatted text report



&nbsp;   Report Must Include (in this order):



&nbsp;   1. HEADER

&nbsp;      - Report title

&nbsp;      - Generation date and time

&nbsp;      - Total records processed



&nbsp;   2. OVERALL SUMMARY

&nbsp;      - Total Revenue (formatted with commas)

&nbsp;      - Total Transactions

&nbsp;      - Average Order Value

&nbsp;      - Date Range of data



&nbsp;   3. REGION-WISE PERFORMANCE

&nbsp;      - Table showing each region with:

&nbsp;        \* Total Sales Amount

&nbsp;        \* Percentage of Total

&nbsp;        \* Transaction Count

&nbsp;      - Sorted by sales amount descending



&nbsp;   4. TOP 5 PRODUCTS

&nbsp;      - Table with columns: Rank, Product Name, Quantity Sold, Revenue



&nbsp;   5. TOP 5 CUSTOMERS

&nbsp;      - Table with columns: Rank, Customer ID, Total Spent, Order Count



&nbsp;   6. DAILY SALES TREND

&nbsp;      - Table showing: Date, Revenue, Transactions, Unique Customers



&nbsp;   7. PRODUCT PERFORMANCE ANALYSIS

&nbsp;      - Best selling day

&nbsp;      - Low performing products (if any)

&nbsp;      - Average transaction value per region



&nbsp;   8. API ENRICHMENT SUMMARY

&nbsp;      - Total products enriched

&nbsp;      - Success rate percentage

&nbsp;      - List of products that couldn't be enriched



&nbsp;   Expected Output Format (sample):

&nbsp;   ============================================

&nbsp;          SALES ANALYTICS REPORT

&nbsp;        Generated: 2024-12-18 14:30:22

&nbsp;        Records Processed: 95

&nbsp;   ============================================



&nbsp;   OVERALL SUMMARY

&nbsp;   --------------------------------------------

&nbsp;   Total Revenue:        ₹15,45,000.00

&nbsp;   Total Transactions:   95

&nbsp;   Average Order Value:  ₹16,263.16

&nbsp;   Date Range:           2024-12-01 to 2024-12-31



&nbsp;   REGION-WISE PERFORMANCE

&nbsp;   --------------------------------------------

&nbsp;   Region    Sales         % of Total  Transactions

&nbsp;   North     ₹4,50,000     29.13%      25

&nbsp;   South     ₹3,80,000     24.60%      22

&nbsp;   ...



&nbsp;   (continue with all sections...)

&nbsp;   """

Evaluation:



. V All 8 sections present (8 points)

. V Proper formatting and alignment (3 points)

. V Accurate calculations (4 points)



Q:6



Part 5: Main Application



Task 5.1: Create Main Script



In main. py , create the main execution flow:

def main():

&nbsp;   """

&nbsp;   Main execution function



&nbsp;   Workflow:

&nbsp;   1. Print welcome message

&nbsp;   2. Read sales data file (handle encoding)

&nbsp;   3. Parse and clean transactions

&nbsp;   4. Display filter options to user

&nbsp;      - Show available regions

&nbsp;      - Show transaction amount range

&nbsp;      - Ask if user wants to filter (y/n)

&nbsp;   5. If yes, ask for filter criteria and apply

&nbsp;   6. Validate transactions

&nbsp;   7. Display validation summary

&nbsp;   8. Perform all data analyses (call all functions from Part 2)

&nbsp;   9. Fetch products from API

&nbsp;   10. Enrich sales data with API info

&nbsp;   11. Save enriched data to file

&nbsp;   12. Generate comprehensive report

&nbsp;   13. Print success message with file locations



&nbsp;   Error Handling:

&nbsp;   - Wrap entire process in try-except

&nbsp;   - Display user-friendly error messages

&nbsp;   - Don't let program crash on errors



&nbsp;   Expected Console Output:

&nbsp;   ========================================

&nbsp;   SALES ANALYTICS SYSTEM

&nbsp;   ========================================



&nbsp;   \[1/10] Reading sales data...

&nbsp;   ✓ Successfully read 95 transactions



&nbsp;   \[2/10] Parsing and cleaning data...

&nbsp;   ✓ Parsed 95 records



&nbsp;   \[3/10] Filter Options Available:

&nbsp;   Regions: North, South, East, West

&nbsp;   Amount Range: ₹500 - ₹90,000



&nbsp;   Do you want to filter data? (y/n): n



&nbsp;   \[4/10] Validating transactions...

&nbsp;   ✓ Valid: 92 | Invalid: 3



&nbsp;   \[5/10] Analyzing sales data...

&nbsp;   ✓ Analysis complete



&nbsp;   \[6/10] Fetching product data from API...

&nbsp;   ✓ Fetched 30 products



&nbsp;   \[7/10] Enriching sales data...

&nbsp;   ✓ Enriched 85/92 transactions (92.4%)



&nbsp;   \[8/10] Saving enriched data...

&nbsp;   ✓ Saved to: data/enriched\_sales\_data.txt



&nbsp;   \[9/10] Generating report...

&nbsp;   ✓ Report saved to: output/sales\_report.txt



&nbsp;   \[10/10] Process Complete!

&nbsp;   ========================================

&nbsp;   """



if \_name\_ == "\_main\_":

&nbsp;   main()

Evaluation:



. V Complete workflow executes (4 points)

. V User interaction for filters (2 points)

. V Proper error handling (2 points)

. V Console output formatting (2 points)



Q:7	

Marking Scheme	

Total Points: 100	

Section	Points	Details

Part 1: File Handling \& Preprocessing	30	

\- Read with encoding handling	10	UTF-8/encoding issues

\- Parse and clean data	15	Handle commas, data types

&nbsp;	5	

\- Validation and filtering		Validation rules, filter display

Part 2: Data Processing	25	

\- Sales summary functions	15	All calculations correct

\- Date-based anallysis		Daily trend, peak day

\- Product performance	3	Low performers

Part 3: API Integration	20	

\- Fetch products	5	API calls work

\- Product mapping	2	Correct structure

\- Enrich and save data	10	Enrichment logic, file output

\- API understanding	3	Correct API usage

Part 4: Report Generation	15	

\- Report content	8	All 8 sections

\- Formatting	3	Professional look

\- Accuracy	4	Calculations correct

Part 5: Main Application	10	

\- Complete workflow	6	All steps execute

\- User interaction	2	Filter options

\- Error handling	2	Try-except blocks

Total Possible: 100 points		



Submission Guidelines



1\. Create a public GitHub repository named sales-analytics-system

2\. Push all your code with proper folder structure as specified

3\. Submit only the root repository URL: https://github.com/your-username/sales-analytics-system

4\. Do NOT submit links to specific files, folders, or branches

5\. Ensure repository remains public and accessible until grades are released



No other submission method will be accepted.



Pre-Submission Checklist



Repository is public and named correctly

All required files present in correct folders

sales\_data.txt is in data/ folder

README.md has setup and run instructions

requirements.txt includes requests library

Code runs without errors from start to finish

enriched\_sales\_data.txt is generated

sales\_report.txt is generated with all sections

At least 10 meaningful git commits

No hardcoded file paths

