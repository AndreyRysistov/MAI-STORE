from PyQt5.uic import loadUi
from base_windows.data_widget import DataWidget
from PyQt5 import QtWidgets
from windows.dialogs.add.form_delivery_dialog import FormDeliveryDialog


class DeliveriesWidget(DataWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('ui_files/widgets/DeliveriesWidget.ui', self)
        self._connect_signals_slots()

    def _connect_signals_slots(self):
        self.tableView.itemClicked.connect(self._on_cell_item_clicked)
        self.tableView.itemDoubleClicked.connect(self._on_cell_item_clicked)
        self.sortButton.clicked.connect(self._sort_button_clicked)
        self.deleteDeliveryButton.clicked.connect(self._delete_button_clicked)
        self.formDeliveryButton.clicked.connect(self._form_delivery_button_clicked)
        self.updateButton.clicked.connect(lambda x: self.update_table(load=True))
        self.resetButton.clicked.connect(self._reset_button_clicked)
        self.filterButton.clicked.connect(self._find_button_clicked)

    def _form_delivery_button_clicked(self):
        try:
            dialog = FormDeliveryDialog(self)
            dialog.exec()
            self.update_table(load=True)
        except Exception as e:
            print(e)

    def _on_cell_item_clicked(self, item):
        try:
            col_idx = self.tableView.column(item)
            col_name = self.tableView.column_labels[col_idx]
            text = item.text()
            if col_name == 'ID_поставки':
                selected_data = self.connector.load_table('deliveries_products')
                selected_data = selected_data[selected_data['ID_поставки'] == int(text)]
                self.update_information_table(selected_data)
            elif col_name == 'Поставщик':
                selected_data = self.connector.load_table('suppliers')
                selected_data = selected_data[selected_data['Поставщик'] == text]
                self.update_information_table(selected_data)
            elif col_name == 'Склад':
                selected_data = self.connector.load_table('storages')
                selected_data = selected_data[selected_data['Адрес_склада'] == text]
                self.update_information_table(selected_data)
        except Exception as e:
            print(e)

    def update_information_table(self, data):
        self.informationTable.setRowCount(0)
        self.informationTable.setColumnCount(len(data.columns))
        self.informationTable.setHorizontalHeaderLabels(data.columns)
        self.informationTable.column_labels = list(data.columns)

        for n, row in zip(range(0, data.shape[0]), data.values):
            self.informationTable.insertRow(self.informationTable.rowCount())
            for m in range(len(row)):
                item = QtWidgets.QTableWidgetItem(str(row[m]))
                self.informationTable.setItem(int(n), int(m), item)
        self.informationTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.informationTable.horizontalHeader().setMinimumSectionSize(0)




