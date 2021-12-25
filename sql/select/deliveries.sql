select
deliveries."ID_поставки",
deliveries."Дата_поставки",
storages."Адрес_склада" as "Склад",
suppliers."Поставщик",
deliveries."№_товарной_накладной",
deliveries."Ответственный",
round(dp."Общий_вес" * dp."Общее количество" * suppliers."Тариф") as "Стоимость_поставки"
from
deliveries

join suppliers
    on deliveries."ID_поставщика" = suppliers."ID_поставщика"
join storages
    on deliveries."ID_склада" = storages."ID_склада"

left join (select
    deliveries_products."ID_поставки",
    sum(products."Вес_(кг)") as "Общий_вес",
    sum(deliveries_products."Количество") as "Общее количество"
    from
    deliveries_products
    join products
        on deliveries_products."ID_товара" = products."ID_товара"
    group by
        deliveries_products."ID_поставки"
) as dp
    on deliveries."ID_поставки" = dp."ID_поставки"