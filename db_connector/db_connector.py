import pyodbc
import pandas as pd


class DBConnector():

    def __init__(self):
        self.conn = pyodbc.connect('DSN=MAI-store')
        self.cursor = self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def load_table(self, table):
        data = pd.read_sql_query(
            open(f'sql/select/{table}.sql', 'r', encoding='utf-8').read(),
            con=self.conn
        )
        return data

    def insert(self, table, values, pkey=None):
        if pkey is None:
            query_text = "insert into {0} values {1};".format(table, values)
            print(query_text)
            self.cursor.execute(query_text)
        else:
            query_text = "insert into {0} values {1} returning {2};".format(table, values, pkey)
            print(query_text)
            self.cursor.execute(query_text)
            returned_id = self.cursor.fetchone()[0]
            return returned_id

    def insert_reterning(self, table, values):
        query_text = "insert into {0} values {1};".format(table, values)
        print(query_text)
        returned_id = self.cursor.execute(query_text)


    def update(self, table, new_values, condition=None):
        if condition is None:
            query_text = "update {0} set {1};".format(table, new_values)
        else:
            query_text = "update {0} set {1} where {2};".format(table, new_values, condition)
        print(query_text)
        self.cursor.execute(query_text)

    def delete(self, table, condition=None):
        if condition is None:
            query_text = "delete from {0}".format(table)
        else:
            query_text = "delete from {0} where {1}".format(table, condition)
        print(query_text)
        self.cursor.execute(query_text)

    def select(self, table, columns, condition=None):
        if condition is None:
            query_text = "select {0} from {1};".format(columns, table)
        else:
            query_text = "select {0} from {1} where {2};".format(columns, table, condition)
        print(query_text)

        try:
            selected_data = pd.read_sql(query_text, self.conn)
        except Exception as e:
            print(e)


        selected_data.fillna('', inplace=True, axis=0)
        selected_data.drop_duplicates(inplace=True)
        # for col in selected_data:
        #     selected_data[col] = selected_data[col].apply(lambda x: remove_spaces(x) if (type(x) is str) else int(x))
        return selected_data