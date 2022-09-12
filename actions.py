from typing import Any, Text, Dict, List 
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionSearch(Action):

    def name(self) -> Text:
        return "action_search"

    def run(self, dispatcher: CollectingDispatcher, 
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        camera = tracker.get_slot('camera')
        ram = tracker.get_slot('RAM')
        battery = tracker.get_slot('battery')
        print(str(camera)+","+str(ram)+","+str(battery))
        dispatcher.utter_message(text='Here are your search results')
        dispatcher.utter_message(text='The features you entered: '+str(camera)+","+str(ram)+","+str(battery))
        return []

class ActionShowLatestNews(Action):

    def name(self) -> Text:
        return "action_show_latest_news"

    def run(self, dispatcher: CollectingDispatcher, 
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text='Here the latest news for your category')
        return []