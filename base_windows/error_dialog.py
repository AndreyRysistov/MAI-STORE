from PyQt5 import QtWidgets
from PyQt5.uic import loadUi


class ErrorDialog(QtWidgets.QDialog):

    def __init__(self, error_message):
        super().__init__()
        loadUi("ui_files/dialogs/error/ErrorDialog.ui", self)
        self.errorLabel.setText(error_message)

    def _connect_signals_slots(self):
        self.dialogBox.accepted.connect(self._ok_button_clicked)