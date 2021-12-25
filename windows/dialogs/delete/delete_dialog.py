from base_windows.base_dialog import BaseDialog
from exception.input_data_exception import InputDataException
from PyQt5.uic import loadUi


class DeleteDialog(BaseDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("ui_files/dialogs/delete/DeleteDialog.ui", self)
        self.connector = parent.connector
        self.data = parent.data
        self.table = parent.table
        row = parent.tableView.currentRow()
        self.id_value = int(parent.tableView.item(row, 0).text())
        self.id_col_name = parent.data.columns[0]
        self._connect_signals_slots()

    def _connect_signals_slots(self):
        self.dialogBox.accepted.connect(self._ok_button_clicked)
        self.dialogBox.rejected.connect(self.close)

    def _ok_button_clicked(self):
        try:
            if self.table == 'deliveries':
                condition = f'"{self.id_col_name}" = {self.id_value}'
                self.connector.delete(table='deliveries_products', condition=condition)
            condition = f'"{self.id_col_name}" = {self.id_value}'
            self.connector.delete(table=self.table, condition=condition)
            self.connector.commit()
            self.close()
        except Exception as input_error:
            self._error_dialog_call('Данную запись нельзя удалить, так как на нее есть ссылки из других таблиц')

