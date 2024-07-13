import datetime as dt
import requests

def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """
    converts temperature from fahrenheit to celsius
    """
    celsius = (fahrenheit - 32) * 5.0/9.0
    return celsius

def kelvin_to_celsius(kelvin: float) -> float:
    """
    converts temperature from kelvin to celsius
    """
    celsius = kelvin - 273.15
    return celsius

def get_city_lat_lon(city_name: str, api_key: str) -> tuple:
    """
    returns latitude and longitude of a given city
    """
    limit = 1
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit={limit}&appid={api_key}"
    response = requests.get(url).json()
    data = response[0]
    lat = data["lat"]
    lon = data["lon"]
    return lat, lon


def get_city_weather(city_name: str, api_key: str):
    """
    returns json formatted city weather data
    """
    lat, lon = get_city_lat_lon(city_name, api_key)
    BASE_URL = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"
    response = requests.get(BASE_URL).json()
    return response

def get_city_main_weather(city_name: str, api_key: str):
    """
    returns city main weather data
    ex.:
    {"temp": 298.48,
    "feels_like": 298.74,
    "temp_min": 297.56,
    "temp_max": 300.05,
    "pressure": 1015,
    "humidity": 64,
    "sea_level": 1015,
    "grnd_level": 933}

    temperature [Kelvin],
    humidity [%],
    pressure [hPa],
    sea_level - Atmospheric pressure on the sea level, hPa
    grnd_level - Atmospheric pressure on the ground level, hPa

    Returns:
    tuple: (dict, string)
    """
    city_data = get_city_weather(city_name, api_key)
    main_data = city_data["main"]
    date = city_data["dt"]
    return main_data, date

def get_main_weather_description_ue(main_city_data: dict, date: str):
    """
    returns main weather data (dict) with temperatures converted to *C
    and string description of the weather

    Returns:
    tuple: (dict, str)
    """
    temp = kelvin_to_celsius(main_city_data["temp"])
    feels_like = kelvin_to_celsius(main_city_data["feels_like"])
    temp_min = kelvin_to_celsius(main_city_data["temp_min"])
    temp_max = kelvin_to_celsius(main_city_data["temp_max"])
    pressure = main_city_data["pressure"]  #hPa
    humidity = main_city_data["humidity"]  #%
    date = dt.datetime.fromtimestamp(date)
    desc = f"date: {date} -- temperature: {round(temp, 1)}*C; feels like: {round(feels_like, 1)}*C; min temperature: {round(temp_min, 1)}*C; max temperature {round(temp_max)}*C; pressure: {pressure}hPa; humidity: {humidity}%"
    converted = {'temp': temp, 'feels_like': feels_like, 'temp_min': temp_min, 'temp_max': temp_max, 'pressure': pressure, 'humidity': humidity, "date": date}
    return converted, desc





"""
used API: https://openweathermap.org
to receive a response you need a valid api key
anyone can get it by creating an account
"""
api_path = "api.txt"
API_KEY = open(api_path, 'r').read().strip()
city = "Warsaw"


main_data, date = get_city_main_weather(city, API_KEY)
converted_data, description = get_main_weather_description_ue(main_data, date)
print(description)

print(get_city_lat_lon("Różan", API_KEY))






