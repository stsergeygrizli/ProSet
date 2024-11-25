import sys
from PyQt5.QtWidgets import QApplication
from gui.product_form import ProductForm
from database.database_handler import DatabaseHandler
from utils.validators import validate_product_data


def test_database_operations():
    """
    Test function to validate and insert a sample product into the database.
    """
    db_handler = DatabaseHandler()

    # Sample product data with updated schema
    sample_product = {
        "sku_info": {
            "sku": "TEST123",
            "sku_type": "generated",
            "sku_status": "current",
            "old_sku": "NA"  # No previous SKU for this example
        },
        "vendor": {"vendor_name": "Vendor A"},
        "sizes": {
            "dimensions": [
                {
                    "name": "width",
                    "unit": "cm",
                    "exact": 10.0
                },
                {
                    "name": "length",
                    "unit": "cm",
                    "exact": "NA"
                }
            ]
        }
    }

    # Validate product data
    try:
        validate_product_data(sample_product)  # Ensure the validation function is updated for the new schema
        print("Validation passed.")
    except ValueError as e:
        print(f"Validation error: {e}")
        return

    # Insert product
    db_handler.insert_product(sample_product)

    # Fetch and print the product
    product = db_handler.fetch_product_by_sku("TEST123")
    print("Fetched product:", product)


def main():
    """
    Entry point for the ProSet application.
    """
    # Uncomment the next line to test database operations during development
    # test_database_operations()

    # Start the GUI
    app = QApplication(sys.argv)
    main_window = ProductForm()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
