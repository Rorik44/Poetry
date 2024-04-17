import logging
from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup
import requests
import time
BOT_TOKEN = ""
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

reply_keyboard = [['/cт', '/шаблон'],
                  ['/произвольный']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

async def close_keyboard(update, context):
    await update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )

async def start(update, context):
    def poet(x):
        url = "https://robotext.io/create-write-job/poem"
        payload = {"radio": "value1",
                   'keys': x}
        headers = {
            'Authorization': 'Bearer 25a04608-5679-49f3-bde6-30ea4c116510'

        }
        url1 = "https://robotext.io/ping-write-job"
        response = requests.request("POST", url, headers=headers, data=payload)
        response1 = response.json()

        url2 = url1 + "?job_id=" + str(response1["job_id"])
        response2 = requests.get(url2, "result")
        response3 = response2.json()
        while response3["status"] != "completed":
            time.sleep(5)
            response2 = requests.get(url2, "result")
            response3 = response2.json()

        return response3["result"]
    await update.message.reply_text(
        poet("Города колыхались в танце любви"),
        reply_markup=markup
    )




def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("close", close_keyboard))




    application.run_polling()


if __name__ == '__main__':
    main()
