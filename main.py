import PySimpleGUI as sg
import requests
from PIL import Image, ImageEnhance
import io
import sys
import os
from weather import (
    get_weather,
    get_forecast,
    api_key,
    get_saved_locations,
    save_location,
    resource_path,
)

# AI script for theme building
PRIMARY_COLOR = "#1e88e5"
SECONDARY_COLOR = "#64b5f6"
BACKGROUND_COLOR = "#f5f5f5"
TEXT_COLOR = "#212121"

sg.theme_add_new(
    "WeatherApp",
    {
        "BACKGROUND": BACKGROUND_COLOR,
        "TEXT": TEXT_COLOR,
        "INPUT": "#FFFFFF",
        "TEXT_INPUT": "#000000",
        "SCROLL": "#c7e78b",
        "BUTTON": ("white", PRIMARY_COLOR),
        "PROGRESS": ("#01826B", "#D0D0D0"),
        "BORDER": 1,
        "SLIDER_DEPTH": 0,
        "PROGRESS_DEPTH": 0,
    },
)

sg.theme("WeatherApp")
#############################################


def get_location():
    response = requests.get(
        f"http://ip-api.com/json/?fields=city,query,regionName,country"
    )
    if response.status_code == 200:
        location_data = response.json()
        return f"{location_data['city']}, {location_data['regionName']}, {location_data['country']}"
    else:
        return "Error fetching location"


def darken_image(path):
    path = resource_path(path)
    bg_image = Image.open(path)
    enhancer = ImageEnhance.Brightness(bg_image)
    bg_image = enhancer.enhance(0.5).resize((660, 470))
    img_bytes = io.BytesIO()
    bg_image.save(img_bytes, format="PNG")
    return img_bytes.getvalue()


# modified from PySimpleGUI cookbook
def custom_title_bar(title):
    return [
        sg.Col(
            [
                [sg.Text(title, font=("Helvetica", 12, "bold"), pad=(10, 5))],
            ],
            pad=(0, 0),
        ),
        sg.Col(
            [
                [
                    sg.Button("⚙️", key="-SETTINGS-", border_width=0),
                    sg.Button("✖", key="Exit", border_width=0),
                ],
            ],
            element_justification="r",
            expand_x=True,
            pad=(0, 0),
        ),
    ]


#############################################

layout = [
    custom_title_bar("Weather App"),
    [sg.Text("Enter location:", font=("Helvetica", 14))],
    [
        sg.Input(
            get_location(), key="-LOCATION-", size=(30, 1), font=("Helvetica", 12)
        ),
        sg.Button("🔍", key="-SEARCH-", border_width=0),
    ],
    [
        sg.Frame(
            "Current Weather",
            [
                [
                    sg.Multiline(
                        "", key="-WEATHER-", size=(40, 5), font=("Helvetica", 12)
                    )
                ],
            ],
            font=("Helvetica", 12, "bold"),
        )
    ],
    [
        sg.Frame(
            "Forecast",
            [
                [
                    sg.Text("Days:", font=("Helvetica", 12)),
                    sg.Input("3", key="-DAYS-", size=(3, 1)),
                    sg.Button("Get Forecast", key="-FORECAST-", border_width=0),
                ]
            ],
            font=("Helvetica", 12, "bold"),
        )
    ],
    [
        sg.Frame(
            "Favorites",
            [
                [
                    sg.Listbox(
                        values=get_saved_locations(),
                        size=(40, 4),
                        key="-FAVORITES-",
                        enable_events=True,
                        font=("Helvetica", 12),
                    )
                ],
                [
                    sg.Button("Add to Favorites", key="-ADD_FAV-", border_width=0),
                ],
            ],
            font=("Helvetica", 12, "bold"),
        )
    ],
    [
        sg.Text("API Key:", font=("Helvetica", 12)),
        sg.Input(api_key, key="-API_KEY-", password_char="*"),
        sg.Button("👁️", key="-SHOW_KEY-", border_width=0),
        sg.Button("Save Key", key="-SAVE_KEY-", border_width=0),
    ],
]

window = sg.Window(
    "Weather App", layout, finalize=True, no_titlebar=True, grab_anywhere=True
)


window.keep_on_top_set()


def main():
    measure = "f"
    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, "Exit"):
            break
        elif event == "-SEARCH-":
            location = values["-LOCATION-"]
            result = get_weather(location, measure, APIKEY=values["-API_KEY-"])
            window["-WEATHER-"].update(result)
        elif event == "-FORECAST-":
            location = values["-LOCATION-"]
            result = get_forecast(
                location, measure, values["-DAYS-"], values["-API_KEY-"]
            )
            window["-WEATHER-"].update(result)
        elif event == "-ADD_FAV-":
            save_location(values["-LOCATION-"])
            window["-FAVORITES-"].update(get_saved_locations())

        elif event == "-FAVORITES-":
            if values["-FAVORITES-"]:
                window["-LOCATION-"].update(values["-FAVORITES-"][0])
                result = get_weather(
                    values["-FAVORITES-"][0], measure, APIKEY=values["-API_KEY-"]
                )
                window["-WEATHER-"].update(result)
        elif event == "-SHOW_KEY-":
            window["-API_KEY-"].update(
                password_char="" if window["-API_KEY-"].PasswordCharacter else "*"
            )
        elif event == "-SAVE_KEY-":
            with open(".env", "w") as file:
                file.write(f"API_KEY={values['-API_KEY-']}\n")
        elif event == "-SETTINGS-":

            new_measure = sg.popup_get_text(
                "Enter temperature unit (f/c):", default_text=measure, keep_on_top=True
            )
            if new_measure in ["f", "c"]:
                measure = new_measure

    window.close()


if __name__ == "__main__":
    main()
