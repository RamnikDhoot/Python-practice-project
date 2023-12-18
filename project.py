from platform import platform # just import platform does not work
from platform import machine
from platform import processor
from platform import system
from platform import version
from platform import python_implementation, python_version_tuple
import os
import requests
from datetime import datetime

def get_weather(city, api_key, unit='metric'):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    unit_str = '°C' if unit == 'metric' else '°F'
    complete_url = f"{base_url}appid={api_key}&q={city}&units={unit}"

    try:
        response = requests.get(complete_url)
        weather_data = response.json()

        if weather_data['cod'] != 404:
            main_data = weather_data['main']
            temperature = main_data['temp']
            pressure = main_data['pressure']
            humidity = main_data['humidity']
            weather_description = weather_data['weather'][0]['description']
            wind_speed = weather_data['wind']['speed']
            sunrise_time = datetime.fromtimestamp(weather_data['sys']['sunrise']).strftime('%H:%M:%S')
            sunset_time = datetime.fromtimestamp(weather_data['sys']['sunset']).strftime('%H:%M:%S')

            weather_report = (f"Temperature: {temperature:.2f}{unit_str}\n"
                              f"Atmospheric Pressure: {pressure} hPa\n"
                              f"Humidity: {humidity}%\n"
                              f"Description: {weather_description.capitalize()}\n"
                              f"Wind Speed: {wind_speed} m/s\n"
                              f"Sunrise: {sunrise_time}\n"
                              f"Sunset: {sunset_time}")
        else:
            weather_report = "City Not Found!"

        return weather_report

    except requests.RequestException as e:
        return f"Error retrieving weather data: {e}"

def get_weather_forecast(city, api_key, unit='metric'):
    base_url = "http://api.openweathermap.org/data/2.5/forecast?"
    unit_str = '°C' if unit == 'metric' else '°F'
    complete_url = f"{base_url}appid={api_key}&q={city}&units={unit}"

    try:
        response = requests.get(complete_url)
        forecast_data = response.json()

        if forecast_data['cod'] != "404":
            forecast_report = "5-Day Weather Forecast:\n"
            for item in forecast_data['list']:
                date_time = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d %H:%M:%S')
                temperature = item['main']['temp']
                description = item['weather'][0]['description']
                forecast_report += (f"{date_time}: Temp: {temperature:.2f}{unit_str}, "
                                    f"Description: {description.capitalize()}\n")
        else:
            forecast_report = "City Not Found!"

        return forecast_report

    except requests.RequestException as e:
        return f"Error retrieving weather forecast: {e}"

def main():
    api_key = "test"
    city = input("Enter city name: ")
    unit = input("Choose temperature unit - Celsius (C) or Fahrenheit (F): ").lower()
    unit = 'metric' if unit == 'c' else 'imperial'

    choice = input("Choose option: 1. Current Weather 2. 5-Day Forecast\n")

    if choice == '1':
        print("\nCurrent Weather Report:")
        print(get_current_weather(city, api_key, unit))
    elif choice == '2':
        print("\nWeather Forecast:")
        print(get_weather_forecast(city, api_key, unit))
    else:
        print("Invalid choice. Please select 1 or 2.")

if __name__ == "__main__":
    main()








dir(os)
#show you a list of the entities contained inside an imported module

print("test")
# platform(aliased = False, terse = False)
# aliased → when set to True (or any non-zero value) it may cause the function to present the alternative underlying layer names instead of the common ones;
# terse → when set to True (or any non-zero value) it may convince the function to present a briefer form of the result (if possible)

print(machine())
#AMD64

print(platform())
#Windows-10-10.0.22621-SP0

print(platform(1))
#Windows-10-10.0.22621-SP0

print(platform(0, 1))
#Windows-10

print(processor())
#AMD64 Family 23 Model 104 Stepping 1, AuthenticAMD

print(system())
#Windows

print(version())
#10.0.22621

print(python_implementation())
for atr in python_version_tuple():
    print(atr)


