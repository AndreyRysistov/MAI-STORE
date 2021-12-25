import pandas as pd
import pyodbc
from db_connector import query

sheets = [
    'categories',
    'images',
    'producers',
    'products',
    'suppliers',
    'storages',
    'deliveries',
    'deliveries_products',
    'products_on_storages',
]


def fill_db_from_excel(path, conn):
    cursor = conn.cursor()
    for sheet in sheets:
        data = pd.read_excel(path, sheet_name=sheet)
        if 'Дата_поставки' in data.columns:
            data['Дата_поставки'] = data['Дата_поставки'].astype('str')
        if 'Телефон' in data.columns:
            data['Телефон'] = data['Телефон'].astype('str')
        for index, row in data.iterrows():
            print(row.values)
            try:
                query.insert(table=sheet, values=tuple(row.values), cursor=cursor)
            except:
                continue
    conn.commit()



if __name__ == '__main__':
    conn = pyodbc.connect('DSN=MAI-store')
    fill_db_from_excel('data/bd.xlsx', conn)
    conn.close()
