import os
import random
import logging
import telegram
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv
from google.cloud import dialogflow


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def send_log(error, bot, chat_id):
    error_message = ''.join(
        traceback.format_exception(
            None,
            error,
            error.__traceback__
        )
    )
    bot.send_message(chat_id=chat_id, text=error_message)


def detect_intent_texts(event, vk_api, project_id):
    session_id = event.user_id
    language_code = 'ru'
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(
        text=event.text, language_code=language_code
    )
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    if not response.query_result.intent.is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=response.query_result.fulfillment_text,
            random_id=random.randint(1, 1000)
        )


if __name__ == '__main__':
    load_dotenv()

    logs_bot_token = os.getenv('LOGS_TELEGRAM_BOT_TOKEN')
    logs_chat_id = os.getenv('LOGS_TELEGRAM_CHAT_ID')
    vk_token = os.getenv('VK_TOKEN')
    project_id = os.getenv('PROJECT_ID')

    logs_telegram_bot = telegram.Bot(token=logs_bot_token)
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            try:
                detect_intent_texts(event, vk_api, project_id)
            except Exception as err:
                logger.exception(err)
                send_log(str(err), logs_telegram_bot, logs_chat_id)