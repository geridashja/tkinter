from tkinter import *
from tkinter import messagebox
from configparser import ConfigParser
import requests
import os

url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

def get_api():
    config_file = "weather_app/config.ini"
    config = ConfigParser()
    config.read(config_file)
    api_key = config['api_key']['key']
    return api_key


def search():
    city = city_text.get()
    weather = get_infos(city)
    if weather:
        Location["text"] = "{}, {}". format(weather[0], weather[1])
        Image["bitmap"] = "icons/{}.png".format(weather[4])
        Temperature["text"] = "{:.2f}°C, {:.2f}°F".format(weather[2], weather[3])
        Weather["text"] = "{}".format(weather[5])
    else:
        messagebox.showerror("Error", "Cannot find the {}".format(city))


def get_infos(city):
    result = requests.get(url.format(city, get_api()))
    if result:
        json = result.json()
        city = json["name"]
        temp_kelvin = json["main"]["temp"]
        temp_celsius = temp_kelvin - 273.15
        temp_far = (temp_kelvin - 273.15) * 9/5 + 32
        country = json["sys"]["country"]
        icon = json["weather"][0]["icon"]
        weather = json["weather"][0]["main"]
        final = (city, country, temp_celsius, temp_far, icon, weather)
        return final
    else:
        return None


root = Tk()
blank_space = " "
root.title(90*blank_space+"Weather Checker")
root.geometry("700x350")

city_text = StringVar()
city_entry = Entry(root, textvariable=city_text)
city_entry.pack()

Search = Button(root, text="Search Weather", command=search)
Search.pack()

Location = Label(root, text="", font=("bold", 18))
Location.pack(pady=8)

Image = Label(root, bitmap='')
Image.pack()

Temperature = Label(root, text="")
Temperature.pack()

Weather = Label(root, text='')
Weather.pack()

root.mainloop()