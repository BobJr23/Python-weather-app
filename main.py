import PySimpleGUI as sg
import requests
from dotenv import load_dotenv
import os

load_dotenv()
apiKey = os.getenv("API_KEY")
sg.Window._move_all_windows = True


# FROM PYSIMPLEGUI DOCS
def title_bar(title, text_color, background_color):
    bc = background_color
    tc = text_color
    font = "Helvetica 12"

    return [
        sg.Col(
            [[sg.T(title, text_color=tc, background_color=bc, font=font, grab=True)]],
            pad=(0, 0),
            background_color=bc,
        ),
        sg.Col(
            [
                [
                    sg.T(
                        "_",
                        text_color=tc,
                        background_color=bc,
                        enable_events=True,
                        font=font,
                        key="-MINIMIZE-",
                    ),
                    sg.Text(
                        "❎",
                        text_color=tc,
                        background_color=bc,
                        font=font,
                        enable_events=True,
                        key="Exit",
                    ),
                ]
            ],
            element_justification="r",
            key="-C-",
            grab=True,
            pad=(0, 0),
            background_color=bc,
        ),
    ]


###


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


bg = [
    [
        sg.Image(filename="cloud.png", key="-IMAGE-"),
    ],
]
window_background = sg.Window(
    "Background",
    bg,
    no_titlebar=True,
    finalize=True,
    margins=(0, 0),
    element_padding=(0, 0),
    grab_anywhere=True,
)


layout = [
    [title_bar("Weather App", "white", "#42526b")],
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
        sg.InputText(apiKey, key="API_KEY", password_char="*"),
        sg.Text(
            "👁️",
            key="SHOWKEY",
            enable_events=True,
        ),
    ],
    [sg.Button("Save")],
    [
        sg.Text("City", background_color="#666666", text_color="white"),
        sg.InputText(get_location(), key="-LOCATION-"),
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
    [sg.Multiline(size=(50, 8), key="-WEATHER-", no_scrollbar=True)],
    [
        sg.Listbox(
            values=["boston ma", "new york ny"],
            size=(30, 4),
            key="FAVORITES",
            enable_events=True,
        )
    ],
    [
        sg.Button("Add Favorite Location", key="SAVELOCATION"),
        sg.Button("Load Favorite Locations", key="LOAD"),
    ],
]


# Create the window
window = sg.Window(
    "BobJr Weather App",
    layout,
    finalize=True,
    transparent_color=sg.theme_background_color(),
    grab_anywhere=True,
    no_titlebar=True,
)
window.keep_on_top_set()
window["-C-"].expand(True, False, False)


def main():
    event, values = window.read(timeout=0)
    window["-WEATHER-"].update(get_weather(values["-LOCATION-"]))
    while True:
        event, values = window.read()
        print(event, values)
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "Get Weather":
            location = values["-LOCATION-"]

            result = get_weather(location)
            window["-WEATHER-"].update(result)
        if event == "FAVORITES":
            window["-WEATHER-"].update(get_weather(values["FAVORITES"][0]))
        if event == "SHOWKEY":
            print(window["SHOWKEY"].get())
            window["API_KEY"].update(password_char="")

    window.close()


if __name__ == "__main__":
    main()
