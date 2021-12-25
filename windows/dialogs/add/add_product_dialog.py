from base_windows.base_dialog import BaseDialog
from PyQt5.uic import loadUi
from exception.input_data_exception import InputDataException
from PyQt5 import QtWidgets
import shutil


class AddProductDialog(BaseDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("ui_files/dialogs/add/AddProductDialog.ui", self)
        self.connector = parent.connector
        self.data = parent.data
        self._update_UI()
        self._connect_signals_slots()

    def _connect_signals_slots(self):
        self.dialogBox.accepted.connect(self._ok_button_clicked)
        self.dialogBox.rejected.connect(self.close)
        self.toolButton.clicked.connect(self._tool_button_clicked)

    def _tool_button_clicked(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        file_name = file_path.split('/')[-1]
        try:
            shutil.copy2(file_path, f'images/{file_name}')
        except Exception as e:
            pass
        self.fileEdit.setText(file_name)

    def _ok_button_clicked(self):
        try:
            articul = self.articulEdit.text() if len(self.articulEdit.text()) > 0 else None
            product_name = self.nameBox.currentText() if len(self.nameBox.currentText()) > 0 else None
            category = self.categoryBox.currentText() if len(self.categoryBox.currentText()) > 0 else None
            producer = self.producerBox.currentText() if len(self.producerBox.currentText()) > 0 else None

            color = self.colorBox.currentText() if len(self.colorBox.currentText()) > 0 else 'NULL'
            material = self.materialBox.currentText() if len(self.materialBox.currentText()) > 0 else 'NULL'
            unit = self.unitBox.currentText() if len(self.unitBox.currentText()) > 0 else 'NULL'
            file = self.fileEdit.text() if len(self.fileEdit.text()) > 0 else 'NULL'
            size = self.sizeEdit.text() if len(self.sizeEdit.text()) > 0 else 'NULL'
            description = self.descriptionEdit.toPlainText() if len(self.descriptionEdit.toPlainText()) > 0 else 'NULL'
            if (articul is None) or (product_name is None) or (category is None) or (producer is None):
                raise InputDataException('Не указаны обязательные поля')
            try:
                trade_price = float(self.tradePriceEdit.text().replace(' ', ''))
                retail_price = float(self.retailPriceEdit.text().replace(' ', ''))
                weight = float(self.weightEdit.text().replace(' ', '').replace(',', '.'))
            except ValueError:
                raise InputDataException('Указан неверный формат для числовых показателей')

            if category not in [self.categoryBox.itemText(i) for i in range(self.categoryBox.count())]:
                self.connector.insert(
                    table='categories',
                    values=f"(default, '{category}')"
                )

            if file not in self.connector.load_table('images')['Файл']:
                self.connector.insert(
                    table='images',
                    values=f"(default, '{file}')"
                )
            category_table = self.connector.load_table('categories')
            category_id = category_table[category_table['Категория'] == category]['ID_категории'].iloc[0]
            image_table = self.connector.load_table('images')
            image_id = image_table[image_table['Файл'] == file]['ID_изображения'].iloc[0]
            producer_table = self.connector.load_table('producers')
            producer_id = producer_table[producer_table['Производитель'] == producer]['ID_производителя'].iloc[0]

            self.connector.insert(
                table="""products ("ID_товара", "Артикул", \
                "Наименование_товара", "Размер", \
                "Материал", "Цвет", "ID_изображения", \
                "Оптовая_цена", "ID_производителя", \
                "ID_категории", "Описание_товара", \
                "Реализуемая_цена", "Единица", "Вес_(кг)")""",
                values=f"""(default, '{articul}', '{product_name}', '{size}', '{material}', '{color}', {image_id},{trade_price}, {producer_id},{category_id}, '{description}', {retail_price}, '{unit}', {weight})""")
            self.connector.commit()
            self.close()
        except InputDataException as input_error:
            self._error_dialog_call(input_error.message)
        except Exception as e:
            print(e)


    def _update_UI(self):
        self.articulEdit.clear()
        self.nameBox.clear()
        self.sizeEdit.clear()
        self.colorBox.clear()
        self.materialBox.clear()
        self.categoryBox.clear()
        self.weightEdit.clear()
        self.producerBox.clear()
        self.unitBox.clear()
        self.fileEdit.clear()
        self.descriptionEdit.clear()
        self.tradePriceEdit.clear()
        self.retailPriceEdit.clear()
        category_table = self.connector.load_table('categories')
        producers_table = self.connector.load_table('producers')
        self.nameBox.addItems([''] + list(map(str, self.data['Наименование_товара'].unique())))
        self.materialBox.addItems([''] + list(map(str, self.data['Материал'].unique())))
        self.categoryBox.addItems([''] + list(map(str, category_table['Категория'].unique())))
        self.producerBox.addItems([''] + list(map(str, producers_table['Производитель'].unique())))
        self.colorBox.addItems([''] + list(map(str, self.data['Цвет'].unique())))
        self.unitBox.addItems([''] + list(map(str, self.data['Единица'].unique())))
