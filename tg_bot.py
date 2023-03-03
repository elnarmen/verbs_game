import os
import logging

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


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Здравствуйте, чем можем помочь? {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True)
    )


def detect_intent_texts(update: Update, context: CallbackContext, project_id):
    session_id = update.effective_user.id
    language_code = 'ru'
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(
        text=update.message.text, language_code=language_code
    )
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    update.message.reply_text(response.query_result.fulfillment_text)


def main():
    load_dotenv()
    project_id = os.getenv('PROJECT_ID')
    TG_TOKEN = os.getenv('TG_TOKEN')

    updater = Updater(TG_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command,
        partial(detect_intent_texts, project_id=project_id)
    ))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
