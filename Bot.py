import telebot
import requests
import time

# Токен вашего бота в Telegram
TOKEN = ''

# Токен для доступа к API Robotext.io
ROBOTEXT_API_TOKEN = '25a04608-5679-49f3-bde6-30ea4c116510'

# Создание объекта бота
bot = telebot.TeleBot(TOKEN)

# Глобальные переменные для хранения текста и длины поэмы
text_for_generation = ""
poem_length = 10


# Приветственное сообщение
@bot.message_handler(commands=['start', 'help'])
def help_message(message):
    response = "Привет! Я бот для генерации стихов.\n\n" \
               "Доступные команды:\n" \
               "/start - Начать общение\n" \
               "/help - Получить справку о доступных командах\n" \
               "/poem - Сгенерировать стих\n" \
               "/save - Сохранить последний сгенерированный стих в файл\n" \
               "/set_word - Установить текст для генерации стиха\n"
    bot.reply_to(message, response)


# Генерация стиха
@bot.message_handler(commands=['poem'])
def generate_poem(message):
    global text_for_generation
    if not text_for_generation:
        bot.reply_to(message, "Перед генерацией стиха установите текст для генерации с помощью команды /set_word")
    else:
        poem = generate_poem_with_robotext()
        bot.reply_to(message, poem)


# Сохранение последнего стиха в файл
@bot.message_handler(commands=['save'])
def save_poem(message):
    with open('last_poem.txt', 'w', encoding="utf - 8") as file:
        file.write(last_poem)
    bot.reply_to(message, "Последний стих сохранен в файле 'last_poem.txt'.")


# Команда для установки текста для генерации стиха
@bot.message_handler(commands=['set_word'])
def set_text(message):
    global text_for_generation
    text_for_generation = message.text.replace('/set_word ', '')
    bot.reply_to(message, f"Текст для генерации установлен: '{text_for_generation}'")


# Функция для генерации стиха с помощью API Robotext.io
def generate_poem_with_robotext():
    global last_poem
    url = "https://robotext.io/create-write-job/poem"
    payload = {
        "radio": "value1",
        'keys': text_for_generation
    }
    headers = {
        'Authorization': f'Bearer {ROBOTEXT_API_TOKEN}'
    }
    url1 = "https://robotext.io/ping-write-job"
    response = requests.request("POST", url, headers=headers, data=payload)
    response1 = response.json()

    if "job_id" not in response1:
        return "Ошибка при отправке запроса к API"

    url2 = url1 + "?job_id=" + str(response1["job_id"])
    response2 = requests.get(url2, "result")
    response3 = response2.json()
    while response3["status"] != "completed":
        time.sleep(5)
        response2 = requests.get(url2, "result")
        response3 = response2.json()

    last_poem = response3["result"]
    return response3["result"]


# Запуск бота
bot.polling()
