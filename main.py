# main.py

from utils.file_handler import read_sales_data
from utils.data_processor import (
    parse_transactions, validate_and_filter,
    calculate_total_revenue, region_wise_sales,
    top_selling_products, customer_analysis,
    daily_sales_trend, find_peak_sales_day,
    low_performing_products, generate_sales_report
)
from utils.api_handler import fetch_all_products, create_product_mapping, enrich_sales_data


def main():
    try:
        print("=" * 40)
        print("SALES ANALYTICS SYSTEM")
        print("=" * 40)

        # 1 Read sales data
        print("\n[1/10] Reading sales data...")
        raw_lines = read_sales_data("data/sales_data.txt")
        print(f"✓ Successfully read {len(raw_lines)} transactions")

        # 2 Parse and clean
        print("\n[2/10] Parsing and cleaning data...")
        transactions = parse_transactions(raw_lines)
        print(f"✓ Parsed {len(transactions)} records")

        # 3 Filter options
        print("\n[3/10] Filter Options Available:")
        choice = input("Do you want to filter data? (y/n): ").strip().lower()

        region = None
        min_amount = None
        max_amount = None

        if choice == "y":
            region = input("Enter region name (or press Enter to skip): ").strip()
            if region == "":
                region = None

            min_input = input("Enter minimum amount (or press Enter to skip): ").strip()
            if min_input != "":
                min_amount = float(min_input)

            max_input = input("Enter maximum amount (or press Enter to skip): ").strip()
            if max_input != "":
                max_amount = float(max_input)

        # 4 Validate + filter
        print("\n[4/10] Validating transactions...")
        valid_transactions, invalid_count, summary = validate_and_filter(
            transactions, region=region, min_amount=min_amount, max_amount=max_amount
        )
        print(f"✓ Valid: {len(valid_transactions)} | Invalid: {invalid_count}")

        # 5 Analysis
        print("\n[5/10] Analyzing sales data...")
        calculate_total_revenue(valid_transactions)
        region_wise_sales(valid_transactions)
        top_selling_products(valid_transactions)
        customer_analysis(valid_transactions)
        daily_sales_trend(valid_transactions)
        find_peak_sales_day(valid_transactions)
        low_performing_products(valid_transactions)
        print("✓ Analysis complete")

        # 6 API fetch
        print("\n[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        product_mapping = create_product_mapping(api_products)

        # 7 Enrich
        print("\n[7/10] Enriching sales data...")
        enriched_transactions = enrich_sales_data(valid_transactions, product_mapping)

        enriched_count = sum(1 for t in enriched_transactions if t.get("API_Match"))
        rate = (enriched_count / len(enriched_transactions)) * 100 if enriched_transactions else 0
        print(f"✓ Enriched {enriched_count}/{len(enriched_transactions)} transactions ({rate:.1f}%)")

        # 8 Save is already done inside enrich_sales_data()

        # 9 Report
        print("\n[9/10] Generating report...")
        generate_sales_report(valid_transactions, enriched_transactions)

        # 10 Done
        print("\n[10/10] Process Complete!")
        print("=" * 40)
        print("✅ Output Files Created:")
        print("- data/enriched_sales_data.txt")
        print("- output/sales_report.txt")
        print("=" * 40)

    except Exception as e:
        print("\n❌ Something went wrong but program did not crash.")
        print("Error:", e)


if __name__ == "__main__":
    main()
