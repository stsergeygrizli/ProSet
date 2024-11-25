from PyQt5.QtWidgets import QApplication
from gui.sku_management_window import SkuManagementWindow
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    sku_window = SkuManagementWindow()
    sku_window.show()
    sys.exit(app.exec_())
