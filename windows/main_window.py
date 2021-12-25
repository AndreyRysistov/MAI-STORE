from base_windows import main_window
from db_connector.db_connector import DBConnector
from PyQt5 import QtCore, QtGui, QtWidgets


class MainWindow(QtWidgets.QMainWindow, main_window.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('MAI-Store')
        self.connector = DBConnector()
        self._init_tables()

    def _init_tables(self):
        self.productsTab.set_connector(self.connector, "products")
        self.productsTab.update_table(load=True)

        self.producersTab.set_connector(self.connector, "producers")
        self.producersTab.update_table(load=True)

        self.accountingTab.set_connector(self.connector, "accounting")
        self.accountingTab.update_table(load=True)

        self.storagesTab.set_connector(self.connector, "storages")
        self.storagesTab.update_table(load=True)

        self.deliveriesTab.set_connector(self.connector, "deliveries")
        self.deliveriesTab.update_table(load=True)

        self.suppliersTab.set_connector(self.connector, "suppliers")
        self.suppliersTab.update_table(load=True)

        self.MainTab.setTabText(self.MainTab.indexOf(self.accountingTab), "Учет")