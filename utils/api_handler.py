import requests


def fetch_all_products():
    """
    Fetches all products from DummyJSON API.

    Requirements:
    - Fetch all available products (use limit=100)
    - Handle connection errors with try-except
    - Return empty list if API fails
    - Print status message (success/failure)
    """
    url = "https://dummyjson.com/products?limit=100"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        products = data.get("products", [])

        print(f"✅ API Success: fetched {len(products)} products")
        return products

    except requests.RequestException as e:
        print(f"❌ API Error: {e}")
        return []


def create_product_mapping(api_products: list[dict]) -> dict:
    """
    Creates a mapping of product IDs to product info.

    Returns:
    {
        1: {'title': 'iPhone 9', 'category': 'smartphones', 'brand': 'Apple', 'rating': 4.69},
        ...
    }
    """
    mapping = {}

    for p in api_products:
        pid = p.get("id")
        if pid is None:
            continue

        mapping[pid] = {
            "title": p.get("title"),
            "category": p.get("category"),
            "brand": p.get("brand"),
            "rating": p.get("rating")
        }

    return mapping


def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    """
    Saves enriched transactions back to a file in pipe-delimited format.
    """
    header = [
        "TransactionID", "Date", "ProductID", "ProductName", "Quantity", "UnitPrice",
        "CustomerID", "Region", "API_Category", "API_Brand", "API_Rating", "API_Match"
    ]

    with open(filename, "w", encoding="utf-8") as file:
        file.write("|".join(header) + "\n")

        for t in enriched_transactions:
            row = [
                str(t.get("TransactionID", "")),
                str(t.get("Date", "")),
                str(t.get("ProductID", "")),
                str(t.get("ProductName", "")),
                str(t.get("Quantity", "")),
                str(t.get("UnitPrice", "")),
                str(t.get("CustomerID", "")),
                str(t.get("Region", "")),
                str(t.get("API_Category", "")) if t.get("API_Category") is not None else "",
                str(t.get("API_Brand", "")) if t.get("API_Brand") is not None else "",
                str(t.get("API_Rating", "")) if t.get("API_Rating") is not None else "",
                str(t.get("API_Match", False))
            ]
            file.write("|".join(row) + "\n")

    print(f"✅ Enriched data saved to: {filename}")


def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information.

    Enrichment Logic:
    - Extract numeric ID from ProductID (P101 → 101)
    - DummyJSON API product IDs are 1 to 100
    - Our dataset has IDs like 101+
      so we normalize using modulo to map into 1–100 range.

    Returns: list of enriched transactions
    Also saves output to: data/enriched_sales_data.txt
    """
    enriched = []

    for t in transactions:
        new_t = dict(t)  # copy original transaction

        try:
            # Extract numeric part from ProductID
            raw_id = int(t["ProductID"].replace("P", ""))

            # Normalize to range 1–100
            numeric_id = raw_id % 100
            if numeric_id == 0:
                numeric_id = 100

            if numeric_id in product_mapping:
                info = product_mapping[numeric_id]
                new_t["API_Category"] = info.get("category")
                new_t["API_Brand"] = info.get("brand")
                new_t["API_Rating"] = info.get("rating")
                new_t["API_Match"] = True
            else:
                new_t["API_Category"] = None
                new_t["API_Brand"] = None
                new_t["API_Rating"] = None
                new_t["API_Match"] = False

        except Exception:
            # If anything fails, keep safe default values
            new_t["API_Category"] = None
            new_t["API_Brand"] = None
            new_t["API_Rating"] = None
            new_t["API_Match"] = False

        enriched.append(new_t)

    # Save to file
    save_enriched_data(enriched)
    return enriched
