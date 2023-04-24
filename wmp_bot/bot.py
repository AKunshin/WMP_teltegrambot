import asyncio
import logging
import os
import requests
import datetime
import pytz
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.filters import Text
from dotenv import load_dotenv


load_dotenv()

timezone = pytz.timezone("Europe/Moscow")
TOKEN = os.getenv("TOKEN")
OPEN_WEATHER_TOKEN = os.getenv("OPEN_WEATHER_TOKEN")

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=TOKEN, parse_mode="HTML")
# Диспетчер
dp = Dispatcher()


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [
            types.KeyboardButton(
                text="В каком городе вы хотите узнать погоду?"),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите желаемое действие..."
    )
    await message.answer(
        f"Здравствуйте, <b>{message.from_user.full_name}!</b>",
        reply_markup=keyboard
    )

# Хэндлер на команду /weather


@dp.message()
async def cmd_weather(message: types.Message):
    # await message.answer("В каком городе вы хотите узнать погоду?")

    token = OPEN_WEATHER_TOKEN

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
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&lang=ru&units=metric&appid={token}"
        )
        data = r.json()

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

        await message.reply(
            f"***{timezone.localize(datetime.datetime.now()).strftime('%d-%m-%Y %H:%M')}*** \
            \nПогода в городе {city_name} сейчас такая: {wd} \
            \nТемпература воздуха: {temp}C°, ощущается как: {temp_feels_like}C° \
            \nВлажность: {humidity}% Давление: {pressure} мм.рт.ст\
            \nРассвет: {sunrise} \nЗакат: {sunset}"
        )
    except:
        # except Exception as e:
        # print(e)
        await message.reply("Проверьте название города")


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
