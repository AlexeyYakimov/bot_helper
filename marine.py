import arrow
import requests

from token_storage import get_stormglass_token

TZ = 'Asia/Tbilisi'
TZ_UTC = 'UTC'

temp = {}
prev_run_time = arrow.now(TZ).floor('day')
shift_time = 2
can_do_request = True

url = 'https://api.stormglass.io/v2/weather/point'
lat = 41.6410
lng = 41.6142


def get_data_message() -> str:
    return convert_data_to_str(windowed_data())


def windowed_data() -> dict:
    start_time = arrow.now(TZ).floor('hours').datetime
    end_time = arrow.now(TZ).floor('hours').shift(hours=shift_time).datetime
    data = get_data()['hours']
    window_dict = {'hours': []}
    hour_list = []

    for day in data:
        time = arrow.get(day['time']).to(TZ).datetime
        if start_time.timestamp() <= time.timestamp() <= end_time.timestamp():
            hour_list.append(day)

    window_dict['hours'] = hour_list
    return window_dict


def get_data() -> dict:
    global prev_run_time, temp, can_do_request
    current_time = arrow.now(TZ)

    try:
        meta_data = temp['meta']
        if meta_data['requestCount'] <= meta_data['dailyQuota']:
            can_do_request = True
        else:
            can_do_request = False
    except:
        can_do_request = False

    run = current_time.timestamp() > prev_run_time.shift(hours=shift_time).timestamp() and can_do_request
    if run or len(temp) == 0:
        start_time = arrow.now(tz=TZ).floor('day').to(TZ_UTC).timestamp()
        end_time = arrow.now(tz=TZ).ceil('day').to(TZ_UTC).timestamp()

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
                    'Authorization': get_stormglass_token()
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

    return response


def convert_data_to_str(data: dict) -> str:
    try:
        hours_list = data['hours']
        res_list = []

        for day_dict in hours_list:
            time = arrow.get(day_dict['time']).to(TZ).datetime.strftime('%H:%M')
            res_list.append(f"On: {time}")
            wave_height = day_dict['waveHeight']['sg']
            res_list.append(f"Wave height: {wave_height}m")
            air_temp = day_dict['airTemperature']['sg']
            res_list.append(f"Air temp: {int(air_temp)} C˚")
            water_temp = day_dict['waterTemperature']['sg']
            res_list.append(f"Water temp: {int(water_temp)} C˚")
            cloud_cover = day_dict['cloudCover']['sg']
            res_list.append(f"Cloud cover: {cloud_cover}")
            humidity = day_dict['humidity']['sg']
            res_list.append(f"Humidity: {int(humidity)}%")
            pressure = day_dict['pressure']['sg']
            mm_hg = 0.75006375541921
            p = pressure * mm_hg
            res_list.append(f"Pressure: {int(p)} mmHG")
            res_list.append("============================")

        result = '\n'.join(res_list)
        result += f"\nLast update time: {prev_run_time.shift(hours=-shift_time).datetime.strftime('%H:%M')}"
        return result
    except:
        return "Some thing went wrong!"
