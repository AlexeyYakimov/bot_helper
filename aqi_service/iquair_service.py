import requests
import arrow

from aqi_service.aqi_utils import get_usaqi_description
from token_storage import get_iqair_token
from utils import TZ_GE

url = f"https://api.airvisual.com/v2/city?key={get_iqair_token()}&country=Georgia&state=Ajaria&city=Batumi"

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

    return f"<b>Now in Batumi AQI:</b> {result} <i>{get_usaqi_description(cached_value)}</i>"


def get_description() -> str:
    return f"<b>Description for AQI <i>{cached_value}</i>:</b> \n<i>{get_usaqi_description(cached_value).value}</i>"