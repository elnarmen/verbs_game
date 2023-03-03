import os
import requests
import json
import logging
from dotenv import load_dotenv
from google.cloud import dialogflow


logger = logging.getLogger(__name__)


def deserialize_phrases(path):
    with open(path, "r") as file:
        phrases_json = file.read()
    deserialized_phrases = json.loads(phrases_json)
    return deserialized_phrases


def create_intent(project_id, display_name, training_phrases_parts, answer):
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=answer)
    message = dialogflow.Intent.Message(text=text)
    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))


def main():
    load_dotenv()
    project_id = os.getenv("PROJECT_ID")
    phrases_path = os.getenv("TRAINING_PHRASES_PATH")
    deserialized_phrases = deserialize_phrases(phrases_path)
    for display_name in deserialized_phrases:
        questions = deserialized_phrases[display_name]["questions"]
        answer = [deserialized_phrases[display_name]["answer"]]
        create_intent(project_id, display_name, questions, answer)


if __name__ == "__main__":
    main()
