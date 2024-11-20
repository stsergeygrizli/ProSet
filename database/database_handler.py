from config.settings import get_mongo_client, DATABASE_NAME, ALL_PRODUCTS_COLLECTION, VENDORS_COLLECTION


class DatabaseHandler:
    def __init__(self):
        # Initialize the MongoDB client and set the database
        self.client = get_mongo_client()
        if not self.client:
            raise Exception("Could not connect to MongoDB. Check your connection settings.")
        self.db = self.client[DATABASE_NAME]

    def get_collection(self, collection_name):
        """
        Return a collection object.
        :param collection_name: Name of the collection.
        :return: MongoDB collection object.
        """
        return self.db[collection_name]

    # -----------------------
    # Product-specific methods
    # -----------------------

    def insert_product(self, product_data):
        """
        Insert or update a product document in the all_products collection.
        """
        collection = self.get_collection(ALL_PRODUCTS_COLLECTION)

        if "sku" not in product_data or "vendor" not in product_data:
            raise ValueError("Both 'sku' and 'vendor' fields are required.")

        result = collection.update_one(
            {"sku": product_data["sku"]},  # Match by SKU
            {"$set": product_data},        # Set new data
            upsert=True                    # Insert if not found
        )
        print(f"Insert/Update result: {result.raw_result}")
        return result

    def fetch_product_by_sku(self, sku):
        """
        Fetch a product document by SKU.
        """
        collection = self.get_collection(ALL_PRODUCTS_COLLECTION)
        return collection.find_one({"sku": sku})

    def fetch_products_by_vendor(self, vendor_name):
        """
        Fetch all products associated with a specific vendor.
        """
        collection = self.get_collection(ALL_PRODUCTS_COLLECTION)
        return list(collection.find({"vendor.vendor_name": vendor_name}))

    def update_product_field(self, sku, field_name, value):
        """
        Update a specific field for a product by SKU.
        """
        collection = self.get_collection(ALL_PRODUCTS_COLLECTION)
        result = collection.update_one(
            {"sku": sku},
            {"$set": {field_name: value}}
        )
        print(f"Field '{field_name}' updated for SKU '{sku}'. Result: {result.raw_result}")
        return result

    def delete_product(self, sku):
        """
        Delete a product document by SKU.
        """
        collection = self.get_collection(ALL_PRODUCTS_COLLECTION)
        result = collection.delete_one({"sku": sku})
        print(f"Product with SKU '{sku}' deleted. Result: {result.raw_result}")
        return result

    # ----------------------
    # Vendor-specific methods
    # ----------------------

    def get_all_vendors(self):
        """
        Retrieve all vendors from the vendors collection.
        """
        collection = self.get_collection(VENDORS_COLLECTION)
        return list(collection.find())

    def get_vendor_by_name(self, name):
        """
        Retrieve a single vendor by name.
        """
        collection = self.get_collection(VENDORS_COLLECTION)
        return collection.find_one({"name": name})

    def create_or_update_vendor(self, vendor_data):
        """
        Create or update a vendor document in the vendors collection.
        """
        collection = self.get_collection(VENDORS_COLLECTION)

        if "name" not in vendor_data or not vendor_data["name"]:
            raise ValueError("Vendor 'name' is required.")

        result = collection.update_one(
            {"name": vendor_data["name"]},  # Match by vendor name
            {"$set": vendor_data},          # Update the document
            upsert=True                     # Insert if not found
        )
        print(f"Vendor Insert/Update result: {result.raw_result}")
        return result

    def delete_vendor(self, name):
        """
        Delete a vendor by name from the vendors collection.
        """
        collection = self.get_collection(VENDORS_COLLECTION)
        result = collection.delete_one({"name": name})
        print(f"Vendor '{name}' deleted. Result: {result.raw_result}")
        return result
