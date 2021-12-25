from PyQt5.uic import loadUi
from base_windows.data_widget import DataWidget
from windows.dialogs.add.add_supplier_dialog import AddSuppliersDialog
from windows.dialogs.edit.edit_supplier_dialog import EditSupplierDialog


class SuppliersWidget(DataWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('ui_files/widgets/SuppliersWidget.ui', self)
        self._connect_signals_slots()

    def _connect_signals_slots(self):
        self.tableView.itemClicked.connect(self._on_cell_item_clicked)
        self.tableView.itemDoubleClicked.connect(self._on_cell_item_clicked)
        self.addSupplierButton.clicked.connect(self._add_supplier_button_clicked)
        self.sortButton.clicked.connect(self._sort_button_clicked)
        self.deleteSupplierButton.clicked.connect(self._delete_button_clicked)
        self.editSupplierButton.clicked.connect(self._edit_supplier_button_clicked)
        self.updateButton.clicked.connect(lambda x: self.update_table(load=True))
        self.resetButton.clicked.connect(self._reset_button_clicked)
        self.filterButton.clicked.connect(self._find_button_clicked)

    def _edit_supplier_button_clicked(self):
        try:
            row = self.tableView.currentRow()
            id_value = int(self.tableView.item(row, 0).text())
            dialog = EditSupplierDialog(id_value, self)
            dialog.exec()
            self.update_table(load=True)
        except Exception as e:
            print(e)


    def _add_supplier_button_clicked(self):
        try:
            dialog = AddSuppliersDialog(self)
            dialog.exec()
            self.update_table(load=True)
        except Exception as e:
            print(e)

    def _on_cell_item_clicked(self, item):
        try:
            col_idx = self.tableView.column(item)
            col_name = self.tableView.column_labels[col_idx]
            text = item.text()
            self.informationBrowser.clear()
            self.informationBrowser.append(text)
        except Exception as e:
            print(e)