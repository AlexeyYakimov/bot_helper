from sqlite3 import Error

from data_models import Currency
from db import tables
from db.connection import create_connection


def fill_currency_name():
    try:
        with create_connection() as conn:
            sql = f''' INSERT INTO {tables.currency_table}(id, name)
                      VALUES(?,?) '''
            cur = conn.cursor()
            cur.execute(sql, [Currency.USD.value, Currency.USD.name])
            cur.execute(sql, [Currency.EUR.value, Currency.EUR.name])
            cur.execute(sql, [Currency.RUB.value, Currency.RUB.name])
            cur.execute(sql, [Currency.GEL.value, Currency.GEL.name])
            conn.commit()
            return cur.lastrowid
    except Error as e:
        print(e)


def get_currency_by_id(currency_id: int) -> Currency:
    try:
        with create_connection() as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM {tables.currency_table} WHERE id= {currency_id}")

            result_id = cur.fetchall()[0][0]

            return Currency(result_id)
    except Error as e:
        print(e)
