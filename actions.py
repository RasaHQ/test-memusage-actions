from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run_once(self) -> List[Dict[Text, Any]]:
        dispatcher = CollectingDispatcher()
        tracker = Tracker.from_dict({"sender_id": "tester"})
        domain = {}
        self.run(dispatcher, tracker, domain)

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        for i in range(100):
            b = list(range(1000000))
        dispatcher.utter_message(text="Hello World!")

        return []
