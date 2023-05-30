from data_models import KoronaData
from korona_service import handlers
from korona_service.korona_api import _get_korona_data


def register_handlers():
    handlers.register_handlers()


def get_korona_amount_for(amount: int) -> KoronaData:
    return _get_korona_data(amount)
