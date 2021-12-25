from base_windows.base_dialog import BaseDialog
from exception.input_data_exception import InputDataException
from PyQt5.uic import loadUi


class EditSupplierDialog(BaseDialog):

    def __init__(self, supplier_id, parent=None):
        super().__init__(parent)
        loadUi("ui_files/dialogs/edit/EditSupplierDialog.ui", self)
        self.connector = parent.connector
        self.data = parent.data
        self.current_supplier_id = supplier_id
        self._connect_signals_slots()
        self._update_UI()

    def _update_UI(self):
        self.supplierEdit.clear()
        self.tarifBox.clear()
        self.cityBox.clear()
        self.addressEdit.clear()
        self.phoneEdit.clear()
        current_supplier = self.data[
            self.data['ID_поставщика'] == self.current_supplier_id
        ]['Поставщик'].iloc[0]
        current_tarif = self.data[
            self.data['ID_поставщика'] == self.current_supplier_id
        ]['Тариф'].iloc[0]

        current_address = self.data[
            self.data['ID_поставщика'] == self.current_supplier_id
        ]['Юридический_адрес'].iloc[0]

        current_phone = self.data[
            self.data['ID_поставщика'] == self.current_supplier_id
        ]['Телефон'].iloc[0]

        current_city = self.data[
            self.data['ID_поставщика'] == self.current_supplier_id
        ]['Город'].iloc[0]

        self.supplierEdit.setText(current_supplier)
        self.tarifBox.setValue(current_tarif)
        self.addressEdit.setText(current_address)
        self.phoneEdit.setText(current_phone)
        self.cityBox.addItems([''] + list(map(str, self.data['Город'].unique())))
        self.cityBox.setCurrentText(current_city)

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

            self.connector.update(
                table='suppliers',
                new_values=f""" "Поставщик"= '{supplier_name}', "Город"='{city}', "Телефон"='{phone}', "Юридический_адрес"='{address}', "Тариф"='{tarif}'""",
                condition=f""" "ID_поставщика"={self.current_supplier_id}"""
            )
            self.connector.commit()
            self.close()
        except InputDataException as input_error:
            self._error_dialog_call(input_error.message)
        except Exception as e:
            print(e)

