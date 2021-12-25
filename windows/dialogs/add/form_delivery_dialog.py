from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from base_windows.base_dialog import BaseDialog
from exception.input_data_exception import InputDataException


class FormDeliveryDialog(BaseDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("ui_files/dialogs/add/FormDeliveryDialog.ui", self)
        self.connector = parent.connector
        self.data = parent.data
        self._update_UI()
        self._connect_signals_slots()

    def _connect_signals_slots(self):
        self.dialogBox.accepted.connect(self._ok_button_clicked)
        self.dialogBox.rejected.connect(self.close)

    def _ok_button_clicked(self):
        try:
            date = self.dateBox.dateTime().toPyDateTime()
            responsible = self.responsibleEdit.text() if len(self.responsibleEdit.text()) > 0 else None
            number = self.numberEdit.text() if len(self.numberEdit.text()) > 0 else None
            storage_address = self.storageBox.currentText() if len(self.storageBox.currentText()) > 0 else None
            supplier = self.supplierBox.currentText() if len(self.supplierBox.currentText()) > 0 else None
            checked_dict = {}
            for i in range(self.productTable.rowCount()):
                if self.productTable.cellWidget(i, 3).findChild(type(QCheckBox())).isChecked():
                    value = self.productTable.cellWidget(i, 4).findChild(type(QDoubleSpinBox())).value()
                    if value > 0:
                        key = self.productTable.item(i, 0).text()
                        checked_dict[int(key)] = int(value)
            if responsible is None or number is None or storage_address is None or supplier is None:
                raise InputDataException('Не введены обязательные поля')
            if number in self.data['№_товарной_накладной']:
                raise InputDataException('Такая поставка уже существует')
            suppliers_table = self.connector.load_table('suppliers')
            supplier_id = suppliers_table[suppliers_table['Поставщик'] == supplier]['ID_поставщика'].iloc[0]
            storages_table = self.connector.load_table('storages')
            storage_id = storages_table[storages_table['Адрес_склада'] == storage_address]['ID_склада'].iloc[0]
            self.connector.insert(
                table="deliveries",
                values=f"(default, '{supplier_id}', '{storage_id}', '{number}', '{date}', '{responsible}')"
            )
            self.connector.commit()
            new_data = self.connector.load_table('deliveries')
            delivery_id = int(new_data[new_data['№_товарной_накладной'] == number]['ID_поставки'].iloc[0])
            for product_id, count in checked_dict.items():
                accounting_table = self.connector.load_table('accounting')
                if product_id in accounting_table['ID_товара']:
                    available = accounting_table[accounting_table['ID_товара'] == int(product_id)]['Доступно'].iloc[0]
                    self.connector.insert(
                        table="deliveries_products",
                        values=f"({delivery_id}, '{product_id}', '{count}')"
                    )
                    available += count
                    self.connector.update(
                        table='products_on_storages',
                        new_values=f""" "Доступно" = '{available}'""",
                        condition=f""" "ID_товара"={product_id}"""
                    )
                else:
                    self.connector.insert(
                        table="deliveries_products",
                        values=f"({delivery_id}, '{product_id}', '{count}')"
                    )
                    self.connector.insert(
                        table='products_on_storages',
                        values=f"('{product_id}', '{storage_id}', '{count}', '{0}', '{0}')"
                    )
            self.connector.commit()
            self.close()
        except InputDataException as input_error:
            self._error_dialog_call(input_error.message)
        except Exception as e:
            print(e)


    def update_product_table(self, data, sort_col='Наименование_товара'):
        data = data.sort_values(by='Наименование_товара')
        self.productTable.setRowCount(0)
        self.productTable.setColumnCount(len(data.columns)+2)
        self.productTable.setHorizontalHeaderLabels(list(data.columns) + ['Выбран'] + ['Количество'])
        self.productTable.column_labels = list(data.columns) + ['Выбран'] + ['Количество']

        for n, row in zip(range(0, data.shape[0]), data.values):
            self.productTable.insertRow(self.productTable.rowCount())
            for m in range(len(row)):
                item = QtWidgets.QTableWidgetItem(str(row[m]))
                self.productTable.setItem(int(n), int(m), item)
        self.productTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.productTable.horizontalHeader().setMinimumSectionSize(0)
        for row in range(data['Наименование_товара'].nunique()):
            widget = QtWidgets.QWidget()
            checkbox = QtWidgets.QCheckBox()
            checkbox.setCheckState(Qt.Unchecked)

            layoutH1 = QtWidgets.QHBoxLayout(widget)
            layoutH1.addWidget(checkbox)
            layoutH1.setAlignment(Qt.AlignCenter)
            layoutH1.setContentsMargins(0, 0, 0, 0)
            self.productTable.setCellWidget(row, 3, widget)

            widget = QtWidgets.QWidget()
            spinbox = QtWidgets.QDoubleSpinBox()
            layoutH2 = QtWidgets.QHBoxLayout(widget)
            layoutH2.addWidget(spinbox)
            layoutH2.setAlignment(Qt.AlignCenter)
            layoutH2.setContentsMargins(0, 0, 0, 0)
            self.productTable.setCellWidget(row, 4, widget)


    def _update_UI(self):
        self.dateBox.clear()
        self.responsibleEdit.clear()
        self.storageBox.clear()
        self.numberEdit.clear()
        self.supplierBox.clear()
        storages = self.connector.load_table('storages')
        products = self.connector.load_table('products')
        suppliers = self.connector.load_table('suppliers')

        self.update_product_table(products[['ID_товара', 'Наименование_товара', 'Артикул']])
        self.storageBox.addItems([''] + list(map(str, storages['Адрес_склада'].unique())))
        self.supplierBox.addItems([''] + list(map(str, suppliers['Поставщик'].unique())))


