from database.database_handler import DatabaseHandler

def validate_product_data(product_data):
    """
    Validate product data based on the schema requirements.
    """
    if not isinstance(product_data, dict):
        raise ValueError("Product data must be a dictionary.")

    # Validate required fields
    if "sku_info" not in product_data or not isinstance(product_data["sku_info"], dict):
        raise ValueError("'sku_info' is required and must be an object.")
    if "vendor" not in product_data or not isinstance(product_data["vendor"], dict):
        raise ValueError("'vendor' is required and must be an object with 'vendor_name'.")

    # Validate `sku_info` structure
    sku_info = product_data["sku_info"]
    if "sku" not in sku_info or not isinstance(sku_info["sku"], str) or not sku_info["sku"].strip():
        raise ValueError("'sku_info.sku' is required and must be a non-empty string.")
    if "sku_type" not in sku_info or sku_info["sku_type"] not in ["generated", "vendor"]:
        raise ValueError("'sku_info.sku_type' must be either 'generated' or 'vendor'.")
    if "sku_status" not in sku_info or sku_info["sku_status"] not in ["current", "discontinued"]:
        raise ValueError("'sku_info.sku_status' must be either 'current' or 'discontinued'.")
    if "old_sku" in sku_info and sku_info["old_sku"] is not None and not isinstance(sku_info["old_sku"], str):
        raise ValueError("'sku_info.old_sku' must be a string or None if provided.")

    # Validate `vendor`
    vendor = product_data["vendor"]
    if "vendor_name" not in vendor or not isinstance(vendor["vendor_name"], str) or not vendor["vendor_name"].strip():
        raise ValueError("'vendor.vendor_name' is required and must be a non-empty string.")

    # Validate `sizes`
    if "sizes" in product_data:
        if "dimensions" in product_data["sizes"]:
            dimensions = product_data["sizes"]["dimensions"]
            if not isinstance(dimensions, list):
                raise ValueError("'sizes.dimensions' must be a list.")
            for dimension in dimensions:
                if not isinstance(dimension, dict):
                    raise ValueError("Each dimension in 'sizes.dimensions' must be an object.")
                if "name" not in dimension or dimension["name"] not in [
                    "width", "length", "thickness", "diagonal", "radius", "diameter", "long_parallel_side",
                    "short_parallel_side", "left_side", "right_side", "long_side", "short_side", "height",
                    "bottom_side", "long_diagonal", "short_diagonal", "side", "long_diameter", "short_diameter",
                    "opposite_sides_distance", "opposite_vertices_distance", "long_opposing_sides",
                    "short_opposing_vertices", "short_opposing_sides", "long_opposing_vertices", "dimension_a",
                    "dimension_b", "dimension_c", "dimension_d", "dimension_e", "dimension_f", "dimension_g",
                    "dimension_h", "back_layer_thickness", "core_layer_thickness", "wear_layer_thickness",
                    "short_return_length", "long_return_length", "return_length", "width_a", "width_b"
                ]:
                    raise ValueError("Each dimension must have a valid 'name'.")
                if "unit" not in dimension or dimension["unit"] not in ["in", "ft", "yd", "mm", "cm", "m", "NA", "UN"]:
                    raise ValueError("Each dimension must have a valid 'unit'.")
                if "exact" in dimension and not (
                    isinstance(dimension["exact"], (float, int)) or dimension["exact"] in ["NA", "UN"]
                ):
                    raise ValueError("Each dimension's 'exact' field must be a number or 'NA'/'UN'.")

    return True

def validate_vendor_name(vendor_name):
    """
    Validate that a given vendor_name exists in the 'vendors' collection.
    :param vendor_name: Name of the vendor to validate.
    :raises ValueError: If the vendor_name does not exist.
    :return: True if the vendor_name is valid.
    """
    if not vendor_name or not isinstance(vendor_name, str):
        raise ValueError("Vendor name must be a non-empty string.")

    db_handler = DatabaseHandler()
    vendor = db_handler.get_vendor_by_name(vendor_name)
    if not vendor:
        raise ValueError(f"Vendor '{vendor_name}' does not exist in the database.")

    return True
