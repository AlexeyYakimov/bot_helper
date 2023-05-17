from db.queues import fill_currency_name
from db.tables import create_currency_db, create_rates_db

create_currency_db()
fill_currency_name()
create_rates_db()
