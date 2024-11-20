from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QHBoxLayout,
    QFormLayout, QScrollArea, QWidget, QMessageBox
)
from database.database_handler import DatabaseHandler


class VendorManagementWindow(QDialog):
    """Window for managing vendor information."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manage Vendors")
        self.resize(800, 600)

        # Initialize database handler
        self.db_handler = DatabaseHandler()

        # Main layout
        layout = QVBoxLayout()

        # Dropdown for vendor selection
        self.vendor_selector = QComboBox()
        self.vendor_selector.addItem("Create New")
        self.load_existing_vendors()
        self.vendor_selector.currentIndexChanged.connect(self.vendor_changed)
        layout.addWidget(self.vendor_selector)

        # Form for vendor information
        self.form_layout = QFormLayout()
        self.name_field = QLineEdit()
        self.full_name_field = QLineEdit()
        self.abbreviation_field = QLineEdit()
        self.headquarters_address_field = QLineEdit()
        self.headquarters_phone_field = QLineEdit()
        self.headquarters_email_field = QLineEdit()

        self.sales_rep_name_field = QLineEdit()
        self.sales_rep_office_phone_field = QLineEdit()
        self.sales_rep_cell_phone_field = QLineEdit()
        self.sales_rep_email1_field = QLineEdit()
        self.sales_rep_email2_field = QLineEdit()

        self.form_layout.addRow("Name:", self.name_field)
        self.form_layout.addRow("Full Name:", self.full_name_field)
        self.form_layout.addRow("Abbreviation:", self.abbreviation_field)
        self.form_layout.addRow("HQ Address:", self.headquarters_address_field)
        self.form_layout.addRow("HQ Phone:", self.headquarters_phone_field)
        self.form_layout.addRow("HQ Email:", self.headquarters_email_field)
        self.form_layout.addRow("Sales Rep Name:", self.sales_rep_name_field)
        self.form_layout.addRow("Sales Rep Office Phone:", self.sales_rep_office_phone_field)
        self.form_layout.addRow("Sales Rep Cell Phone:", self.sales_rep_cell_phone_field)
        self.form_layout.addRow("Sales Rep Email 1:", self.sales_rep_email1_field)
        self.form_layout.addRow("Sales Rep Email 2:", self.sales_rep_email2_field)

        layout.addLayout(self.form_layout)

        # Scrollable section for warehouse locations
        self.warehouse_scroll = QScrollArea()
        self.warehouse_scroll.setWidgetResizable(True)
        self.warehouse_container = QWidget()
        self.warehouse_layout = QVBoxLayout(self.warehouse_container)
        self.warehouse_scroll.setWidget(self.warehouse_container)
        layout.addWidget(QLabel("Warehouses:"))
        layout.addWidget(self.warehouse_scroll)

        # Add/Edit buttons
        self.add_warehouse_button = QPushButton("Add Warehouse")
        self.add_warehouse_button.clicked.connect(self.add_warehouse)
        layout.addWidget(self.add_warehouse_button)

        # Control buttons
        button_layout = QHBoxLayout()
        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(self.toggle_editing)
        self.save_button = QPushButton("Save")
        self.save_button.setEnabled(False)  # Initially disabled
        self.save_button.clicked.connect(self.save_vendor)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel_changes)
        self.delete_button = QPushButton("Delete Vendor")
        self.delete_button.clicked.connect(self.delete_vendor)

        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.delete_button)

        layout.addLayout(button_layout)

        # Set main layout
        self.setLayout(layout)

        # Disable editing by default
        self.set_fields_editable(False)

        # Monitor changes in fields
        for field in [
            self.name_field, self.full_name_field, self.abbreviation_field,
            self.headquarters_address_field, self.headquarters_phone_field, self.headquarters_email_field,
            self.sales_rep_name_field, self.sales_rep_office_phone_field, self.sales_rep_cell_phone_field,
            self.sales_rep_email1_field, self.sales_rep_email2_field
        ]:
            field.textChanged.connect(self.monitor_field_changes)

    def monitor_field_changes(self):
        """Monitor field changes and enable the Save button if there are unsaved changes."""
        # Enable the Save button if any field is modified
        self.save_button.setEnabled(True)

    def load_existing_vendors(self):
        """Load existing vendors into the dropdown."""
        vendors = self.db_handler.get_collection("vendors").find()
        self.vendor_selector.clear()
        self.vendor_selector.addItem("Create New")
        for vendor in vendors:
            self.vendor_selector.addItem(vendor["name"])

    def vendor_changed(self):
        """Load selected vendor's details into fields."""
        if self.vendor_selector.currentText() == "Create New":
            self.clear_fields()
            self.set_fields_editable(True)
        else:
            vendor = self.db_handler.get_collection("vendors").find_one({"name": self.vendor_selector.currentText()})
            self.populate_fields(vendor)
            self.set_fields_editable(False)

    def populate_fields(self, vendor):
        """Populate fields with vendor data."""
        self.name_field.setText(vendor.get("name", ""))
        self.full_name_field.setText(vendor.get("full_name", ""))
        self.abbreviation_field.setText(vendor.get("abbreviation", ""))
        self.headquarters_address_field.setText(vendor.get("headquarters_address", ""))
        self.headquarters_phone_field.setText(vendor.get("headquarters_phone", ""))
        self.headquarters_email_field.setText(vendor.get("headquarters_email", ""))
        self.sales_rep_name_field.setText(vendor.get("sales_rep", {}).get("name", ""))
        self.sales_rep_office_phone_field.setText(vendor.get("sales_rep", {}).get("office_phone", ""))
        self.sales_rep_cell_phone_field.setText(vendor.get("sales_rep", {}).get("cell_phone", ""))
        self.sales_rep_email1_field.setText(vendor.get("sales_rep", {}).get("email1", ""))
        self.sales_rep_email2_field.setText(vendor.get("sales_rep", {}).get("email2", ""))

        self.clear_warehouses()
        for warehouse in vendor.get("warehouses", []):
            self.add_warehouse(
                warehouse.get("name", ""),
                warehouse.get("address", ""),
                warehouse.get("phone", ""),
                warehouse.get("email", "")
            )

    def clear_fields(self):
        """Clear all fields."""
        self.name_field.clear()
        self.full_name_field.clear()
        self.abbreviation_field.clear()
        self.headquarters_address_field.clear()
        self.headquarters_phone_field.clear()
        self.headquarters_email_field.clear()
        self.sales_rep_name_field.clear()
        self.sales_rep_office_phone_field.clear()
        self.sales_rep_cell_phone_field.clear()
        self.sales_rep_email1_field.clear()
        self.sales_rep_email2_field.clear()
        self.clear_warehouses()

    def clear_warehouses(self):
        """Clear all warehouse widgets."""
        while self.warehouse_layout.count():
            widget = self.warehouse_layout.takeAt(0).widget()
            if widget:
                widget.deleteLater()

    def add_warehouse(self, name=None, address=None, phone=None, email=None):
        """Add a warehouse section."""
        name = str(name) if name else ""
        address = str(address) if address else ""
        phone = str(phone) if phone else ""
        email = str(email) if email else ""

        warehouse_widget = QWidget()
        warehouse_layout = QFormLayout()

        name_field = QLineEdit(name)
        name_field.textChanged.connect(self.monitor_field_changes)
        address_field = QLineEdit(address)
        address_field.textChanged.connect(self.monitor_field_changes)
        phone_field = QLineEdit(phone)
        phone_field.textChanged.connect(self.monitor_field_changes)
        email_field = QLineEdit(email)
        email_field.textChanged.connect(self.monitor_field_changes)

        warehouse_layout.addRow("Name:", name_field)
        warehouse_layout.addRow("Address:", address_field)
        warehouse_layout.addRow("Phone:", phone_field)
        warehouse_layout.addRow("Email:", email_field)

        warehouse_widget.setLayout(warehouse_layout)
        self.warehouse_layout.addWidget(warehouse_widget)

    def toggle_editing(self):
        """Enable or disable editing."""
        self.set_fields_editable(True)
        self.save_button.setEnabled(False)  # Save button should remain disabled until changes occur

    def set_fields_editable(self, editable):
        """Set all fields as editable or read-only."""
        self.name_field.setReadOnly(not editable)
        self.full_name_field.setReadOnly(not editable)
        self.abbreviation_field.setReadOnly(not editable)
        self.headquarters_address_field.setReadOnly(not editable)
        self.headquarters_phone_field.setReadOnly(not editable)
        self.headquarters_email_field.setReadOnly(not editable)
        self.sales_rep_name_field.setReadOnly(not editable)
        self.sales_rep_office_phone_field.setReadOnly(not editable)
        self.sales_rep_cell_phone_field.setReadOnly(not editable)
        self.sales_rep_email1_field.setReadOnly(not editable)
        self.sales_rep_email2_field.setReadOnly(not editable)
        for i in range(self.warehouse_layout.count()):
            widget = self.warehouse_layout.itemAt(i).widget()
            if widget:
                for field in widget.findChildren(QLineEdit):
                    field.setReadOnly(not editable)

    def save_vendor(self):
        """Save vendor details to the database."""
        try:
            name = self.name_field.text().strip()
            if not name:
                QMessageBox.warning(self, "Error", "Name is required.", parent=self)
                return

            vendor = {
                "name": name,
                "full_name": self.full_name_field.text().strip(),
                "abbreviation": self.abbreviation_field.text().strip(),
                "headquarters_address": self.headquarters_address_field.text().strip(),
                "headquarters_phone": self.headquarters_phone_field.text().strip(),
                "headquarters_email": self.headquarters_email_field.text().strip(),
                "sales_rep": {
                    "name": self.sales_rep_name_field.text().strip(),
                    "office_phone": self.sales_rep_office_phone_field.text().strip(),
                    "cell_phone": self.sales_rep_cell_phone_field.text().strip(),
                    "email1": self.sales_rep_email1_field.text().strip(),
                    "email2": self.sales_rep_email2_field.text().strip(),
                },
                "warehouses": []
            }

            # Collect warehouse information
            for i in range(self.warehouse_layout.count()):
                widget = self.warehouse_layout.itemAt(i).widget()
                if widget:
                    warehouse = {
                        "name": widget.findChildren(QLineEdit)[0].text().strip(),
                        "address": widget.findChildren(QLineEdit)[1].text().strip(),
                        "phone": widget.findChildren(QLineEdit)[2].text().strip(),
                        "email": widget.findChildren(QLineEdit)[3].text().strip(),
                    }
                    vendor["warehouses"].append(warehouse)

            # Save to the database
            self.db_handler.create_or_update_vendor(vendor)
            print("Vendor saved successfully:", vendor)

            # Reset the form and disable the Save button
            self.clear_fields()
            self.save_button.setEnabled(False)

        except Exception as e:
            print(f"Error saving vendor: {e}")
            QMessageBox.critical(self, "Error", f"An error occurred while saving: {e}", parent=self)


    def cancel_changes(self):
        """Cancel changes and reload the current vendor."""
        self.vendor_changed()

    def delete_vendor(self):
        """Delete the selected vendor."""
        if self.vendor_selector.currentText() == "Create New":
            QMessageBox.warning(self, "Error", "Cannot delete a vendor that hasn’t been created.", parent=self)
            return

        confirm = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete the vendor '{self.vendor_selector.currentText()}'?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirm == QMessageBox.Yes:
            collection = self.db_handler.get_collection("vendors")
            collection.delete_one({"name": self.vendor_selector.currentText()})
            QMessageBox.information(self, "Success", "Vendor deleted successfully.", parent=self)
            self.load_existing_vendors()
            self.clear_fields()
