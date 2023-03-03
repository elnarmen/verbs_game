import os
import requests
from dotenv import load_dotenv

from google.cloud import dialogflow


def parse_json_data(url):
    response = requests.get(url)
    response.raise_for_status()
    decoded_responce = response.json()
    return decoded_responce


def create_intent(project_id, display_name, training_phrases_parts, answer):
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
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
    phrases_url = \
        "https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json"
    deserialized_phrases = parse_json_data(phrases_url)

    for display_name in deserialized_phrases:
        questions = deserialized_phrases[display_name]["questions"]
        answer = [deserialized_phrases[display_name]["answer"]]
        create_intent(project_id, display_name, questions, answer)


if __name__ == "__main__":
    main()
