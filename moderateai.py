import os
import telebot
import requests
import logging
from dotenv import load_dotenv
from geopy.geocoders import Nominatim

load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')
WEATHER_TOKEN = os.environ.get('WEATHER_TOKEN')
POLLING_TIMEOUT = None

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Hello Padwan, what do you want to search for?')

@bot.message_handler(commands=['weather'])
def send_weather(message):
    location = 'Enter a Location: '
    sent_message = bot.send_message(message.chat.id, location, parse_mode='Markdown')
    bot.register_next_step_handler(sent_message, fetch_weather)
    return location

def location_handler(message):
    geolocator = Nominatim(user_agent="weather_bot")
    location = geolocator.geocode(message.text)
    if location:
        return location.latitude, location.longitude
    else:
        return "Loc not found"
+
def fetch_weather(message):
    lat, lon = location_handler(message)
    if lat and lon:
        api_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_TOKEN}"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            weather = data['weather'][0]['description']
            temp = data['main']['temp']
            bot.send_message(message.chat.id, f"Weather: {weather}\nTemperature: {temp}°C")
        else:
            bot.send_message(message.chat.id, "Failed to fetch weather data")

    else:
        bot.send_message(message.chat.id, "Invalid location")

bot.infinity_polling()