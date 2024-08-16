import PySimpleGUI as sg
import requests
from dotenv import load_dotenv
import os

load_dotenv()
apiKey = os.getenv("API_KEY")


def get_weather(location):
    response = requests.get(
        f"http://api.weatherapi.com/v1/current.json?key={apiKey}&q={location}"
    )
    if response.status_code == 200:
        weather_data = response.json()
        weather_info = (
            f"Location: {weather_data['location']['name']}, {weather_data['location']['country']}\n"
            f"Temperature: {weather_data['current']['temp_c']}°C\n"
            f"Condition: {weather_data['current']['condition']['text']}"
        )
        return weather_info
    else:
        return "Error fetching weather stuff"


def get_forecast(location):
    response = requests.get(
        f"http://api.weatherapi.com/v1/forecast.json?key={apiKey}&q={location}&days=3"
    )
    if response.status_code == 200:
        forecast_data = response.json()
        forecast_info = f"Location: {forecast_data['location']['name']}, {forecast_data['location']['country']}\n"
        for day in forecast_data["forecast"]["forecastday"]:
            forecast_info += (
                f"Date: {day['date']}\n"
                f"Max Temp: {day['day']['maxtemp_c']}°C\n"
                f"Min Temp: {day['day']['mintemp_c']}°C\n"
                f"Condition: {day['day']['condition']['text']}\n\n"
            )
        return forecast_info
    else:
        return "Error fetching forecast stuff"


def get_location():
    response = requests.get(
        f"http://ip-api.com/json/?fields=city,query,regionName,country"
    )
    if response.status_code == 200:
        location_data = response.json()
        return f"{location_data['city']}, {location_data['regionName']}, {location_data['country']}"
    else:
        return "Error fetching location stuff"


layout = [
    [
        sg.Text(
            "Weather App",
            font=("Arial", 20),
            background_color="#666666",
            text_color="white",
        ),
        sg.Button("Dark Mode", button_color=("white", "#666666"), key="THEME"),
    ],
    [
        sg.Text("API Key", background_color="#666666", text_color="white"),
        sg.InputText(apiKey, key="API_KEY"),
    ],
    [sg.Button("Save")],
    [
        sg.Text("City", background_color="#666666", text_color="white"),
        sg.InputText("City, Country", key="-LOCATION-"),
    ],
    [sg.Radio("Fahrenheit", "TEMP", default=True), sg.Radio("Celsius", "TEMP")],
    [sg.Button("Get Weather"), sg.Button("Get 3-Day Forecast")],
    [
        sg.Text(
            "Enter a city and click the button to get the weather.",
            background_color="#666666",
            text_color="white",
        )
    ],
    [sg.Text("Favorites", background_color="#666666", text_color="white")],
    [sg.Multiline(size=(35, 20), key="-WEATHER-")],
    [sg.Listbox(values=["boston ma", "new york ny"], size=(30, 4), key="FAVORITES")],
    [sg.Button("Add Favorite Location"), sg.Button("Load Favorite Locations")],
]


# Create the window
window = sg.Window("BobJr Weather App", layout)


def main():
    window.read(timeout=0)
    location = get_location()
    window["-LOCATION-"].update(location)
    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WINDOW_CLOSED:
            break
        if event == "Fetch Weather":
            location = values["-LOCATION-"]

            result = get_weather(location)
            window["-WEATHER-"].update(result)

    window.close()


if __name__ == "__main__":
    main()
