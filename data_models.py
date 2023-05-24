class Currency:
    def __init__(self, currency_id: int, name: str, full_name: str):
        self.currency_id = currency_id
        self.name = name
        self.full_name = full_name


class CurrencyData:
    def __init__(self, timestamp: int, rate: float, currency: Currency, source_currency: Currency):
        self.timestamp = timestamp
        self.rate = rate
        self.currency = currency
        self.source_currency = source_currency
