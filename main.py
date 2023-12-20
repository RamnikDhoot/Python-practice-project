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

    if "Error" in weather_report or "Not Found" in weather_report:
        messagebox.showerror("Error", weather_report)
    else:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, weather_report)

def save_report():
    report = result_text.get(1.0, tk.END)
    if report.strip():
        file = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file:
            with open(file, "w") as file:
                file.write(report)
    else:
        messagebox.showinfo("Info", "No report to save.")

# GUI setup
root = tk.Tk()
root.title("Weather App")
root.geometry("400x500")

# Frame for input fields
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

# City entry
tk.Label(input_frame, text="City:").grid(row=0, column=0, padx=10)
city_entry = tk.Entry(input_frame, width=20)
city_entry.grid(row=0, column=1, padx=10)

# Temperature unit radio buttons
var = tk.IntVar()
var.set(1)
tk.Radiobutton(input_frame, text="Celsius", variable=var, value=1).grid(row=1, column=0)
tk.Radiobutton(input_frame, text="Fahrenheit", variable=var, value=2).grid(row=1, column=1)

# Forecast checkbox
forecast_var = tk.IntVar()
tk.Checkbutton(input_frame, text="5-Day Forecast", variable=forecast_var).grid(row=2, columnspan=2)

# Submit button
tk.Button(root, text="Get Weather", command=display_weather).pack(pady=10)

# Text box for results
result_text = tk.Text(root, height=15, width=45)
result_text.pack(pady=10)

# Save button
tk.Button(root, text="Save Report", command=save_report).pack()

# Run the application
root.mainloop()
