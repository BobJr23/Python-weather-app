import PySimpleGUI as sg
import requests
from weather import (
    get_weather,
    get_forecast,
    apiKey,
    get_saved_locations,
    save_location,
)

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
                    sg.Text(
                        "",
                        size=(68, 1),
                        background_color=bc,
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
        sg.Image(filename="sun.png", key="-IMAGE-", size=(700, 450)),
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
    [
        sg.Radio("Fahrenheit", "TEMP", default=True, enable_events=True),
        sg.Radio("Celsius", "TEMP", enable_events=True),
    ],
    [
        sg.Button("Get Weather"),
        sg.Button("Get Forecast"),
        sg.InputText("3", tooltip="Number of days", key="DAYS", size=(3, 1)),
    ],
    [
        sg.Multiline(
            size=(50, 8),
            key="-WEATHER-",
            no_scrollbar=True,
            expand_x=True,
            # background_color=sg.theme_background_color(),
            # text_color="white",
        )
    ],
    [
        sg.Listbox(
            values=get_saved_locations(),
            size=(30, 4),
            key="FAVORITES",
            enable_events=True,
            expand_x=True,
            sbar_width=1,
            sbar_arrow_width=1,
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
    measure = "f"
    while True:
        event, values = window.read()
        print(event, values)
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == 0:
            measure = "f"
        if event == 1:
            measure = "c"
        if event == "Get Weather":
            location = values["-LOCATION-"]
            result = get_weather(location, measure)
            window["-WEATHER-"].update(result)
        if event == "Get Forecast":
            location = values["-LOCATION-"]
            result = get_forecast(location, measure, values["DAYS"])
            window["-WEATHER-"].update(result)
        if event == "FAVORITES":
            window["-WEATHER-"].update(get_weather(values["FAVORITES"][0]))
            window["-LOCATION-"].update(values["FAVORITES"][0])
        if event == "SHOWKEY":
            print(window["SHOWKEY"].get())
            window["API_KEY"].update(password_char="")
        if event == "SAVELOCATION":
            save_location(values["-LOCATION-"])
            window["FAVORITES"].update(get_saved_locations())
        if event == "LOAD":
            window["FAVORITES"].update(get_saved_locations())

    window.close()


if __name__ == "__main__":
    main()
