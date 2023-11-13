import arrow
import requests

import in_memory_db.in_memory_data as tz
from in_memory_db.token_storage import get_token, Token
from weather_service.utils import get_cloud_coverage, map_to_weather_data, get_rounded_time

temp = {}
prev_run_time = arrow.now(tz.TZ_CURRENT).floor('day')
shift_time = 2
can_do_request = True

url = 'https://api.stormglass.io/v2/weather/point'
lat = 41.6410
lng = 41.6142

_hours_key = 'hours'


def get_formatted_tg_message() -> str:
    return convert_data_to_str(get_data_for_three_hours())


def get_current_weather() -> dict:
    data = get_data()[_hours_key]
    result = {}
    for hour in data:
        weather_time = arrow.get(hour['time'])
        current_time = arrow.now(tz.TZ_CURRENT)

        if weather_time.time().hour >= current_time.time().hour and get_rounded_time(weather_time, current_time):
            result = map_to_weather_data(hour)

    return result


def get_data_for_three_hours() -> list:
    start_time = arrow.now(tz.TZ_CURRENT).floor('hours').timestamp()
    end_time = arrow.now(tz.TZ_CURRENT).floor('hours').shift(hours=shift_time).timestamp()
    data = get_data()[_hours_key]

    hour_list = []

    for hour in data:
        time = arrow.get(hour['time']).timestamp()
        if start_time <= time <= end_time:
            hour_list.append(map_to_weather_data(hour))

    return hour_list


def get_data_for_all_day() -> list:
    data = get_data()[_hours_key]
    result = []
    for hour in data:
        result.append(map_to_weather_data(hour))

    return result


def get_data() -> dict:
    global prev_run_time, temp, can_do_request
    current_time = arrow.now(tz.TZ_CURRENT)

    try:
        meta_data = temp['meta']
        if meta_data['requestCount'] <= meta_data['dailyQuota']:
            can_do_request = True
        else:
            can_do_request = False
    except:
        if len(temp) == 0:
            can_do_request = True
        else:
            can_do_request = False

    run = current_time.timestamp() > prev_run_time.shift(hours=shift_time).timestamp() and can_do_request
    if run or len(temp) == 0:
        start_time = arrow.now(tz=tz.TZ_CURRENT).floor('day').to(tz.TZ_UTC).timestamp()
        end_time = arrow.now(tz=tz.TZ_CURRENT).ceil('day').to(tz.TZ_UTC).timestamp()

        try:
            response = requests.get(
                url=url,
                params={
                    'lat': lat,
                    'lng': lng,
                    'params': ','.join(
                        ['waveHeight', 'airTemperature', 'humidity', 'waterTemperature', 'pressure', 'cloudCover']),
                    'start': start_time,
                    'end': end_time
                },
                headers={
                    'Authorization': get_token(Token.STORMGLASS)
                }
            ).json()

            temp = response
            print(response)
            prev_run_time = current_time.shift(hours=shift_time)
            response = temp
        except:
            response = temp
    else:
        response = temp

    for time in response[_hours_key]:
        time_ge = arrow.get(time['time']).to(tz.TZ_CURRENT)
        time['time'] = time_ge.format('YYYY-MM-DD HH:mm:ssZZ')

    return test.data


def convert_data_to_str(data: list) -> str:
    try:
        res_list = []

        for day_dict in data:
            time = arrow.get(day_dict['time']).datetime.strftime('%H:%M')
            res_list.append(f"<b>At: {time}</b>")

            wave_height = day_dict['waveHeight']
            res_list.append(f"🌊 Wave height: {wave_height} m")

            air_temp = day_dict['airTemperature']
            res_list.append(f"🌡️ Air temp: {int(air_temp)} C˚")

            water_temp = day_dict['waterTemperature']
            res_list.append(f"💦 Water temp: {int(water_temp)} C˚")

            cloud_cover = day_dict['cloudCover']
            res_list.append(f"{get_cloud_coverage(int(cloud_cover))} Cloud cover: {int(cloud_cover)}%")

            humidity = day_dict['humidity']
            res_list.append(f"💧 Humidity: {int(humidity)}%")

            pressure = day_dict['pressure']
            mm_hg = 0.75006375541921
            p = pressure * mm_hg

            res_list.append(f"💪 Pressure: {int(p)} mmHG")
            res_list.append("============================")

        result = '\n'.join(res_list)
        result += f"\nLast update time: {prev_run_time.shift(hours=-shift_time).datetime.strftime('%H:%M')}"
        return result
    except:
        return "Some thing went wrong!"
