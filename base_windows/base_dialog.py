from PyQt5 import QtWidgets
from base_windows.error_dialog import ErrorDialog


class BaseDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

    def _error_dialog_call(self, error_message):
        try:
            dialog = ErrorDialog(error_message)
            dialog.exec()
        except Exception as err:
            print(err)