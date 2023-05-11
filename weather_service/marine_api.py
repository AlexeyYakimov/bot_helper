import arrow
import requests

from utils.global_utils import TZ_GE, TZ_UTC
from utils.token_storage import get_token, Token

temp = {'hours':[]}
prev_run_time = arrow.now(TZ_GE).floor('day')
shift_time = 2
can_do_request = True

url = 'https://api.stormglass.io/v2/weather/point'
lat = 41.6410
lng = 41.6142


def get_data_message() -> str:
    return convert_data_to_str(windowed_data())


def windowed_data() -> list:
    start_time = arrow.now(TZ_GE).floor('hours').datetime
    end_time = arrow.now(TZ_GE).floor('hours').shift(hours=shift_time).datetime
    # data = get_data()['hours']
    data = test2['hours']
    hour_list = []

    for day in data:
        time = arrow.get(day['time']).to(TZ_GE).datetime
        if start_time.timestamp() <= time.timestamp() <= end_time.timestamp():
            hour_list.append(map_to_weather_data(day))

    return hour_list


def get_data() -> dict:
    global prev_run_time, temp, can_do_request
    current_time = arrow.now(TZ_GE)

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
        start_time = arrow.now(tz=TZ_GE).floor('day').to(TZ_UTC).timestamp()
        end_time = arrow.now(tz=TZ_GE).ceil('day').to(TZ_UTC).timestamp()

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

    return response


def convert_data_to_str(data: list) -> str:
    try:
        res_list = []

        for day_dict in data:
            time = arrow.get(day_dict['time']).to(TZ_GE).datetime.strftime('%H:%M')
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


def map_to_weather_data(data: dict) -> dict:
    avg_dict = {}
    for k, v in data.items():
        avg_dict[k] = get_avg_value(v)
    return avg_dict


def get_avg_value(data):
    if type(data) is dict:
        values = data.values()
        avg = sum(values) / len(values)
        return round(avg, 2)
    else:
        return data


def get_cloud_coverage(coverage) -> str:

    if 90 <= coverage <= 100:
        cloud_icon = "☁️"
    elif 70 < coverage < 90:
        cloud_icon = "🌥"
    elif 50 < coverage <= 70:
        cloud_icon = "🌥"
    elif 15 < coverage <= 50:
        cloud_icon = "⛅"
    elif 0 < coverage <= 15:
        cloud_icon = "🌤"
    elif coverage == 0:
        cloud_icon = "☀️"

    return cloud_icon

test2 = {'hours': [{'airTemperature': {'dwd': 14.96, 'noaa': 12.71, 'sg': 14.96},
                        'cloudCover': {'dwd': 100.0, 'noaa': 80.7, 'sg': 100.0},
                        'humidity': {'dwd': 86.04, 'noaa': 89.7, 'sg': 86.04},
                        'pressure': {'dwd': 1018.13, 'noaa': 1019.27, 'sg': 1018.13},
                        'time': '2023-05-10T20:00:00+00:00',
                        'waterTemperature': {'meto': 13.52, 'noaa': 13.6, 'sg': 13.52},
                        'waveHeight': {'dwd': 0.19, 'icon': 0.18, 'sg': 0.18}},
                       {'airTemperature': {'dwd': 14.83, 'noaa': 12.48, 'sg': 14.83},
                        'cloudCover': {'dwd': 100.0, 'noaa': 71.5, 'sg': 100.0},
                        'humidity': {'dwd': 88.05, 'noaa': 91.5, 'sg': 88.05},
                        'pressure': {'dwd': 1017.86, 'noaa': 1018.98, 'sg': 1017.86},
                        'time': '2023-05-10T21:00:00+00:00',
                        'waterTemperature': {'meto': 13.48, 'noaa': 13.39, 'sg': 13.48},
                        'waveHeight': {'dwd': 0.19, 'icon': 0.18, 'sg': 0.18}},
                       {'airTemperature': {'dwd': 14.63, 'noaa': 12.47, 'sg': 14.63},
                        'cloudCover': {'dwd': 100.0, 'noaa': 81.0, 'sg': 100.0},
                        'humidity': {'dwd': 90.85, 'noaa': 90.47, 'sg': 90.85},
                        'pressure': {'dwd': 1017.39, 'noaa': 1018.43, 'sg': 1017.39},
                        'time': '2023-05-10T22:00:00+00:00',
                        'waterTemperature': {'meto': 13.45, 'noaa': 13.35, 'sg': 13.45},
                        'waveHeight': {'dwd': 0.2, 'icon': 0.18, 'sg': 0.18}},
                       {'airTemperature': {'dwd': 14.57, 'noaa': 12.47, 'sg': 14.57},
                        'cloudCover': {'dwd': 100.0, 'noaa': 90.5, 'sg': 100.0},
                        'humidity': {'dwd': 92.22, 'noaa': 89.43, 'sg': 92.22},
                        'pressure': {'dwd': 1017.39, 'noaa': 1017.88, 'sg': 1017.39},
                        'time': '2023-05-10T23:00:00+00:00',
                        'waterTemperature': {'meto': 13.41, 'noaa': 13.31, 'sg': 13.41},
                        'waveHeight': {'dwd': 0.21, 'icon': 0.19, 'sg': 0.19}},
                       {'airTemperature': {'dwd': 14.66, 'noaa': 12.46, 'sg': 14.66},
                        'cloudCover': {'dwd': 99.94, 'noaa': 100.0, 'sg': 99.94},
                        'humidity': {'dwd': 89.69, 'noaa': 88.4, 'sg': 89.69},
                        'pressure': {'dwd': 1016.95, 'noaa': 1017.34, 'sg': 1016.95},
                        'time': '2023-05-11T00:00:00+00:00',
                        'waterTemperature': {'meto': 13.4, 'noaa': 13.26, 'sg': 13.4},
                        'waveHeight': {'dwd': 0.23, 'icon': 0.19, 'sg': 0.19}},
                       {'airTemperature': {'dwd': 14.83, 'noaa': 12.48, 'sg': 14.83},
                        'cloudCover': {'dwd': 100.0, 'noaa': 100.0, 'sg': 100.0},
                        'humidity': {'dwd': 86.64, 'noaa': 90.57, 'sg': 86.64},
                        'pressure': {'dwd': 1017.17, 'noaa': 1017.88, 'sg': 1017.17},
                        'time': '2023-05-11T01:00:00+00:00',
                        'waterTemperature': {'meto': 13.39, 'noaa': 13.33, 'sg': 13.39},
                        'waveHeight': {'dwd': 0.24, 'icon': 0.19, 'sg': 0.19}},
                       {'airTemperature': {'dwd': 14.82, 'noaa': 12.49, 'sg': 14.82},
                        'cloudCover': {'dwd': 99.9, 'noaa': 100.0, 'sg': 99.9},
                        'humidity': {'dwd': 82.9, 'noaa': 92.73, 'sg': 82.9},
                        'pressure': {'dwd': 1017.48, 'noaa': 1018.42, 'sg': 1017.48},
                        'time': '2023-05-11T02:00:00+00:00',
                        'waterTemperature': {'meto': 13.39, 'noaa': 13.4, 'sg': 13.39},
                        'waveHeight': {'dwd': 0.26, 'icon': 0.19, 'sg': 0.19}},
                       {'airTemperature': {'dwd': 14.75, 'noaa': 12.51, 'sg': 14.75},
                        'cloudCover': {'dwd': 99.59, 'noaa': 100.0, 'sg': 99.59},
                        'humidity': {'dwd': 82.76, 'noaa': 94.9, 'sg': 82.76},
                        'pressure': {'dwd': 1018.11, 'noaa': 1018.96, 'sg': 1018.11},
                        'time': '2023-05-11T03:00:00+00:00',
                        'waterTemperature': {'meto': 13.38, 'noaa': 13.46, 'sg': 13.38},
                        'waveHeight': {'dwd': 0.28, 'icon': 0.19, 'sg': 0.19}},
                       {'airTemperature': {'dwd': 14.8, 'noaa': 12.62, 'sg': 14.8},
                        'cloudCover': {'dwd': 100.0, 'noaa': 99.1, 'sg': 100.0},
                        'humidity': {'dwd': 87.23, 'noaa': 93.9, 'sg': 87.23},
                        'pressure': {'dwd': 1018.79, 'noaa': 1019.65, 'sg': 1018.79},
                        'time': '2023-05-11T04:00:00+00:00',
                        'waterTemperature': {'meto': 13.38, 'noaa': 13.59, 'sg': 13.38},
                        'waveHeight': {'dwd': 0.28, 'icon': 0.19, 'sg': 0.19}},
                       {'airTemperature': {'dwd': 14.8, 'noaa': 12.74, 'sg': 14.8},
                        'cloudCover': {'dwd': 100.0, 'noaa': 98.2, 'sg': 100.0},
                        'humidity': {'dwd': 88.72, 'noaa': 92.9, 'sg': 88.72},
                        'pressure': {'dwd': 1019.66, 'noaa': 1020.35, 'sg': 1019.66},
                        'time': '2023-05-11T05:00:00+00:00',
                        'waterTemperature': {'meto': 13.37, 'noaa': 13.72, 'sg': 13.37},
                        'waveHeight': {'dwd': 0.29, 'icon': 0.2, 'sg': 0.2}},
                       {'airTemperature': {'dwd': 14.59, 'noaa': 12.85, 'sg': 14.59},
                        'cloudCover': {'dwd': 100.0, 'noaa': 97.3, 'sg': 100.0},
                        'humidity': {'dwd': 87.42, 'noaa': 91.9, 'sg': 87.42},
                        'pressure': {'dwd': 1020.45, 'noaa': 1021.04, 'sg': 1020.45},
                        'time': '2023-05-11T06:00:00+00:00',
                        'waterTemperature': {'meto': 13.48, 'noaa': 13.85, 'sg': 13.48},
                        'waveHeight': {'dwd': 0.29, 'icon': 0.2, 'sg': 0.2}},
                       {'airTemperature': {'dwd': 14.46, 'noaa': 12.86, 'sg': 14.46},
                        'cloudCover': {'dwd': 97.84, 'noaa': 93.0, 'sg': 97.84},
                        'humidity': {'dwd': 89.29, 'noaa': 92.53, 'sg': 89.29},
                        'pressure': {'dwd': 1020.97, 'noaa': 1021.18, 'sg': 1020.97},
                        'time': '2023-05-11T07:00:00+00:00',
                        'waterTemperature': {'meto': 13.72, 'noaa': 14.0, 'sg': 13.72},
                        'waveHeight': {'dwd': 0.28, 'icon': 0.2, 'sg': 0.2}},
                       {'airTemperature': {'dwd': 14.54, 'noaa': 12.88, 'sg': 14.54},
                        'cloudCover': {'dwd': 98.35, 'noaa': 88.7, 'sg': 98.35},
                        'humidity': {'dwd': 87.51, 'noaa': 93.17, 'sg': 87.51},
                        'pressure': {'dwd': 1020.82, 'noaa': 1021.31, 'sg': 1020.82},
                        'time': '2023-05-11T08:00:00+00:00',
                        'waterTemperature': {'meto': 13.95, 'noaa': 14.15, 'sg': 13.95},
                        'waveHeight': {'dwd': 0.28, 'icon': 0.21, 'sg': 0.21}},
                       {'airTemperature': {'dwd': 14.6, 'noaa': 12.89, 'sg': 14.6},
                        'cloudCover': {'dwd': 99.86, 'noaa': 84.4, 'sg': 99.86},
                        'humidity': {'dwd': 86.88, 'noaa': 93.8, 'sg': 86.88},
                        'pressure': {'dwd': 1020.71, 'noaa': 1021.45, 'sg': 1020.71},
                        'time': '2023-05-11T09:00:00+00:00',
                        'waterTemperature': {'meto': 14.16, 'noaa': 14.29, 'sg': 14.16},
                        'waveHeight': {'dwd': 0.28, 'icon': 0.21, 'sg': 0.21}},
                       {'airTemperature': {'dwd': 14.61, 'noaa': 12.95, 'sg': 14.61},
                        'cloudCover': {'dwd': 99.98, 'noaa': 83.27, 'sg': 99.98},
                        'humidity': {'dwd': 86.34, 'noaa': 94.23, 'sg': 86.34},
                        'pressure': {'dwd': 1020.81, 'noaa': 1021.37, 'sg': 1020.81},
                        'time': '2023-05-11T10:00:00+00:00',
                        'waterTemperature': {'meto': 14.37, 'noaa': 14.49, 'sg': 14.37},
                        'waveHeight': {'dwd': 0.29, 'icon': 0.21, 'sg': 0.21}},
                       {'airTemperature': {'dwd': 14.69, 'noaa': 13.0, 'sg': 14.69},
                        'cloudCover': {'dwd': 100.0, 'noaa': 82.13, 'sg': 100.0},
                        'humidity': {'dwd': 84.68, 'noaa': 94.67, 'sg': 84.68},
                        'pressure': {'dwd': 1020.96, 'noaa': 1021.28, 'sg': 1020.96},
                        'time': '2023-05-11T11:00:00+00:00',
                        'waterTemperature': {'meto': 14.56, 'noaa': 14.68, 'sg': 14.56},
                        'waveHeight': {'dwd': 0.29, 'icon': 0.21, 'sg': 0.21}},
                       {'airTemperature': {'dwd': 14.71, 'noaa': 13.05, 'sg': 14.71},
                        'cloudCover': {'dwd': 97.93, 'noaa': 81.0, 'sg': 97.93},
                        'humidity': {'dwd': 83.78, 'noaa': 95.1, 'sg': 83.78},
                        'pressure': {'dwd': 1021.01, 'noaa': 1021.2, 'sg': 1021.01},
                        'time': '2023-05-11T12:00:00+00:00',
                        'waterTemperature': {'meto': 14.63, 'noaa': 14.88, 'sg': 14.63},
                        'waveHeight': {'dwd': 0.29, 'icon': 0.21, 'sg': 0.21}},
                       {'airTemperature': {'dwd': 14.66, 'noaa': 12.96, 'sg': 14.66},
                        'cloudCover': {'dwd': 98.8, 'noaa': 75.4, 'sg': 98.8},
                        'humidity': {'dwd': 84.14, 'noaa': 94.53, 'sg': 84.14},
                        'pressure': {'dwd': 1020.94, 'noaa': 1021.01, 'sg': 1020.94},
                        'time': '2023-05-11T13:00:00+00:00',
                        'waterTemperature': {'meto': 14.58, 'noaa': 14.64, 'sg': 14.58},
                        'waveHeight': {'dwd': 0.29, 'icon': 0.21, 'sg': 0.21}},
                       {'airTemperature': {'dwd': 14.67, 'noaa': 12.87, 'sg': 14.67},
                        'cloudCover': {'dwd': 100.0, 'noaa': 69.8, 'sg': 100.0},
                        'humidity': {'dwd': 86.74, 'noaa': 93.97, 'sg': 86.74},
                        'pressure': {'dwd': 1021.1, 'noaa': 1020.82, 'sg': 1021.1}, 'time': '2023-05-11T14:00:00+00:00',
                        'waterTemperature': {'meto': 14.54, 'noaa': 14.41, 'sg': 14.54},
                        'waveHeight': {'dwd': 0.29, 'icon': 0.22, 'sg': 0.22}},
                       {'airTemperature': {'dwd': 14.59, 'noaa': 12.78, 'sg': 14.59},
                        'cloudCover': {'dwd': 99.94, 'noaa': 64.2, 'sg': 99.94},
                        'humidity': {'dwd': 86.87, 'noaa': 93.4, 'sg': 86.87},
                        'pressure': {'dwd': 1020.76, 'noaa': 1020.63, 'sg': 1020.76},
                        'time': '2023-05-11T15:00:00+00:00',
                        'waterTemperature': {'meto': 14.52, 'noaa': 14.17, 'sg': 14.52},
                        'waveHeight': {'dwd': 0.29, 'icon': 0.22, 'sg': 0.22}},
                       {'airTemperature': {'dwd': 14.59, 'noaa': 12.75, 'sg': 14.59},
                        'cloudCover': {'dwd': 100.0, 'noaa': 73.2, 'sg': 100.0},
                        'humidity': {'dwd': 84.69, 'noaa': 93.13, 'sg': 84.69},
                        'pressure': {'dwd': 1021.09, 'noaa': 1021.02, 'sg': 1021.09},
                        'time': '2023-05-11T16:00:00+00:00',
                        'waterTemperature': {'meto': 14.5, 'noaa': 14.01, 'sg': 14.5},
                        'waveHeight': {'dwd': 0.28, 'icon': 0.22, 'sg': 0.22}},
                       {'airTemperature': {'dwd': 14.69, 'noaa': 12.72, 'sg': 14.69},
                        'cloudCover': {'dwd': 100.0, 'noaa': 82.2, 'sg': 100.0},
                        'humidity': {'dwd': 85.03, 'noaa': 92.87, 'sg': 85.03},
                        'pressure': {'dwd': 1021.13, 'noaa': 1021.42, 'sg': 1021.13},
                        'time': '2023-05-11T17:00:00+00:00',
                        'waterTemperature': {'meto': 14.48, 'noaa': 13.84, 'sg': 14.48},
                        'waveHeight': {'dwd': 0.28, 'icon': 0.22, 'sg': 0.22}},
                       {'airTemperature': {'dwd': 14.61, 'noaa': 12.7, 'sg': 14.61},
                        'cloudCover': {'dwd': 100.0, 'noaa': 91.2, 'sg': 100.0},
                        'humidity': {'dwd': 87.07, 'noaa': 92.6, 'sg': 87.07},
                        'pressure': {'dwd': 1021.3, 'noaa': 1021.82, 'sg': 1021.3}, 'time': '2023-05-11T18:00:00+00:00',
                        'waterTemperature': {'meto': 14.43, 'noaa': 13.68, 'sg': 14.43},
                        'waveHeight': {'dwd': 0.27, 'icon': 0.22, 'sg': 0.22}},
                       {'airTemperature': {'dwd': 14.57, 'noaa': 12.77, 'sg': 14.57},
                        'cloudCover': {'dwd': 100.0, 'noaa': 94.13, 'sg': 100.0},
                        'humidity': {'dwd': 89.09, 'noaa': 92.3, 'sg': 89.09},
                        'pressure': {'dwd': 1021.05, 'noaa': 1020.95, 'sg': 1021.05},
                        'time': '2023-05-11T19:00:00+00:00',
                        'waterTemperature': {'meto': 14.34, 'noaa': 13.71, 'sg': 14.34},
                        'waveHeight': {'dwd': 0.27, 'icon': 0.22, 'sg': 0.22}}],
             'meta': {'cost': 1, 'dailyQuota': 10, 'end': '2023-05-11 19:59', 'lat': 41.641, 'lng': 41.6142,
                      'params': ['waveHeight', 'airTemperature', 'humidity', 'waterTemperature', 'pressure',
                                 'cloudCover'], 'requestCount': 10, 'start': '2023-05-10 20:00'}}