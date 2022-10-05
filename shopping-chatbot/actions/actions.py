from typing import Any, Text, Dict, List 
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import FormValidationAction
from rasa_sdk.events import FollowupAction

import re
import MySQLdb

hostname = "db4free.net"
username = "rasa_shopping_db"
password = "password12"
database = "shopping_db"

class ValidatePhoneSearchForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_phone_search_form"

    def validate_RAM(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        ram_int = int(re.findall(r'[0-9]+',value)[0])
        
        if ram_int < 50:
            return {"RAM":ram_int}
        else:
            dispatcher.utter_message(text="Please enter the correct RAM value.")
            return {"RAM":None}

    def validate_camera(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        
        camera_int = int(re.findall(r'[0-9]+',value)[0])
        if camera_int < 150:
            return {"camera":camera_int}
        else:
            dispatcher.utter_message(text="Please enter the correct camera value.")
            return {"camera":None}

    def validate_budget(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        
        budget_int = int(re.findall(r'[0-9]+',value)[0])
        if budget_int < 4000:
            return {"budget":budget_int}
        else:
            dispatcher.utter_message(text="Please enter the budget in USD and below 4000.")
            return {"budget":None}

    def validate_battery(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        
        battery_int = int(re.findall(r'[0-9]+',value)[0])
        if battery_int < 5000:
            return {"battery":battery_int}
        else:
            dispatcher.utter_message(text="Please enter the correct value for battery")
            return {"battery":None}

class ValidateLaptopSearchForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_laptop_search_form"

    def validate_RAM(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        
        ram_int = int(re.findall(r'[0-9]+',value)[0])
        if ram_int < 50:
            return {"RAM":ram_int}
        else:
            dispatcher.utter_message(text="Please enter the correct RAM value.")
            return {"RAM":None}

    def validate_battery_backup(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        
        battery_backup_int = int(re.findall(r'[0-9]+',value)[0])
        if battery_backup_int < 150:
            return {"battery_backup":battery_backup_int}
        else:
            dispatcher.utter_message(text="Please enter the correct value for battery backup.")
            return {"battery_backup":None}

    def validate_storage_capacity(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        
        storage_capacity_int = int(re.findall(r'[0-9]+',value)[0])
        if storage_capacity_int < 1000:
            return {"storage_capacity":storage_capacity_int}
        else:
            dispatcher.utter_message(text="Please enter the correct storage capacity in GBs")
            return {"storage_capacity":None}

    def validate_budget(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
    
        budget_int = int(re.findall(r'[0-9]+',value)[0])
        if budget_int < 4000:
            return {"budget":budget_int}
        else:
            dispatcher.utter_message(text="Please enter the budget in USD and below 4000.")
            return {"budget":None}

class FindItemsLaptop(Action):

    def name(self) -> Text:
        return "action_find_laptop"

    def run(self, dispatcher: CollectingDispatcher, 
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        db = MySQLdb.connect(hostname,username,password,database)
        ram = tracker.get_slot('RAM')
        storage_capacity = tracker.get_slot('storage_capacity')
        battery_backup = tracker.get_slot('battery_backup')
        budget = tracker.get_slot('budget')

        cursor = db.cursor()
        cursor.execute("SELECT product_url FROM products WHERE ram >= %s AND storage >= %s AND battery_backup >= %s AND price_usd <= %s AND category= %s", [int(ram), int(storage_capacity), int(battery_backup), int(budget), 'laptop'])

        products = cursor.fetchall()

        if len(products) != 0:
            dispatcher.utter_message(text='Please find your searched items here:')
            for x in products:
                dispatcher.utter_message(text=x[0])
        else:
            dispatcher.utter_message(text="Looks like there aren't any products that math your search.")

        return []

class FindItemsPhone(Action):

    def name(self) -> Text:
        return "action_find_phone"

    def run(self, dispatcher: CollectingDispatcher, 
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        db = MySQLdb.connect(hostname,username,password,database)
        ram = tracker.get_slot('RAM')
        camera = tracker.get_slot('camera')
        battery = tracker.get_slot('battery')
        budget = tracker.get_slot('budget')

        cursor = db.cursor()
        cursor.execute("SELECT product_url FROM products WHERE ram >= %s AND back_camera_megapixel >= %s AND battery_mah >= %s AND price_usd <= %s AND category= %s", [int(ram), int(camera), int(battery), int(budget), 'phone'])

        products = cursor.fetchall()

        if len(products) != 0:
            dispatcher.utter_message(text='Please find your searched items here:')
            for x in products:
                dispatcher.utter_message(text=x[0])
        else:
            dispatcher.utter_message(text="Looks like there aren't any products that math your search.")

        return []

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

        db = MySQLdb.connect(hostname,username,password,database)
        cursor = db.cursor()
        cursor.execute("SELECT blog_url FROM news WHERE category=%s LIMIT 3",['phone'])
        
        news = cursor.fetchall()

        if len(news) != 0:
            dispatcher.utter_message(text='Here the latest news for your category')
            for x in news:
                dispatcher.utter_message(text=x[0])
        else:
            dispatcher.utter_message(text="Looks like there isnt any news available.")

        dispatcher.utter_message(response='utter_select_next')
        return []

class MyFallback(Action):

    def name(self) -> Text:
        return "action_my_fallback"

    def run(self, dispatcher: CollectingDispatcher, 
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response = "utter_fallback")
        return []

class YourResidence(Action):

    def name(self) -> Text:
        return "action_your_residence"

    def run(self, dispatcher: CollectingDispatcher, 
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response = "utter_residence")
        return [FollowupAction(tracker.active_loop.get('name'))]
    