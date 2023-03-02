import logging
import os

from telegram import Update, ForceReply
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv
from google.cloud import dialogflow

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
load_dotenv()
logger = logging.getLogger(__name__)
PROJECT_ID = os.getenv('PROJECT_ID')
TG_TOKEN = os.getenv('TG_TOKEN')
print(TG_TOKEN)

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True)
    )


def detect_intent_texts(update: Update, context: CallbackContext):
    session_id = update.effective_user.id
    language_code = 'ru'
    session_client = dialogflow.SessionsClient()
    project_id = PROJECT_ID
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
    updater = Updater(TG_TOKEN)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, detect_intent_texts))

    updater.start_polling()
    updater.idle()

if __name__=='__main__':
    main()
