#!/usr/bin/env/python3

# version = 0.1
# author = Ilya Temerev
# email = kidmoto@yandex.ru

from config import TOKEN
import main

from aiogram import Bot, Dispatcher, executor, types


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler()
async def report(message: types.Message):
    await message.answer('Сообщение принято')


if __name__ == '__main__':
    executor.start_polling(dp)

