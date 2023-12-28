import tkinter as tk
from tkinter import simpledialog
import module
import main

def read_config(file_path):
    config = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            config[key] = value
    return config

config = read_config('config.txt')
api_key = config.get('api_key', 'test')

def run_gui():
    def fetch_and_display():
        city = city_entry.get()
        unit = 'metric' if temp_var.get() == 1 else 'imperial'
        forecast = forecast_var.get() == 1
        choice = '3' if historical_var.get() == 1 else ('2' if forecast else '1')

        if choice == '1':
            result = get_weather_with_cache(city, api_key, unit)
        elif choice == '2':
            result = get_weather_with_cache(city, api_key, unit, True)
        elif choice == '3':
            result = get_historical_weather(city, api_key, unit)

        result_label.config(text=result)

    root = tk.Tk()
    root.title("Weather App")

    city_entry = tk.Entry(root, width=20)
    city_entry.pack()

    temp_var = tk.IntVar(value=1)
    tk.Radiobutton(root, text="Celsius", variable=temp_var, value=1).pack()
    tk.Radiobutton(root, text="Fahrenheit", variable=temp_var, value=2).pack()

    forecast_var = tk.IntVar()
    tk.Checkbutton(root, text="5-Day Forecast", variable=forecast_var).pack()

    historical_var = tk.IntVar()
    tk.Checkbutton(root, text="Historical Weather", variable=historical_var).pack()

    tk.Button(root, text="Get Weather", command=fetch_and_display).pack()

    result_label = tk.Label(root, text="", justify=tk.LEFT)
    result_label.pack()

    root.mainloop()

if __name__ == "__main__":
    run_gui()
