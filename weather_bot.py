import datetime
import requests

from config import wether_token, telegram_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=telegram_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_commands(message: types.Message):
    await message.reply("Напиши назву міста і я пришлю тобі погоду")

@dp.message_handler()
async def get_wether(message: types.Message):
    try:
        r = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={wether_token}&units=metric&'
            )
        data = r.json()

        city_name = data["name"]
        temp = data["main"]["temp"]
        pressure = data["main"]["pressure"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        sunrise = str(datetime.datetime.fromtimestamp(data["sys"]["sunrise"]))[11:]
        sunset = str(datetime.datetime.fromtimestamp(data["sys"]["sunset"]))[11:]

        await message.reply(f"Дата: {datetime.datetime.now().strftime('%Y-%m-%d')}\n"
                f"Час: {datetime.datetime.now().strftime('%H:%m')}\n"
                f"Місто: {city_name}\nТемпература: {temp}°C\n"
                f"Тиск: {pressure} р.с.\n"
                f"Вологість: {humidity}%\n"
                f"Вітер: {wind}м.с.\n"
                f"Схід сонця: {sunrise}\n"
                f"Захід сонця: {sunset}\n"
                f"Гарного дня!\n"
        )
    except:
        await message.reply("Ви не вірно ввели назву місто")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
