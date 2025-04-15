import requests

WEATHER_API_KEY = "137f14bfa0d3400a8f9183700251404"
city = "Москва"
url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&lang=ru"
response = requests.get(url)
current_weather_data = response.json()

url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={city}&days=14&lang=ru"
response = requests.get(url)
forecast_weather_data = response.json()

print(list(map(int, current_weather_data["current"]["last_updated"].split()[0].split("-"))))
print(*forecast_weather_data["forecast"]["forecastday"], sep="\n")