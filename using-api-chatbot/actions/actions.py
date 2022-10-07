# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import json

class ActionCatApi(Action):

     def name(self) -> Text:
        return "action_cat_api"

     def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #Retorna uma imagem aleatoria de um gato, pela seguinte API:
        response_API = requests.get('https://api.thecatapi.com/v1/images/search')

        #Retorna api em forma de texto
        data = response_API.text

        #Converte para JSON
        parse_json = json.loads(data)

        #Retorna a url da imagem
        img_url = parse_json[0]['url']

        #Envia a mensagem
        dispatcher.utter_message(image=img_url)

        return []

