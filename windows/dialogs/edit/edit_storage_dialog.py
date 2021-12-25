from base_windows.base_dialog import BaseDialog
from exception.input_data_exception import InputDataException
from PyQt5.uic import loadUi


class EditStorageDialog(BaseDialog):

    def __init__(self, storage_id, parent=None):
        super().__init__(parent)
        loadUi("ui_files/dialogs/edit/EditStorageDialog.ui", self)
        self.connector = parent.connector
        self.data = parent.data
        self.current_storage_id = storage_id
        self._connect_signals_slots()
        self._update_UI()

    def _update_UI(self):
        self.addressEdit.clear()
        self.squareBox.clear()
        current_address = self.data[self.data['ID_склада'] == self.current_storage_id]['Адрес_склада'].iloc[0]
        current_square = self.data[self.data['ID_склада'] == self.current_storage_id]['Площадь (кв. метр)'].iloc[0]
        self.addressEdit.setText(current_address)
        self.squareBox.setValue(current_square)

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
                raise InputDataException('Указанный склад уже существует')

            self.connector.update(
                table='storages',
                new_values=f""" "Адрес_склада"= '{address}', "Площадь (кв. метр)"='{square}' """,
                condition=f""" "ID_склада"={self.current_storage_id}"""
            )

            self.connector.commit()
            self.close()
        except InputDataException as input_error:
            self._error_dialog_call(input_error.message)
        except Exception as e:
            print(e)

