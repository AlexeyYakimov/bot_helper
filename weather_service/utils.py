def get_rounded_time(start_time, current_time) -> bool:
    t = current_time

    if t.time().minute >= 30:
        t = t.shift(hours=1)

    t = t.floor('hours').time()
    return start_time.time() == t


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
