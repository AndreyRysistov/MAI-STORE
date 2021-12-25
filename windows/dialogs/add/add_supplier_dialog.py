from base_windows.base_dialog import BaseDialog
from exception.input_data_exception import InputDataException
from PyQt5.uic import loadUi


class AddSuppliersDialog(BaseDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("ui_files/dialogs/add/AddSuppliersDialog.ui", self)
        self.connector = parent.connector
        self.data = parent.data
        self._connect_signals_slots()
        self._update_UI()

    def _connect_signals_slots(self):
        self.dialogBox.accepted.connect(self._ok_button_clicked)
        self.dialogBox.rejected.connect(self.close)

    def _ok_button_clicked(self):
        try:
            supplier_name = self.supplierEdit.text() if len(self.supplierEdit.text()) > 0 else None
            address = self.addressEdit.text() if len(self.addressEdit.text()) > 0 else None
            phone = self.phoneEdit.text() if len(self.phoneEdit.text()) > 0 else None
            city = self.cityBox.currentText() if len(self.cityBox.currentText()) > 0 else None
            tarif = self.tarifBox.value() if self.tarifBox.value() > 0 else None
            if (supplier_name is None) or (city is None) or (address is None) or (tarif is None):
                raise InputDataException('Не указаны обязательные поля')
            if 11 > len(phone) > 12:
                raise InputDataException('Номер телефона указан некорректно')
            if (supplier_name in self.data['Поставщик']) and (phone in self.data['Телефон']):
                raise InputDataException('Указанный поставщик уже существует')

            self.connector.insert(
                table='suppliers',
                values=f"(default, '{supplier_name}', '{city}', '{address}', '{phone}', '{tarif}')"
            )
            self.connector.commit()
            self.close()
        except InputDataException as input_error:
            self._error_dialog_call(input_error.message)
        except Exception as e:
            print(e)


    def _update_UI(self):
        self.supplierEdit.clear()
        self.addressEdit.clear()
        self.phoneEdit.clear()
        self.cityBox.clear()
        self.tarifBox.clear()
        self.cityBox.addItems([''] + list(map(str, self.data['Город'].unique())))
