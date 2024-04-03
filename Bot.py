import logging
from telegram.ext import Application, MessageHandler, filters

BOT_TOKEN = ""

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


async def echo(update, context):
    await update.message.reply_text(
        "К сожалению, сейчас у этого бота нет нужных функций для полноценного общения с пользователем")


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    text_handler = MessageHandler(filters.TEXT, echo)

    application.add_handler(text_handler)

    application.run_polling()


if __name__ == '__main__':
    main()