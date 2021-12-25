from base_windows.base_dialog import BaseDialog
from exception.input_data_exception import InputDataException
from PyQt5.uic import loadUi


class AddProducerDialog(BaseDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("ui_files/dialogs/add/AddProducerDialog.ui", self)
        self.connector = parent.connector
        self.data = parent.data
        self._connect_signals_slots()

    def _connect_signals_slots(self):
        self.dialogBox.accepted.connect(self._ok_button_clicked)
        self.dialogBox.rejected.connect(self.close)

    def _ok_button_clicked(self):
        try:
            producer_name = self.producerNameEdit.text() if len(self.producerNameEdit.text()) > 0 else None
            registration = self.registrationEdit.text() if len(self.registrationEdit.text()) > 0 else None
            phone = self.phoneEdit.text() if len(self.phoneEdit.text()) > 0 else None
            address = self.adressEdit.text() if len(self.adressEdit.text()) > 0 else None
            if (producer_name is None) or (registration is None) or (phone is None) or (address is None):
                raise InputDataException('Не указаны обязательные поля')
            if 11 > len(phone) > 12:
                raise InputDataException('Номер телефона указан некорректно')
            if not registration.isdigit():
                raise InputDataException('Регистрационный номер указан некорректно')
            if (producer_name in self.data['Производитель'])\
                    or (registration in self.data['Данные_регистрации'].apply(lambda x: x.split(' ')[-1])):
                raise InputDataException('Указанный производитель уже существует')

            registration = 'регистрационный номер' + ' ' + registration
            self.connector.insert(
                table='producers',
                values=f"(default, '{producer_name}', '{address}', '{phone}', '{registration}')"
            )
            self.connector.commit()
            self.close()
        except InputDataException as input_error:
            self._error_dialog_call(input_error.message)
        except Exception as e:
            print(e)

