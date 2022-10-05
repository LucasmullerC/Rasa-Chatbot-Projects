import datetime
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import ReminderScheduled, ReminderCancelled
from rasa_sdk.executor import CollectingDispatcher

class ActionSetReminder(Action):
    """Schedules a reminder, supplied with the last message's entities."""

    def name(self) -> Text:
        return "action_set_reminder"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        dispatcher.utter_message("Ok! Irei te enviar um lembrete em 15 segundos.")

        date = datetime.datetime.now() + datetime.timedelta(seconds=15)
        entities = tracker.latest_message.get("entities")

        reminder = ReminderScheduled(
            "EXTERNAL_reminder",
            trigger_date_time=date,
            entities=entities,
            name="my_reminder",
            kill_on_user_message=False,
        )

        return [reminder]

class ActionReactToReminder(Action):
    """Reminds the user to call someone."""

    def name(self) -> Text:
        return "action_react_to_reminder"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        name = next(tracker.get_latest_entity_values("name"), "alguém")
        dispatcher.utter_message(f"Este é o seu lembrete de ligar para {name}!")

        return []

class ForgetReminders(Action):
    """Cancels all reminders."""

    def name(self) -> Text:
        return "action_forget_reminders"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        dispatcher.utter_message("Cancelando todos os seus lembretes.")

        # Cancel all reminders
        return [ReminderCancelled()]
