#!/usr/bin/env/python3

# version = 0.1
# author = Ilya Temerev
# email = kidmoto@yandex.ru

from config import TOKEN
import main

from aiogram import Bot, Dispatcher, executor, types


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


def save_text(message):
    with open('temp.txt', 'w') as file:
        file.write(message)


@dp.message_handler()
async def report(message: types.Message):
    save_text(message.text)

    await message.answer('Сообщение принято, готовлю файл.')

    report = main.UserData()
    report.write_docx()

    await message.answer_document(open('temp.docx', 'rb'))


if __name__ == '__main__':
    executor.start_polling(dp)
