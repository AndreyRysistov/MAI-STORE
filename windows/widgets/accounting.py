from PyQt5.uic import loadUi
from base_windows.data_widget import DataWidget
from windows.dialogs.delete.write_off_product_dialog import WriteOffProductDialog

class AccountingWidget(DataWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('ui_files/widgets/AccountingWidget.ui', self)
        self.table = None
        self.connector = None
        self.data = None
        self._connect_signals_slots()

    def _connect_signals_slots(self):
        self.tableView.itemClicked.connect(self._on_cell_item_clicked)
        self.tableView.itemDoubleClicked.connect(self._on_cell_item_clicked)
        self.sortButton.clicked.connect(self._sort_button_clicked)
        self.updateButton.clicked.connect(lambda x: self.update_table(load=True))
        self.resetButton.clicked.connect(self._reset_button_clicked)
        self.filterButton.clicked.connect(self._find_button_clicked)
        self.writeOffProductButton.clicked.connect(self._write_off_button_clicked)

    def _write_off_button_clicked(self):
        try:
            dialog = WriteOffProductDialog(self)
            dialog.exec()
            self.update_table(load=True)
        except Exception as e:
            print(e)

    def _on_cell_item_clicked(self, item):
        col_idx = self.tableView.column(item)
        col_name = self.tableView.column_labels[col_idx]
        text = item.text()
        self.informationBrowser.clear()
        self.informationBrowser.append(text)



