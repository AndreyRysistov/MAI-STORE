from PyQt5 import QtCore, QtGui
from PyQt5.uic import loadUi
from windows.dialogs.add.add_product_dialog import AddProductDialog
from windows.dialogs.edit.edit_product_dialog import EditProductDialog
from base_windows.data_widget import DataWidget


class ProductsWidget(DataWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('ui_files/widgets/ProductsWidget.ui', self)
        self._connect_signals_slots()

    def _connect_signals_slots(self):
        self.productImage.setVisible(False)
        self.tableView.itemClicked.connect(self._on_cell_item_clicked)
        self.tableView.itemDoubleClicked.connect(self._on_cell_item_clicked)
        self.sortButton.clicked.connect(self._sort_button_clicked)
        self.addProductButton.clicked.connect(self._add_product_button_clicked)
        self.editProductButton.clicked.connect(self._edit_product_button_clicked)
        self.deleteProductButton.clicked.connect(self._delete_button_clicked)
        self.updateButton.clicked.connect(lambda x: self.update_table(load=True))
        self.resetButton.clicked.connect(self._reset_button_clicked)
        self.filterButton.clicked.connect(self._find_button_clicked)

    def _edit_product_button_clicked(self):
        try:
            row = self.tableView.currentRow()
            id_value = int(self.tableView.item(row, 0).text())
            dialog = EditProductDialog(id_value, self)
            dialog.exec()
            self.update_table(load=True)
        except Exception as e:
            print(e)

    def _add_product_button_clicked(self):
        try:
            dialog = AddProductDialog(self)
            dialog.exec()
            self.update_table(load=True)
        except Exception as e:
            print(e)

    def _on_cell_item_clicked(self, item):
        try:
            self.productImage.setVisible(False)
            col_idx = self.tableView.column(item)
            col_name = self.tableView.column_labels[col_idx]
            if col_name == 'Файл':
                pixmap = QtGui.QPixmap(f'images/{item.text()}')
                self.productImage.setVisible(True)
                self.productImage.setPixmap(pixmap.scaled(
                    self.productImage.size(),
                    QtCore.Qt.KeepAspectRatio
                ))
            elif col_name == 'Производитель':
                selected_data = self.connector.select('producers', '*', condition=f""""Производитель" = '{item.text()}'""")
                text = ''
                for col, value in zip(selected_data.columns, *selected_data.values):
                    text += str(col) + ' : ' + str(value) + '\n'
                self.informationBrowser.clear()
                self.informationBrowser.append(text)
            else:
                text = item.text()
                self.informationBrowser.clear()
                self.informationBrowser.append(text)
        except Exception as e:
            print(e)

