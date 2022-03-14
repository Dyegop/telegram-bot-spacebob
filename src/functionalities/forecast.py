import requests
import json
import logging
import src.base as base
from geopy.geocoders import Nominatim


# LOG
logger = logging.getLogger(__name__)



class Forecast(base.Parameters):
    def __init__(self, lat: str, lon: str):
        super().__init__()
        self.lat = lat
        self.lon = lon
        self._forecast_url = f'https://api.openweathermap.org/data/2.5/weather?lat={self.lat}&lon={self.lon}&units=metric&appid={self.open_weather_token}'

    def request_forecast_data(self):
        try:
            re = requests.get(self._forecast_url)
            data = json.loads(re.text)
            return dict(data.get('weather')[0]), dict(data.get('main')), data["name"]
        except requests.exceptions.HTTPError as err:
            logger.error(f"Request error: {err}")

    def get_city_from_coordinates(self):
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.reverse(f"{self.lat}, {self.lon}")
        address = location.raw['address']
        return address.get('city', '')

    @staticmethod
    def weather_emoji(weather_code):
        """ Return weather icon based on code"""
        # Dictionary that relates weather Unicode emoji with weather condition codes from openWeatherAPI
        weather_emojis = {
            '\U000026A1': [210, 211, 212, 221],
            '\U000026C8': [200, 201, 202, 504, 531],
            '\U0001F329': [230, 231, 232],
            '\U0001F327': [300, 301, 302, 310, 311, 312, 313, 314, 321, 503, 504, 522],
            '\U0001F326': [500, 501, 520, 521],
            '\U0001F328': [511, 611, 612, 613, 615, 616],
            '\U00002744': [600, 601, 602, 620, 621, 622],
            '\U0001F32A': [771, 781],
            '\U0001F32B': [701, 721, 731, 741],
            '\U00002600': [800],
            '\U00002601': [801, 802, 803, 804]
        }
        return [k for k, v in weather_emojis.items() if weather_code in v][0]
