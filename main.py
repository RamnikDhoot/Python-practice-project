import module
#When a module is imported, its contents are implicitly executed by Python. It gives the module the chance to initialize some of its internal aspects

import requests
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

def fetch_weather(city, api_key, unit, forecast=False):
    base_url = "http://api.openweathermap.org/data/2.5/"
    url_type = "forecast" if forecast else "weather"
    unit_str = '°C' if unit == 'metric' else '°F'
    complete_url = f"{base_url}{url_type}?appid={api_key}&q={city}&units={unit}"

    try:
        response = requests.get(complete_url)
        data = response.json()

        if data['cod'] != "404":
            if forecast:
                report = "5-Day Weather Forecast:\n"
                for item in data['list']:
                    date_time = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d %H:%M:%S')
                    temperature = item['main']['temp']
                    description = item['weather'][0]['description']
                    report += (f"{date_time}: Temp: {temperature:.2f}{unit_str}, "
                               f"Description: {description.capitalize()}\n")
            else:
                main_data = data['main']
                temperature = main_data['temp']
                pressure = main_data['pressure']
                humidity = main_data['humidity']
                description = data['weather'][0]['description']
                report = (f"Temperature: {temperature:.2f}{unit_str}\n"
                          f"Atmospheric Pressure: {pressure} hPa\n"
                          f"Humidity: {humidity}%\n"
                          f"Description: {description.capitalize()}")
        else:
            report = "City Not Found!"

        return report

    except requests.RequestException as e:
        return f"Error: {e}"

def display_weather():
    city = city_entry.get()
    unit = 'metric' if var.get() == 1 else 'imperial'
    forecast = forecast_var.get() == 1
    weather_report = fetch_weather(city, "YOUR_API_KEY", unit, forecast)
    result_label.config(text=weather_report)

# GUI setup
root = tk.Tk()
root.title("Weather App")

# City entry
tk.Label(root, text="City:").pack()
city_entry = tk.Entry(root)
city_entry.pack()

# Temperature unit radio buttons
var = tk.IntVar()
var.set(1)
tk.Radiobutton(root, text="Celsius", variable=var, value=1).pack()
tk.Radiobutton(root, text="Fahrenheit", variable=var, value=2).pack()

# Forecast checkbox
forecast_var = tk.IntVar()
tk.Checkbutton(root, text="5-Day Forecast", variable=forecast_var).pack()

# Submit button
tk.Button(root, text="Get Weather", command=display_weather).pack()

# Result label
result_label = tk.Label(root, text="", justify=tk.LEFT)
result_label.pack()

# Run the application
root.mainloop()
