import PySimpleGUI as sg
import requests
from dotenv import load_dotenv
import os

load_dotenv()
apiKey = os.getenv('API_KEY')

def get_weather(location):
    response = requests.get(f'http://api.weatherapi.com/v1/current.json?key={apiKey}&q={location}')
    if response.status_code == 200:
        weather_data = response.json()
        weather_info = f"Location: {weather_data['location']['name']}, {weather_data['location']['country']}\n" \
                       f"Temperature: {weather_data['current']['temp_c']}°C\n" \
                       f"Condition: {weather_data['current']['condition']['text']}"
        return weather_info
    else:
        return 'Error fetching weather data'

def get_location():
    response = requests.get(f'http://ip-api.com/json/?fields=city,query,regionName,country')
    if response.status_code == 200:
        location_data = response.json()
        return f"{location_data['city']}, {location_data['regionName']}, {location_data['country']}"
    else:
        return 'Error fetching location data'

layout = [
    [sg.Text('Enter Location:'), sg.InputText(key='-LOCATION-', default_text=get_location())],
    [sg.Button('Fetch Weather')],
    [sg.Multiline('', size=(40, 40), key='-WEATHER-')]
]


# Create the window
window = sg.Window('BobJr Weather App', layout)

def main():
    window.read()
    location = get_location()
    window['-LOCATION-'].update(location)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == 'Fetch Weather':
            location = values['-LOCATION-']

            result = get_weather(location)
            window['-WEATHER-'].update(result)

    # Close the window
    window.close()

if __name__ == '__main__':
    main()