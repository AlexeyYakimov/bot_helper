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


class KoronaData:
    def __init__(self,
                 timestamp: int,
                 rate: float,
                 sending_amount: float,
                 sending_currency: Currency,
                 receiving_amount: float,
                 receiving_currency: Currency,
                 commission: float):
        self.timestamp = timestamp
        self.rate = rate
        self.sending_amount = sending_amount
        self.sending_currency = sending_currency
        self.receiving_amount = receiving_amount
        self.receiving_currency = receiving_currency
        self.commission = commission
