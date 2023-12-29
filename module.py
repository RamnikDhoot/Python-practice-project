

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
    
def is_valid_city(city):
    return city.isalpha()

def is_valid_choice(choice):
    return choice in ['1', '2']

def get_historical_weather(city, api_key, unit='metric'):
    print("Fetching historical weather data is not implemented yet.")
    return "Historical Weather Data"

def main():
    api_key = "YOUR_API_KEY"  # Replace with your actual API key
    while True:
        city = input("Enter city name (or 'exit' to quit): ")
        if city.lower() == 'exit':
            break
        if not is_valid_city(city):
            print("Invalid city name. Please try again.")
            continue

        unit = input("Choose temperature unit - Celsius (C) or Fahrenheit (F): ").lower()
        unit = 'metric' if unit == 'c' else 'imperial'

        choice = input("Choose option: 1. Current Weather 2. 5-Day Forecast 3. Historical Weather\n")

        if not is_valid_choice(choice):
            print("Invalid choice. Please select 1, 2, or 3.")
            continue

        if choice == '1':
            print("\nCurrent Weather Report:")
            print(get_weather_with_cache(city, api_key, unit))
        elif choice == '2':
            print("\nWeather Forecast:")
            print(get_weather_with_cache(city, api_key, unit, True))
        elif choice == '3':
            print("\nHistorical Weather Data:")
            print(get_historical_weather(city, api_key, unit))

if __name__ == "__main__":
    refresh_thread = threading.Thread(target=refresh_weather, daemon=True)
    refresh_thread.start()
    root.mainloop()

