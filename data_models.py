from enum import Enum


class Currency(Enum):
    USD = 1
    EUR = 2
    RUB = 3
    GEL = 4

    @classmethod
    def from_str(cls, label: str):
        label = label.upper()
        if label in ('USD', 1):
            return cls.USD
        elif label in ('EUR', 2):
            return cls.EUR
        elif label in ('RUB', 3):
            return cls.RUB
        elif label in ('GEL', 4):
            return cls.GEL
        else:
            raise NotImplementedError


class CurrencyData:
    def __init__(self, timestamp: int, rate: float, currency: Currency, source_currency: Currency):
        self.timestamp = timestamp
        self.rate = rate
        self.currency = currency
        self.source_currency = source_currency
