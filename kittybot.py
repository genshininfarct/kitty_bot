# kittybot/kittybot.py
import requests
from telebot import TeleBot, types
#секретим 
import os
from dotenv import load_dotenv
#логи
import logging
#время
import time
from datetime import datetime
import random

load_dotenv()

secret_token = os.getenv('TOKEN')
bot = TeleBot(token=secret_token)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)

#url картинки
URL = 'https://api.thecatapi.com/v1/images/search'

def get_new_image():
    try:
        time.sleep(2)  # Ждем 2 секунды перед запросом
        response = requests.get(URL)
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        new_url = 'https://api.thedogapi.com/v1/images/search'
        response = requests.get(new_url)

    response = response.json()
    random_cat = response[0].get('url')
    return random_cat


@bot.message_handler(commands=['start'])
def wake_up(message):
    chat = message.chat
    name = message.chat.first_name
    #объект клавы
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #button_newcat = types.KeyboardButton('/newcat')
    #добавление объекта кнопи на клавиатуру
    #keyboard.add(button_newcat)
    keyboard.row(
        types.KeyboardButton('Который час?'),  # Создаём первую кнопку в строке.
        types.KeyboardButton('Определи мой ip'),  # Создаём вторую кнопку в строке.
    )
    keyboard.row(  # Вторая строка кнопок.
        types.KeyboardButton('/newcat'),
        types.KeyboardButton('/random_digit'),  # Создаём кнопку в строке.
    )

    bot.send_message(
        chat_id=chat.id,
        text=f'Удаляю клавиатуру!',
        # Удаляем клавиатуру из интерфейса пользователя:
        reply_markup=types.ReplyKeyboardRemove(),
    )

    bot.send_message(
        chat_id=chat.id,
        text=f'Привет, {name}. Посмотри, какого котика я тебе нашёл',
        # Отправляем клавиатуру в сообщении бота: передаём объект клавиатуры
        # в параметр reply_markup объекта send_message.
        # Telegram-клиент "запомнит" клавиатуру и будет отображать её в интерфейсе бота.
        reply_markup=keyboard
    )
    
    bot.send_photo(chat.id, get_new_image())

# Добавляем хендлер для команд:

@bot.message_handler(commands=['newcat'])
def new_cat(message):
    chat = message.chat
    bot.send_photo(chat.id, get_new_image())

@bot.message_handler(func=lambda message: message.text == 'Который час?')
def handle_time(message):
    current_time = datetime.now().strftime("%H:%M:%S")
    bot.send_message(message.chat.id, f"Сейчас {current_time}")

@bot.message_handler(func=lambda message: message.text == 'Определи мой ip')
def handle_ip(message):
    try:
        ip_response = requests.get('https://api.ipify.org?format=json')
        ip = ip_response.json()['ip']
        bot.send_message(message.chat.id, f"Твой IP: {ip}")
    except:
        bot.send_message(message.chat.id, "Не могу определить IP :(")

@bot.message_handler(commands=['random_digit'])
def what_time(message):
    chat = message.chat
    bot.send_message(chat.id, f"Случайное число: {random.randint(1, 100)}")

@bot.message_handler(func=lambda message: True)
def say_hi(message):
    chat = message.chat
    chat_id = chat.id
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(
        types.KeyboardButton('/start')
    )
    bot.send_message(
        chat_id=chat_id,
        text='Привет, я KittyBot!',
        reply_markup=keyboard
        )


def main():
    bot.polling()

if __name__ == '__main__':
    main()