from base_windows.base_dialog import BaseDialog
from exception.input_data_exception import InputDataException
from PyQt5.uic import loadUi


class EditProducerDialog(BaseDialog):

    def __init__(self, producer_id, parent=None):
        super().__init__(parent)
        loadUi("ui_files/dialogs/edit/EditProducerDialog.ui", self)
        self.connector = parent.connector
        self.data = parent.data
        self.current_producer_id = producer_id
        self._connect_signals_slots()
        self._update_UI()

    def _update_UI(self):
        self.producerNameEdit.clear()
        self.registrationEdit.clear()
        self.addressEdit.clear()
        self.phoneEdit.clear()
        current_producer_name = self.data[
            self.data['ID_производителя'] == self.current_producer_id
        ]['Производитель'].iloc[0]
        current_registration = self.data[
            self.data['ID_производителя'] == self.current_producer_id
        ]['Данные_регистрации'].iloc[0].replace('регистрационный номер ', '')

        current_address = self.data[
            self.data['ID_производителя'] == self.current_producer_id
        ]['Юридический_адрес'].iloc[0]

        current_phone = self.data[
            self.data['ID_производителя'] == self.current_producer_id
        ]['Телефон'].iloc[0]

        self.producerNameEdit.setText(current_producer_name)
        self.registrationEdit.setText(current_registration)
        self.addressEdit.setText(current_address)
        self.phoneEdit.setText(current_phone)

    def _connect_signals_slots(self):
        self.dialogBox.accepted.connect(self._ok_button_clicked)
        self.dialogBox.rejected.connect(self.close)

    def _ok_button_clicked(self):
        try:
            producer_name = self.producerNameEdit.text() if len(self.producerNameEdit.text()) > 0 else None
            registration = self.registrationEdit.text() if len(self.registrationEdit.text()) > 0 else Non
            registration = registration.replace(' ', '')
            phone = self.phoneEdit.text() if len(self.phoneEdit.text()) > 0 else None
            address = self.addressEdit.text() if len(self.addressEdit.text()) > 0 else None

            if (producer_name is None) or (registration is None) or (phone is None) or (address is None):
                raise InputDataException('Не указаны обязательные поля')
            if 11 > len(phone) > 12:
                raise InputDataException('Номер телефона указан некорректно')
            if not registration.isdigit():
                raise InputDataException('Регистрационный номер указан некорректно')
            if (producer_name in self.data['Производитель']) \
                    or (registration in self.data['Данные_регистрации'].apply(lambda x: x.split(' ')[-1])):
                raise InputDataException('Указанный производитель уже существует')

            registration = 'регистрационный номер' + ' ' + registration
            self.connector.update(
                table='producers',
                new_values=f""" "Производитель"= '{producer_name}', "Юридический_адрес"='{address}', "Телефон"='{phone}', "Данные_регистрации"='{registration}' """,
                condition=f""""ID_производителя"={self.current_producer_id}"""
            )
            self.connector.commit()
            self.close()
        except InputDataException as input_error:
            self._error_dialog_call(input_error.message)
        except Exception as e:
            print(e)

