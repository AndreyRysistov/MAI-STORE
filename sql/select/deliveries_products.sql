select
deliveries_products."ID_товара",
deliveries_products."ID_поставки",
products."Артикул",
products."Наименование_товара",
products."Оптовая_цена",
products."Вес_(кг)",
deliveries_products."Количество",
products."Единица",
(deliveries_products."Количество" * products."Оптовая_цена") as "Итого"
from
deliveries_products
join products on deliveries_products."ID_товара" = products."ID_товара"