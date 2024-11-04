import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests

# Replace 'your_api_key_here' with your actual OpenWeatherMap API key
API_KEY = '6e178561871e88e085bdd46d3ea1117f'
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

def get_weather(location):
    """Fetch the weather data for the specified location and update the UI."""
    params = {
        'q': location,
        'appid': API_KEY,
        'units': 'metric'
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        city = data['name']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        description = data['weather'][0]['description']
        
        result = f"Weather in {city}:\nTemperature: {temperature}°C\nHumidity: {humidity}%\nConditions: {description.capitalize()}"
        result_label.config(text=result)
    except requests.exceptions.HTTPError as http_err:
        messagebox.showerror("HTTP Error", f"Could not retrieve data. HTTP Error: {http_err}")
    except requests.exceptions.RequestException as err:
        messagebox.showerror("Error", f"Could not retrieve data: {err}")
    except KeyError:
        messagebox.showerror("Invalid Location", "Please enter a valid city or ZIP code.")

def on_search():
    """Handle the search button click event."""
    location = location_entry.get().strip()
    if location:
        get_weather(location)
    else:
        messagebox.showwarning("Input Error", "Please enter a valid location.")

# Set up the main window
root = tk.Tk()
root.title("Weather App")
root.geometry("500x550")
root.configure(bg="powder blue")

# Outer frame for border effect in lavender
border_frame = tk.Frame(root, bg="#E6E6FA", bd=4, relief="groove")
border_frame.pack(padx=10, pady=10, fill="both", expand=True)

# Inner frame to hold the content, keeping background "powder blue"
content_frame = tk.Frame(border_frame, bg="powder blue")
content_frame.pack(padx=10, pady=10, fill="both", expand=True)

# Load and display an image at the top of the app
try:
    image = Image.open("weathericon.png")
    image = image.resize((100, 100))
    photo = ImageTk.PhotoImage(image)
    img_label = tk.Label(content_frame, image=photo, bg="powder blue")
    img_label.pack(pady=5)
except FileNotFoundError:
    print("Weather icon image file not found. Make sure 'weather_icon.png' is in the same directory.")

# Create and place the UI elements with updated fonts and colors
title_label = tk.Label(content_frame, text="Weather App", font=("Arial", 30, "bold"), bg="powder blue")
title_label.pack(pady=10)

location_label = tk.Label(content_frame, text="Enter city or ZIP code:", font=("Arial", 16), bg="powder blue")
location_label.pack()

location_entry = tk.Entry(content_frame, width=30, font=("Arial", 14))
location_entry.pack(pady=5)

search_button = tk.Button(content_frame, text="Search", command=on_search, font=("Arial", 14), bg="light gray")
search_button.pack(pady=10)

# Result label within the content frame
result_label = tk.Label(content_frame, text="", font=("Arial", 14), bg="powder blue", justify="left")
result_label.pack(pady=20)

# Run the application
root.mainloop()
