import requests
import datetime

WEATHER_API_KEY = "137f14bfa0d3400a8f9183700251404"
city = "Москва"
# url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&lang=ru"
# response = requests.get(url)
# current_weather_data = response.json()

url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={city}&days=14&lang=ru"
response = requests.get(url)
forecast_weather_data = response.json()

# url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={city}&days=1&lang=ru"
# response = requests.get(url)
# hourly_forecast_weather_data = response.json()["forecast"]["forecastday"][0]["hour"]

print(forecast_weather_data)

# print(datetime.datetime.now().hour)