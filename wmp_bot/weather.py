import os
import requests
import datetime
import pytz
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

OPEN_WEATHER_TOKEN = os.getenv("OPEN_WEATHER_TOKEN")

timezone = pytz.timezone("Europe/Moscow")


def get_weather(city: str, token: str):

    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&lang=ru&units=metric&appid={token}"
        )
        data = r.json()
        # pprint(data)

        city_name = data["name"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Не могу определить погоду в этом городе"

        temp = data["main"]["temp"]
        temp_feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset = datetime.datetime.fromtimestamp(data["sys"]["sunset"])

        print(f"***{timezone.localize(datetime.datetime.now()).strftime('%d-%m-%Y %H:%M')}*** \
              \nПогода в городе {city_name} сейчас такая: {wd} \
              \nТемпература воздуха: {temp}C°, ощущается как: {temp_feels_like}C° \
              \nВлажность: {humidity}% Давление: {pressure} мм.рт.ст\
              \nРассвет: {sunrise} \nЗакат: {sunset}")
        
    except Exception as e:
        print(e)
        print("Проверьте название города")


def main():
    city = input("В каком городе, вы желаете узнать погоду?\n")
    token = OPEN_WEATHER_TOKEN
    get_weather(city, token)


if __name__ == "__main__":
    main()
