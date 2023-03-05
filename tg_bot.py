import os
import logging
import telegram
import traceback
from telegram import Update, ForceReply

from telegram.ext import (
    Updater,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    Filters)

from dotenv import load_dotenv
from google.cloud import dialogflow
from functools import partial
from dialogflow_handlers import detect_intent_texts
from logs_handler import TelegramLogsHandler


logger = logging.getLogger(__name__)


def error_handler(update: Update, context: CallbackContext):
    logger.exception(context.error)


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Здравствуйте, чем можем помочь? {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True)
    )


def send_message(update: Update, context: CallbackContext, project_id):
    1/0
    session_id = update.effective_user.id
    text = update.message.text
    response = detect_intent_texts(project_id, session_id, text)
    update.message.reply_text(response.fulfillment_text)


def main():
    load_dotenv()

    project_id = os.getenv('PROJECT_ID')
    logs_chat_id = os.getenv('LOGS_TELEGRAM_CHAT_ID')
    logs_bot = telegram.Bot(token=os.getenv('LOGS_TELEGRAM_BOT_TOKEN'))

    logger.setLevel(logging.ERROR)
    logger.addHandler(TelegramLogsHandler(logs_bot, logs_chat_id))

    updater = Updater(os.getenv('TELEGRAM_TOKEN'), use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_error_handler(error_handler)
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command,
        partial(send_message, project_id=project_id)
    ))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
