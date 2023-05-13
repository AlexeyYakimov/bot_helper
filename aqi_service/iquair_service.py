import arrow
import requests

from aqi_service.aqi_utils import get_usaqi_description, AQI
from in_memory_db.in_memory_data import TZ_GE
from in_memory_db.token_storage import Token, get_token

url = f"https://api.airvisual.com/v2/city?key={get_token(Token.AQI)}&country=Georgia&state=Ajaria&city=Batumi"

last_request = arrow.now(TZ_GE)
cached_value = 0
time_shift = 1
first_run = True


def get_data() -> str:
    global cached_value, last_request, first_run

    try:
        current_time = arrow.now(TZ_GE)

        if first_run or current_time > last_request.shift(hours=time_shift):
            data = requests.get(url).json()["data"]["current"]["pollution"]["aqius"]
            cached_value = data
            last_request = arrow.now(TZ_GE)
            first_run = False
            result = data
        else:
            result = cached_value
    except:
        result = cached_value

    aqi_type = get_usaqi_description(cached_value)
    return f"<b>Now in Batumi AQI:</b> {result} <i>{AQI.colors[aqi_type]}</i>"


def get_description() -> str:
    aqi_type = get_usaqi_description(cached_value)
    return f"<b>Description for AQI <i>{cached_value}</i> {AQI.colors[aqi_type]}:</b> \n<i>{aqi_type.value}</i>"
