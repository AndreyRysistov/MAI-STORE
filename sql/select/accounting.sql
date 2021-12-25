select
products."ID_товара",
products."Артикул",
products."Наименование_товара",
products_on_storages."Доступно",
products_on_storages."Списано",
products_on_storages."Реализовано",
storages."ID_склада",
storages."Адрес_склада"

from
products_on_storages
join products on products_on_storages."ID_товара" = products."ID_товара"
join storages on products_on_storages."ID_склада" = storages."ID_склада"