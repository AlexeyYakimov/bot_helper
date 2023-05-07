from aqi_service import iquair_service as aqi, handlers


def get_data() -> str:
    return aqi.get_data()


def get_description() -> str:
    return aqi.get_description()


def register_handlers():
    handlers.register_handlers()
