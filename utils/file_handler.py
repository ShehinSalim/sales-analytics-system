# utils/file_handler.py

def read_sales_data(filename: str) -> list[str]:
    """
    Reads sales data from a file while handling encoding issues.
    Returns a list of raw transaction lines (strings).
    """

    encodings_to_try = ["utf-8", "latin-1", "cp1252"]

    for encoding in encodings_to_try:
        try:
            with open(filename, "r", encoding=encoding) as file:
                lines = file.readlines()

            # Remove header and empty lines
            cleaned_lines = []
            for i, line in enumerate(lines):
                line = line.strip()

                # Skip header row (first line)
                if i == 0:
                    continue

                # Skip empty lines
                if line == "":
                    continue

                cleaned_lines.append(line)

            print(f"✅ File read successfully using encoding: {encoding}")
            return cleaned_lines

        except UnicodeDecodeError:
            # Try next encoding
            continue

        except FileNotFoundError:
            print(f"❌ Error: File not found -> {filename}")
            return []

    print("❌ Error: Could not read file due to encoding issues.")
    return []
