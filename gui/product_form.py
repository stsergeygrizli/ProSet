from PyQt5.QtWidgets import QMainWindow, QMenuBar, QMenu, QAction, QApplication
from gui.vendor_management_window import VendorManagementWindow
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
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

    def open_vendor_management(self):
        """Open the Vendor Management Window."""
        vendor_window = VendorManagementWindow()
        vendor_window.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = ProductForm()
    main_window.show()
    sys.exit(app.exec_())
