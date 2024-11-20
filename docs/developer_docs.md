# Developer Documentation for ProSet

## Project Folder Structure

ProSet/ 
├── assets/ # Static assets (icons, images, etc.) 
├── config/ # Configuration files 
│ ├── init.py 
│ └── settings.py # MongoDB connection settings 
├── database/ # Database-related code 
│ ├── init.py 
│ └── database_handler.py # Handles CRUD operations for the MongoDB database 
├── docs/ # Documentation files 
│ ├── change_log.md # Tracks project changes 
│ ├── developer_docs.md # Documentation for developers 
│ └── user_training.md # Instructions for users 
├── gui/ # GUI-related code 
│ ├── init.py 
│ └── product_form.py # Product management form logic 
├── raw_data/ # Raw data processing 
│ ├── init.py 
│ └── spreadsheet_handler.py # Spreadsheet loading and processing 
├── utils/ # Utility functions 
│ ├── init.py 
│ └── validators.py # Validation logic for product data 
├── main.py # Entry point for the application 
└── requirements.txt # Project dependencies


---

## Database Schema Validator

### MongoDB Collection: `all_products`

This collection stores product data. The schema validator ensures data consistency. Below is the current validator:

```json
{
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
                  ...
                ],
                "description": "Name of the dimension."
              },
              "unit": {
                "bsonType": "string",
                "enum": ["in", "ft", "yd", "mm", "cm", "m", "NA", "UN"],
                "description": "Unit of measurement or special value 'NA'/'UN'."
              },
              "exact": {
                "oneOf": [
                  { "bsonType": "double" },
                  { "enum": ["NA", "UN"] }
                ],
                "description": "Exact dimension value, or 'NA'/'UN'."
              }
            }
          }
        }
      }
    }
  }
}
```
## Updating the Database Validator

To update the MongoDB validator for the `all_products` collection, use the `update_validator.py` script in the `utils` folder.

### Steps:
1. Ensure you have access to the MongoDB database.
2. Run the script: python utils/update_validator.py

