from datetime import datetime


# ============================================================
# PART 1.2: PARSE AND CLEAN DATA
# ============================================================

def parse_transactions(raw_lines: list[str]) -> list[dict]:
    """
    Parses raw lines into clean list of dictionaries.

    Requirements:
    - Split by pipe delimiter '|'
    - Remove commas from ProductName
    - Remove commas from numeric fields and convert types
    - Convert Quantity to int
    - Convert UnitPrice to float
    - Skip rows with incorrect number of fields
    """

    transactions = []

    for line in raw_lines:
        parts = line.split("|")

        # Skip rows with incorrect number of fields
        if len(parts) != 8:
            continue

        transaction_id, date, product_id, product_name, quantity, unit_price, customer_id, region = parts

        # Clean ProductName (remove commas)
        product_name = product_name.replace(",", "")

        # Remove commas from numeric values
        quantity = quantity.replace(",", "")
        unit_price = unit_price.replace(",", "")

        # Convert to proper types
        try:
            quantity = int(quantity)
            unit_price = float(unit_price)
        except ValueError:
            # Skip invalid numeric values
            continue

        transactions.append({
            "TransactionID": transaction_id.strip(),
            "Date": date.strip(),
            "ProductID": product_id.strip(),
            "ProductName": product_name.strip(),
            "Quantity": quantity,
            "UnitPrice": unit_price,
            "CustomerID": customer_id.strip(),
            "Region": region.strip()
        })

    return transactions


# ============================================================
# PART 1.3: VALIDATION AND FILTERING
# ============================================================

def validate_and_filter(transactions: list[dict], region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters.

    Parameters:
    - transactions: list of transaction dictionaries
    - region: filter by specific region (optional)
    - min_amount: minimum transaction amount (Quantity * UnitPrice) (optional)
    - max_amount: maximum transaction amount (optional)

    Returns: tuple (valid_transactions, invalid_count, filter_summary)
    """

    total_input = len(transactions)
    invalid_count = 0
    valid_transactions = []

    # Display available regions to user before filtering
    available_regions = sorted(set(t.get("Region", "") for t in transactions if t.get("Region", "").strip() != ""))
    print("\n📌 Available Regions:", ", ".join(available_regions) if available_regions else "None")

    # Display transaction amount range
    amounts = []
    for t in transactions:
        try:
            amounts.append(t["Quantity"] * t["UnitPrice"])
        except Exception:
            continue

    if amounts:
        print(f"📌 Transaction Amount Range: ₹{min(amounts):,.0f} - ₹{max(amounts):,.0f}")
    else:
        print("📌 Transaction Amount Range: Not available")

    # Validation rules
    for t in transactions:
        try:
            tid = t["TransactionID"]
            pid = t["ProductID"]
            cid = t["CustomerID"]
            reg = t["Region"]
            qty = t["Quantity"]
            price = t["UnitPrice"]

            # Required fields present?
            if tid.strip() == "" or pid.strip() == "" or cid.strip() == "" or reg.strip() == "":
                invalid_count += 1
                continue

            # ID formats
            if not tid.startswith("T"):
                invalid_count += 1
                continue
            if not pid.startswith("P"):
                invalid_count += 1
                continue
            if not cid.startswith("C"):
                invalid_count += 1
                continue

            # Quantity and price rules
            if qty <= 0:
                invalid_count += 1
                continue
            if price <= 0:
                invalid_count += 1
                continue

            valid_transactions.append(t)

        except Exception:
            invalid_count += 1

    # Filtering
    filtered_by_region = 0
    filtered_by_amount = 0
    filtered_transactions = valid_transactions

    if region:
        before = len(filtered_transactions)
        filtered_transactions = [t for t in filtered_transactions if t["Region"].lower() == region.lower()]
        filtered_by_region = before - len(filtered_transactions)
        print(f"✅ After region filter ({region}): {len(filtered_transactions)} records")

    if min_amount is not None:
        before = len(filtered_transactions)
        filtered_transactions = [t for t in filtered_transactions if (t["Quantity"] * t["UnitPrice"]) >= min_amount]
        filtered_by_amount += before - len(filtered_transactions)

    if max_amount is not None:
        before = len(filtered_transactions)
        filtered_transactions = [t for t in filtered_transactions if (t["Quantity"] * t["UnitPrice"]) <= max_amount]
        filtered_by_amount += before - len(filtered_transactions)

    if min_amount is not None or max_amount is not None:
        print(f"✅ After amount filter: {len(filtered_transactions)} records")

    summary = {
        "total_input": total_input,
        "invalid": invalid_count,
        "filtered_by_region": filtered_by_region,
        "filtered_by_amount": filtered_by_amount,
        "final_count": len(filtered_transactions)
    }

    return filtered_transactions, invalid_count, summary


# ============================================================
# PART 2.1: SALES SUMMARY CALCULATOR
# ============================================================

def calculate_total_revenue(transactions: list[dict]) -> float:
    """
    Calculates total revenue from all transactions.
    Returns sum of (Quantity * UnitPrice).
    """
    return sum(t["Quantity"] * t["UnitPrice"] for t in transactions)


def region_wise_sales(transactions: list[dict]) -> dict:
    """
    Analyzes sales by region.

    Returns dictionary:
    {
        'North': {'total_sales': ..., 'transaction_count': ..., 'percentage': ...},
        ...
    }
    """
    total_revenue = calculate_total_revenue(transactions)
    region_data = {}

    for t in transactions:
        reg = t["Region"]
        amount = t["Quantity"] * t["UnitPrice"]

        if reg not in region_data:
            region_data[reg] = {"total_sales": 0.0, "transaction_count": 0}

        region_data[reg]["total_sales"] += amount
        region_data[reg]["transaction_count"] += 1

    # Percentages
    for reg in region_data:
        region_data[reg]["percentage"] = (region_data[reg]["total_sales"] / total_revenue * 100) if total_revenue else 0

    # Sort by total_sales descending
    sorted_regions = dict(sorted(region_data.items(), key=lambda x: x[1]["total_sales"], reverse=True))
    return sorted_regions


def top_selling_products(transactions: list[dict], n=5):
    """
    Finds top n products by total quantity sold.

    Returns list of tuples:
    [
        ('Laptop', 45, 2250000.0),
        ...
    ]
    """
    product_data = {}

    for t in transactions:
        name = t["ProductName"]
        qty = t["Quantity"]
        revenue = qty * t["UnitPrice"]

        if name not in product_data:
            product_data[name] = {"qty": 0, "rev": 0.0}

        product_data[name]["qty"] += qty
        product_data[name]["rev"] += revenue

    result = [(name, info["qty"], info["rev"]) for name, info in product_data.items()]
    result.sort(key=lambda x: x[1], reverse=True)

    return result[:n]


def customer_analysis(transactions: list[dict]) -> dict:
    """
    Analyzes customer purchase patterns.

    Returns dictionary:
    {
        'C001': {
            'total_spent': ...,
            'purchase_count': ...,
            'avg_order_value': ...,
            'products_bought': [...]
        },
        ...
    }
    """
    customers = {}

    for t in transactions:
        cid = t["CustomerID"]
        amount = t["Quantity"] * t["UnitPrice"]
        product = t["ProductName"]

        if cid not in customers:
            customers[cid] = {
                "total_spent": 0.0,
                "purchase_count": 0,
                "products_bought": set()
            }

        customers[cid]["total_spent"] += amount
        customers[cid]["purchase_count"] += 1
        customers[cid]["products_bought"].add(product)

    for cid in customers:
        count = customers[cid]["purchase_count"]
        customers[cid]["avg_order_value"] = customers[cid]["total_spent"] / count if count else 0
        customers[cid]["products_bought"] = sorted(list(customers[cid]["products_bought"]))

    # Sort by total_spent descending
    sorted_customers = dict(sorted(customers.items(), key=lambda x: x[1]["total_spent"], reverse=True))
    return sorted_customers


# ============================================================
# PART 2.2: DATE-BASED ANALYSIS
# ============================================================

def daily_sales_trend(transactions: list[dict]) -> dict:
    """
    Analyzes sales trends by date.

    Returns dictionary sorted by date:
    {
        '2024-12-01': {'revenue': ..., 'transaction_count': ..., 'unique_customers': ...},
        ...
    }
    """
    trend = {}

    for t in transactions:
        date = t["Date"]
        amount = t["Quantity"] * t["UnitPrice"]
        cid = t["CustomerID"]

        if date not in trend:
            trend[date] = {"revenue": 0.0, "transaction_count": 0, "customers": set()}

        trend[date]["revenue"] += amount
        trend[date]["transaction_count"] += 1
        trend[date]["customers"].add(cid)

    for date in trend:
        trend[date]["unique_customers"] = len(trend[date]["customers"])
        del trend[date]["customers"]

    return dict(sorted(trend.items()))


def find_peak_sales_day(transactions: list[dict]):
    """
    Identifies the date with highest revenue.

    Returns tuple: (date, revenue, transaction_count)
    """
    trend = daily_sales_trend(transactions)

    best_date = None
    best_revenue = 0
    best_count = 0

    for date, info in trend.items():
        if info["revenue"] > best_revenue:
            best_date = date
            best_revenue = info["revenue"]
            best_count = info["transaction_count"]

    return (best_date, best_revenue, best_count)


# ============================================================
# PART 2.3: PRODUCT PERFORMANCE
# ============================================================

def low_performing_products(transactions: list[dict], threshold=10):
    """
    Identifies products with low sales.

    Returns list of tuples:
    [
        ('Webcam', 4, 12000.0),
        ...
    ]
    """
    product_summary = {}

    for t in transactions:
        name = t["ProductName"]
        qty = t["Quantity"]
        revenue = qty * t["UnitPrice"]

        if name not in product_summary:
            product_summary[name] = {"qty": 0, "rev": 0.0}

        product_summary[name]["qty"] += qty
        product_summary[name]["rev"] += revenue

    low_perf = [(name, info["qty"], info["rev"]) for name, info in product_summary.items() if info["qty"] < threshold]
    low_perf.sort(key=lambda x: x[1])  # sort by quantity ascending
    return low_perf


# ============================================================
# PART 4: REPORT GENERATION
# ============================================================

def generate_sales_report(transactions, enriched_transactions, output_file="output/sales_report.txt"):
    """
    Generates a comprehensive formatted text report
    and writes it to output/sales_report.txt
    """

    total_revenue = calculate_total_revenue(transactions)
    total_transactions = len(transactions)
    avg_order_value = total_revenue / total_transactions if total_transactions else 0

    # Date range
    dates = [t["Date"] for t in transactions]
    date_start = min(dates) if dates else "N/A"
    date_end = max(dates) if dates else "N/A"

    # Region stats
    region_stats = region_wise_sales(transactions)

    # Top products
    top_products = top_selling_products(transactions, n=5)

    # Top customers
    customers = customer_analysis(transactions)
    top_customers = list(customers.items())[:5]

    # Daily trend
    trend = daily_sales_trend(transactions)

    # Best selling day
    peak_date, peak_revenue, peak_txns = find_peak_sales_day(transactions)

    # Low performing products
    low_perf = low_performing_products(transactions)

    # Enrichment summary
    total_enriched = len(enriched_transactions)
    enriched_success = sum(1 for t in enriched_transactions if t.get("API_Match") is True)
    success_rate = (enriched_success / total_enriched * 100) if total_enriched else 0

    # Products that couldn't be enriched (ProductID list)
    failed_products = sorted(set(t["ProductID"] for t in enriched_transactions if not t.get("API_Match")))

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(output_file, "w", encoding="utf-8") as f:
        # 1. HEADER
        f.write("=" * 44 + "\n")
        f.write("          SALES ANALYTICS REPORT\n")
        f.write(f"        Generated: {now}\n")
        f.write(f"        Records Processed: {total_transactions}\n")
        f.write("=" * 44 + "\n\n")

        # 2. OVERALL SUMMARY
        f.write("OVERALL SUMMARY\n")
        f.write("-" * 44 + "\n")
        f.write(f"Total Revenue:        ₹{total_revenue:,.2f}\n")
        f.write(f"Total Transactions:   {total_transactions}\n")
        f.write(f"Average Order Value:  ₹{avg_order_value:,.2f}\n")
        f.write(f"Date Range:           {date_start} to {date_end}\n\n")

        # 3. REGION-WISE PERFORMANCE
        f.write("REGION-WISE PERFORMANCE\n")
        f.write("-" * 44 + "\n")
        f.write(f"{'Region':<10}{'Sales':<16}{'% of Total':<12}{'Transactions':<12}\n")
        for reg, info in region_stats.items():
            f.write(f"{reg:<10}₹{info['total_sales']:,.0f}       {info['percentage']:>6.2f}%      {info['transaction_count']}\n")
        f.write("\n")

        # 4. TOP 5 PRODUCTS
        f.write("TOP 5 PRODUCTS\n")
        f.write("-" * 44 + "\n")
        f.write(f"{'Rank':<6}{'Product Name':<20}{'Qty Sold':<10}{'Revenue':<10}\n")
        for i, (name, qty, rev) in enumerate(top_products, start=1):
            f.write(f"{i:<6}{name:<20}{qty:<10}₹{rev:,.0f}\n")
        f.write("\n")

        # 5. TOP 5 CUSTOMERS
        f.write("TOP 5 CUSTOMERS\n")
        f.write("-" * 44 + "\n")
        f.write(f"{'Rank':<6}{'Customer ID':<12}{'Total Spent':<15}{'Orders':<10}\n")
        for i, (cid, info) in enumerate(top_customers, start=1):
            f.write(f"{i:<6}{cid:<12}₹{info['total_spent']:,.0f}       {info['purchase_count']}\n")
        f.write("\n")

        # 6. DAILY SALES TREND
        f.write("DAILY SALES TREND\n")
        f.write("-" * 44 + "\n")
        f.write(f"{'Date':<12}{'Revenue':<16}{'Txns':<8}{'Unique Customers':<15}\n")
        for date, info in trend.items():
            f.write(f"{date:<12}₹{info['revenue']:,.0f}       {info['transaction_count']:<8}{info['unique_customers']}\n")
        f.write("\n")

        # 7. PRODUCT PERFORMANCE ANALYSIS
        f.write("PRODUCT PERFORMANCE ANALYSIS\n")
        f.write("-" * 44 + "\n")
        f.write(f"Best Selling Day: {peak_date} (₹{peak_revenue:,.0f}, {peak_txns} transactions)\n\n")

        # Low performing products
        if low_perf:
            f.write("Low Performing Products:\n")
            for name, qty, rev in low_perf:
                f.write(f"- {name}: {qty} units, ₹{rev:,.0f}\n")
        else:
            f.write("Low Performing Products: None\n")

        f.write("\nAverage Transaction Value per Region:\n")
        for reg, info in region_stats.items():
            avg_val = info["total_sales"] / info["transaction_count"] if info["transaction_count"] else 0
            f.write(f"- {reg}: ₹{avg_val:,.0f}\n")

        f.write("\n")

        # 8. API ENRICHMENT SUMMARY
        f.write("API ENRICHMENT SUMMARY\n")
        f.write("-" * 44 + "\n")
        f.write(f"Total products enriched: {enriched_success}/{total_enriched}\n")
        f.write(f"Success rate: {success_rate:.2f}%\n\n")

        f.write("Products that couldn't be enriched:\n")
        if failed_products:
            for pid in failed_products:
                f.write(f"- {pid}\n")
        else:
            f.write("- None\n")

    print(f"✅ Report generated successfully: {output_file}")
