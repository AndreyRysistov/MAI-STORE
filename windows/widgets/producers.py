from PyQt5.uic import loadUi
from base_windows.data_widget import DataWidget
from windows.dialogs.add.add_producer_dialog import AddProducerDialog
from windows.dialogs.edit.edit_producer_dialog import EditProducerDialog


class ProducersWidget(DataWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('ui_files/widgets/ProducersWidget.ui', self)
        self._connect_signals_slots()

    def _connect_signals_slots(self):
        self.tableView.itemClicked.connect(self._on_cell_item_clicked)
        self.tableView.itemDoubleClicked.connect(self._on_cell_item_clicked)
        self.addProducerButton.clicked.connect(self._add_producer_button_clicked)
        self.sortButton.clicked.connect(self._sort_button_clicked)
        self.deleteProducerButton.clicked.connect(self._delete_button_clicked)
        self.editProducerButton.clicked.connect(self._edit_producer_button_clicked)
        self.updateButton.clicked.connect(lambda x: self.update_table(load=True))
        self.resetButton.clicked.connect(self._reset_button_clicked)
        self.filterButton.clicked.connect(self._find_button_clicked)

    def _add_producer_button_clicked(self):
        try:
            dialog = AddProducerDialog(self)
            dialog.exec()
            self.update_table(load=True)
        except Exception as e:
            print(e)

    def _edit_producer_button_clicked(self):
        try:
            row = self.tableView.currentRow()
            id_value = int(self.tableView.item(row, 0).text())
            dialog = EditProducerDialog(id_value, self)
            dialog.exec()
            self.update_table(load=True)
        except Exception as e:
            print(e)

    def _on_cell_item_clicked(self, item):
        col_idx = self.tableView.column(item)
        col_name = self.tableView.column_labels[col_idx]
        text = item.text()
        self.producersBrowser.clear()
        self.producersBrowser.append(text)