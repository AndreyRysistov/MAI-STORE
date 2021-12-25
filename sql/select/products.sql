select
"ID_товара", "Артикул",
"Наименование_товара",
"Оптовая_цена",
"Реализуемая_цена",
"Вес_(кг)", "Материал",
"Цвет", "Размер",
"Производитель",
"Категория", "Файл", "Описание_товара", "Единица"
from
products
join images on products."ID_изображения"=images."ID_изображения"
join categories on products."ID_категории"=categories."ID_категории"
join producers on products."ID_производителя"=producers."ID_производителя"


