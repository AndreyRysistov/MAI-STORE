from base_windows.base_dialog import BaseDialog
from PyQt5.uic import loadUi


class WriteOffProductDialog(BaseDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("ui_files/dialogs/delete/WriteOffProduct.ui", self)
        self.connector = parent.connector
        self.data = parent.data
        self.table = parent.table
        row = parent.tableView.currentRow()
        self.id_value = int(parent.tableView.item(row, 0).text())
        self.id_col_name = parent.data.columns[0]
        self.current_product = self.data[
            self.data[self.id_col_name] == self.id_value
            ]['Наименование_товара'].iloc[0]
        self.current_available_count = self.data[
            self.data[self.id_col_name] == self.id_value
            ]['Доступно'].iloc[0]
        self.current_write_off_count = self.data[
            self.data[self.id_col_name] == self.id_value
            ]['Доступно'].iloc[0]
        self._connect_signals_slots()
        self._update_UI()

    def _connect_signals_slots(self):
        self.dialogBox.accepted.connect(self._ok_button_clicked)
        self.dialogBox.rejected.connect(self.close)

    def _update_UI(self):
        self.productLabel.setText(self.current_product)

    def _ok_button_clicked(self):
        try:
            write_of_count = self.writeOffBox.value()
            new_write_of_count = self.current_write_off_count + write_of_count
            new_available_count = self.current_available_count - write_of_count
            self.connector.update(
                table='products_on_storages',
                new_values=f""" "Доступно"= '{new_available_count}', "Списано"= '{new_write_of_count}' """,
                condition=f'"{self.id_col_name}" = {self.id_value}'
            )
            self.connector.commit()
            self.close()
        except Exception as input_error:
            print(input_error)
            self._error_dialog_call(input_error)

