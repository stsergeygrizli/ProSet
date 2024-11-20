def validate_product_data(product_data):
    """
    Validate product data based on the schema requirements.
    """
    if not isinstance(product_data, dict):
        raise ValueError("Product data must be a dictionary.")

    # Required fields
    if "sku" not in product_data or not product_data["sku"]:
        raise ValueError("'sku' is required and must not be empty.")
    if "vendor" not in product_data or not isinstance(product_data["vendor"], dict):
        raise ValueError("'vendor' is required and must be an object with 'vendor_name'.")

    # Sizes validation
    if "sizes" in product_data:
        if "dimensions" in product_data["sizes"]:
            for dimension in product_data["sizes"]["dimensions"]:
                if not isinstance(dimension, dict):
                    raise ValueError("Each dimension must be an object.")
                if "name" not in dimension or "unit" not in dimension:
                    raise ValueError("Each dimension must have 'name' and 'unit' fields.")
    return True
