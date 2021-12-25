from PyQt5 import QtWidgets
from windows.dialogs.delete.delete_dialog import DeleteDialog


class DataWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.connector = None
        self.data = None
        self.table = None

    def set_connector(self, connector, table=None):
        self.connector = connector
        self.table = table

    def _reset_button_clicked(self):
        self.findEdit.clear()
        self.columnsBox.clear()
        self.update_table(load=False)

    def _sort_button_clicked(self):
        col = self.columnsBox.currentText()
        if col not in self.data.columns:
            col = self.data.columns[0]
        try:
            sorted_data = self.data.sort_values(by=col)
            self.update_table(data=sorted_data)
            self.columnsBox.setCurrentText(col)
        except Exception as e:
            print(e)

    def _delete_button_clicked(self):
        try:
            dialog = DeleteDialog(self)
            dialog.exec()
            self.update_table(load=True)
        except Exception as err:
            print(err)

    def _find_button_clicked(self):
        try:
            find_value = self.findEdit.text()
            column_id = self.tableView.currentColumn()
            if find_value.isdigit():
                find_value = float(find_value)
                filter_data = self.data[self.data.iloc[:, column_id] == find_value]
            else:
                filter_data = self.data[self.data.iloc[:, column_id].str.find(find_value) >= 0]
                filter_data_lower = self.data[self.data.iloc[:, column_id].str.lower().str.find(find_value)>=0]
                filter_data = filter_data.append(filter_data_lower)
            self.update_table(filter_data)

        except Exception as err:
            print(err)

    def update_table(self, data=None, load=False):
        if load:
            self.data = self.connector.load_table(self.table)
        if data is None:
            data = self.data
        self.columnsBox.clear()
        self.tableView.setRowCount(0)
        self.tableView.setColumnCount(len(data.columns))
        self.tableView.setHorizontalHeaderLabels(data.columns)
        self.tableView.column_labels = list(data.columns)

        for n, row in zip(range(0, data.shape[0]), data.values):
            self.tableView.insertRow(self.tableView.rowCount())
            for m in range(len(row)):
                item = QtWidgets.QTableWidgetItem(str(row[m]))
                self.tableView.setItem(int(n), int(m), item)
        self.tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.tableView.horizontalHeader().setMinimumSectionSize(0)
        self.columnsBox.addItems([''] + list(data.columns))