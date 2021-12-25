from base_windows.base_dialog import BaseDialog
from exception.input_data_exception import InputDataException
from PyQt5.uic import loadUi


class AddStorageDialog(BaseDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("ui_files/dialogs/add/AddStorageDialog.ui", self)
        self.connector = parent.connector
        self.data = parent.data
        self._connect_signals_slots()

    def _connect_signals_slots(self):
        self.dialogBox.accepted.connect(self._ok_button_clicked)
        self.dialogBox.rejected.connect(self.close)

    def _ok_button_clicked(self):
        try:
            address = self.addressEdit.text() if len(self.addressEdit.text()) > 0 else None
            square = self.squareBox.value() if self.squareBox.value() > 0 else None
            if (address is None) or (square is None):
                raise InputDataException('Не указаны обязательные поля')

            if address in self.data['Адрес_склада']:
                raise InputDataException('Указанный поставщик уже существует')

            self.connector.insert(
                table='storages',
                values=f"(default, '{address}', '{square}')"
            )

            self.connector.commit()
            self.close()
        except InputDataException as input_error:
            self._error_dialog_call(input_error.message)
        except Exception as e:
            print(e)

