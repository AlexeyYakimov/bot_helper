from enum import Enum


class AQI:
    class Quality(Enum):
        GREEN = "Air quality is satisfactory, and air pollution poses little or no risk."
        YELLOW = "Air quality is acceptable. However, there may be a risk for some people," \
                 " particularly those who are unusually sensitive to air pollution."
        ORANGE = "Members of sensitive groups may experience health effects." \
                 " The general public is less likely to be affected."
        RED = "Some members of the general public may experience health effects; " \
              "members of sensitive groups may experience more serious health effects."
        PURPLE = "Health alert: The risk of health effects is increased for everyone."
        MAROON = "Health warning of emergency conditions: everyone is more likely to be affected."

        def __str__(self):
            return f"{self.name.lower().capitalize()}"

    ranges = {
        Quality.GREEN: range(0, 51),
        Quality.YELLOW: range(51, 101),
        Quality.ORANGE: range(101, 151),
        Quality.RED: range(151, 201),
        Quality.PURPLE: range(201, 301),
        Quality.MAROON: range(301, 2000)
    }

    colors = {
        Quality.GREEN: "🟢",
        Quality.YELLOW: "🟡",
        Quality.ORANGE: "🟠",
        Quality.RED: "🔴",
        Quality.PURPLE: "🟣",
        Quality.MAROON: "🟤",
    }


def get_usaqi_description(aqi: int) -> AQI.Quality:
    if aqi in AQI.ranges[AQI.Quality.GREEN]:
        result = AQI.Quality.GREEN
    elif aqi in AQI.ranges[AQI.Quality.YELLOW]:
        result = AQI.Quality.YELLOW
    elif aqi in AQI.ranges[AQI.Quality.ORANGE]:
        result = AQI.Quality.ORANGE
    elif aqi in AQI.ranges[AQI.Quality.RED]:
        result = AQI.Quality.RED
    elif aqi in AQI.ranges[AQI.Quality.PURPLE]:
        result = AQI.Quality.PURPLE
    else:
        result = AQI.Quality.MAROON

    return result