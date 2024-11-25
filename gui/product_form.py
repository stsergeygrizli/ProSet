from PyQt5.QtWidgets import QMainWindow, QMenuBar, QMenu, QAction, QApplication
from gui.vendor_management_window import VendorManagementWindow
from gui.sku_management_window import SkuManagementWindow
import sys


class ProductForm(QMainWindow):
    """Main GUI for the application."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ProSet - Product Management")
        self.resize(800, 600)

        # Menu bar
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        # Add menus
        self.add_menus()

    def add_menus(self):
        """Add menus to the menu bar."""
        # Vendor Management Menu
        vendor_menu = QMenu("Vendors", self)
        self.menu_bar.addMenu(vendor_menu)

        # Vendor Management Action
        vendor_action = QAction("Manage Vendors", self)
        vendor_action.triggered.connect(self.open_vendor_management)
        vendor_menu.addAction(vendor_action)

        # Manage SKUs Action
        skus_action = QAction("Manage SKUs", self)
        skus_action.triggered.connect(self.open_sku_management)
        vendor_menu.addAction(skus_action)

    def open_vendor_management(self):
        """Open the Vendor Management Window."""
        self.vendor_window = VendorManagementWindow()
        self.vendor_window.exec_()

    def open_sku_management(self):
        """Open the SKU Management window."""
        self.sku_management_window = SkuManagementWindow()
        self.sku_management_window.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = ProductForm()
    main_window.show()
    sys.exit(app.exec_())
