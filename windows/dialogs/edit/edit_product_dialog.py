from base_windows.base_dialog import BaseDialog
from exception.input_data_exception import InputDataException
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
import shutil


class EditProductDialog(BaseDialog):

    def __init__(self, product_id, parent=None):
        super().__init__(parent)
        loadUi("ui_files/dialogs/edit/EditProductDialog.ui", self)
        self.connector = parent.connector
        self.data = parent.data
        self.current_product_id = product_id
        self._connect_signals_slots()
        self._update_UI()

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

        current_data = self.data[self.data['ID_товара'] == self.current_product_id]
        current_articul = current_data['Артикул'].iloc[0]
        current_name = current_data['Наименование_товара'].iloc[0]
        current_size = current_data['Размер'].iloc[0]
        current_material = current_data['Материал'].iloc[0]
        current_color = current_data['Цвет'].iloc[0]
        current_category = current_data['Категория'].iloc[0]
        current_weight = current_data['Вес_(кг)'].iloc[0]
        current_producer = current_data['Производитель'].iloc[0]
        current_description = current_data['Описание_товара'].iloc[0]
        current_unit = current_data['Единица'].iloc[0]
        current_file = current_data['Файл'].iloc[0]
        current_trade_price = current_data['Оптовая_цена'].iloc[0]
        current_retail_price = current_data['Реализуемая_цена'].iloc[0]

        self.articulEdit.setText(current_articul)
        self.nameBox.setCurrentText(current_name)
        self.sizeEdit.setText(current_size)
        self.colorBox.setCurrentText(current_color)
        self.materialBox.setCurrentText(current_material)
        self.categoryBox.setCurrentText(current_category)
        self.weightEdit.setText(str(current_weight))
        self.producerBox.setCurrentText(current_producer)
        self.unitBox.setCurrentText(current_unit)
        self.fileEdit.setText(current_file)
        self.descriptionEdit.setText(current_description)
        self.tradePriceEdit.setText(str(current_trade_price))
        self.retailPriceEdit.setText(str(current_retail_price))

    def _connect_signals_slots(self):
        self.dialogBox.accepted.connect(self._ok_button_clicked)
        self.dialogBox.rejected.connect(self.close)
        self.toolButton.clicked.connect(self._tool_button_clicked)

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
            if file not in self.connector.load_table('images')['Файл'].values:
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
            self.connector.update(
                table='products',
                new_values=f""" "Артикул"= '{articul}', \
                "Наименование_товара"='{product_name}', "Размер"='{size}', \
                "Материал"='{material}', "Цвет"='{color}', \
                "ID_изображения"='{image_id}', "Оптовая_цена"='{trade_price}', \
                "ID_производителя"='{producer_id}', "ID_категории"='{category_id}', \
                "Описание_товара"='{description}', "Реализуемая_цена"='{retail_price}', \
                "Единица"='{unit}', "Вес_(кг)"='{weight}'
                """,
                condition=f""" "ID_товара"={self.current_product_id}"""
            )
            self.connector.commit()
            self.close()
        except InputDataException as input_error:
            self._error_dialog_call(input_error.message)
        except Exception as e:
            print(e)

