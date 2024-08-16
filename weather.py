import requests
from dotenv import load_dotenv
import os

load_dotenv()
apiKey = os.getenv("API_KEY")


def get_weather(location, measure="f"):
    response = requests.get(
        f"http://api.weatherapi.com/v1/current.json?key={apiKey}&q={location}"
    )
    if response.status_code == 200:
        weather_data = response.json()
        weather_info = (
            f"Location: {weather_data['location']['name']}, {weather_data['location']['country']}\n"
            f"Temperature: {weather_data['current']['temp_'+measure]}°{measure.upper()}\n"
            f"Feels Like: {weather_data['current']['feelslike_'+measure]}°{measure.upper()}\n"
            f"Condition: {weather_data['current']['condition']['text']}"
        )
        return weather_info
    else:
        return "Error fetching weather stuff"


def get_forecast(location, measure="f", days="3"):
    response = requests.get(
        f"http://api.weatherapi.com/v1/forecast.json?key={apiKey}&q={location}&days="
        + days
    )
    if response.status_code == 200:
        forecast_data = response.json()
        forecast_info = f"Location: {forecast_data['location']['name']}, {forecast_data['location']['country']}\n"
        for day in forecast_data["forecast"]["forecastday"]:
            forecast_info += (
                f"Date: {day['date']}\n"
                f"Max Temp: {day['day']['maxtemp_'+measure]}°{measure.upper()}\n"
                f"Min Temp: {day['day']['mintemp_'+measure]}°{measure.upper()}\n"
                f"Condition: {day['day']['condition']['text']}\n\n"
            )
        return forecast_info
    else:
        return "Error fetching forecast stuff"


def get_saved_locations():
    with open("locations.txt", "r") as file:
        locations = file.readlines()
        file.close()
    return locations


def save_location(location):
    with open("locations.txt", "a") as file:
        file.write(location + "\n")
        file.close()


if __name__ == "__main__":
    print(get_weather("New York"))
    print(get_forecast("New York"))
