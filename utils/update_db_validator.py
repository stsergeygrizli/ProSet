from pymongo import MongoClient
from config.settings import MONGO_URI, DATABASE_NAME, COLLECTION_NAME

def update_validator():
    """
    Updates the validator for the 'all_products' collection.
    """
    # MongoDB client connection
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    # Define the updated validator
    validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["sku", "vendor"],
            "properties": {
                "sku": {
                    "bsonType": "string",
                    "description": "Unique SKU for the product."
                },
                "vendor": {
                    "bsonType": "object",
                    "description": "Vendor details.",
                    "properties": {
                        "vendor_name": {
                            "bsonType": "string",
                            "description": "Name of the vendor."
                        }
                    }
                },
                "sizes": {
                    "bsonType": "object",
                    "description": "All size-related information for the product.",
                    "properties": {
                        "dimensions": {
                            "bsonType": "array",
                            "description": "List of dimensions for a single piece.",
                            "items": {
                                "bsonType": "object",
                                "properties": {
                                    "name": {
                                        "bsonType": "string",
                                        "enum": [
                                            "width", "length", "thickness", "diagonal", "radius",
                                            "diameter", "long_parallel_side", "short_parallel_side",
                                            "left_side", "right_side", "long_side", "short_side",
                                            "height", "bottom_side", "long_diagonal", "short_diagonal",
                                            "side", "long_diameter", "short_diameter",
                                            "opposite_sides_distance", "opposite_vertices_distance",
                                            "long_opposing_sides", "short_opposing_vertices",
                                            "short_opposing_sides", "long_opposing_vertices",
                                            "dimension_a", "dimension_b", "dimension_c",
                                            "dimension_d", "dimension_e", "dimension_f",
                                            "dimension_g", "dimension_h", "back_layer_thickness",
                                            "core_layer_thickness", "wear_layer_thickness", "short_return_length",
                                            "long_return_length", "return_length", "width_a", "width_b"
                                        ],
                                        "description": "Name of the dimension."
                                    },
                                    "unit": {
                                        "bsonType": "string",
                                        "enum": ["in", "ft", "yd", "mm", "cm", "m", "NA", "UN"],
                                        "description": "Unit of measurement for the dimension, or 'NA'/'UN' for unknown or not applicable."
                                    },
                                    "exact": {
                                        "oneOf": [
                                            {"bsonType": "double"},
                                            {"enum": ["NA", "UN"]}
                                        ],
                                        "description": "Exact dimension value, or special values 'NA'/'UN'."
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    # Update the validator
    try:
        result = db.command({
            "collMod": COLLECTION_NAME,
            "validator": validator,
            "validationAction": "error",  # Reject invalid documents
            "validationLevel": "strict"  # Enforce validation on all inserts and updates
        })
        print(f"Validator updated successfully: {result}")
    except Exception as e:
        print(f"Failed to update validator: {e}")


if __name__ == "__main__":
    update_validator()
