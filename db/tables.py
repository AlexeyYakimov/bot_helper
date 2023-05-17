from sqlite3 import Error

from db.connection import create_connection

currency_table = "currency_name"
rates_table = "rates"


def _create_table(conn, create_table_sql) -> bool:
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        return True
    except Error as e:
        print(e)
        return False


def create_currency_db() -> bool:
    currency_name = f"""CREATE TABLE "{currency_table}" (
        "id"    INTEGER,
        "name"  TEXT UNIQUE,
        PRIMARY KEY("id")
    );"""
    with create_connection() as connection:
        return _create_table(connection, currency_name)


def create_rates_db() -> bool:
    rates = f"""CREATE TABLE "{rates_table}" (
        "id"    INTEGER UNIQUE,
        "timestamp" INTEGER,
        "rate"  NUMERIC,
        "id_currency_name"  INTEGER,
        "id_source" INTEGER, 
        PRIMARY KEY("id" AUTOINCREMENT),
        FOREIGN KEY("id_currency_name") REFERENCES "currency_name"("id"));"""

    with create_connection() as connection:
        return _create_table(connection, rates)


def drop_db():
    with create_connection() as connection:
        _create_table(connection, f"""DROP TABLE {rates_table}""")
        _create_table(connection, f"""DROP TABLE {currency_table}""")
