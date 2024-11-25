import os
import random
import string
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, QFileDialog,
    QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout
)
from PyQt5.QtCore import Qt
from database.database_handler import DatabaseHandler
import openpyxl
from utils.validators import validate_vendor_name


class SkuManagementWindow(QDialog):
    """Window for managing SKUs for a given vendor."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manage SKUs")
        self.resize(900, 600)

        # Initialize database handler
        self.db_handler = DatabaseHandler()

        # Main layout
        layout = QVBoxLayout()

        # Vendor selection
        layout.addWidget(QLabel("Select Vendor:"))
        self.vendor_selector = QComboBox()
        self.load_existing_vendors()
        layout.addWidget(self.vendor_selector)

        # Buttons for SKU operations
        button_layout = QHBoxLayout()
        self.export_button = QPushButton("Export SKUs")
        self.export_button.clicked.connect(self.export_skus)
        self.import_button = QPushButton("Import SKUs")
        self.import_button.clicked.connect(self.import_skus)
        self.generate_button = QPushButton("Generate SKUs")
        self.generate_button.clicked.connect(self.generate_skus)
        button_layout.addWidget(self.export_button)
        button_layout.addWidget(self.import_button)
        button_layout.addWidget(self.generate_button)
        layout.addLayout(button_layout)

        # SKU Table
        self.sku_table = QTableWidget()
        self.sku_table.setColumnCount(4)
        self.sku_table.setHorizontalHeaderLabels(["SKU", "Status", "Old SKU", "Report"])
        layout.addWidget(self.sku_table)

        self.setLayout(layout)

    def load_existing_vendors(self):
        """Load vendor names into the dropdown."""
        self.vendor_selector.clear()
        vendors = self.db_handler.get_collection("vendors").find()
        for vendor in vendors:
            self.vendor_selector.addItem(vendor["name"])

    def export_skus(self):
        """Export SKUs for the selected vendor to a spreadsheet."""
        vendor_name = self.vendor_selector.currentText()
        if not vendor_name:
            QMessageBox.warning(self, "Error", "Please select a vendor.")
            return

        # Fetch products for the vendor
        products = self.db_handler.get_collection("all_products").find({"vendor.vendor_name": vendor_name})

        # Create a spreadsheet
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Excel Files (*.xlsx)")
        if not file_path:
            return

        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.append(["vendor_name", "sku", "sku_type", "sku_status", "old_sku", "report"])  # Headers

        for product in products:
            sku_info = product.get("sku_info", {})
            sheet.append([
                vendor_name,
                sku_info.get("sku", ""),
                sku_info.get("sku_type", ""),
                sku_info.get("sku_status", ""),
                sku_info.get("old_sku", ""),
                ""  # Empty report column
            ])

        workbook.save(file_path)
        QMessageBox.information(self, "Success", f"SKUs exported to {file_path}")

    def import_skus(self):
        """Import SKUs from a spreadsheet and update the database."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Excel Files (*.xlsx)")
        if not file_path:
            return

        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active

        for row_idx, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):  # Skip the header row
            print(f"Row {row_idx}: {row}")  # Debugging

            vendor_name, sku, sku_type, sku_status, old_sku, report = row

            # Replace None with "NA" explicitly
            old_sku = old_sku if old_sku is not None else "NA"

            try:
                validate_vendor_name(vendor_name)

                product_data = {
                    "sku_info": {
                        "sku": sku,
                        "sku_type": sku_type,
                        "sku_status": sku_status,
                        "old_sku": old_sku
                    },
                    "vendor": {"vendor_name": vendor_name}
                }

                collection = self.db_handler.get_collection("all_products")
                result = collection.update_one(
                    {"sku_info.sku": sku, "vendor.vendor_name": vendor_name},
                    {"$set": product_data},
                    upsert=True  # Insert if not found
                )

                if result.upserted_id:
                    report = "Inserted new product"
                elif result.modified_count > 0:
                    report = "Updated existing product"
                else:
                    report = "No changes made"

            except ValueError as e:
                print(f"Validation error: {e}")
                report = f"Validation error: {e}"

            except Exception as e:
                print(f"Unexpected error: {e}")
                report = f"Unexpected error: {e}"

            # Write the report back to the spreadsheet
            sheet.cell(row=row_idx, column=6).value = report

        workbook.save(file_path)
        QMessageBox.information(self, "Success", "SKUs imported and updated successfully.")

    def generate_skus(self):
        """Placeholder method for generating SKUs."""
        print("Generate SKUs button clicked. Functionality not implemented yet.")

