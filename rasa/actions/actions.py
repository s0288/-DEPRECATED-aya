# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/

from typing import Any, Text, Dict, List, Union

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, ReminderScheduled, ReminderCancelled, FollowupAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction

import datetime 
# import src.db_actions

# Actions_DB = src.db_actions.Actions_DB()


#### STARTING AND ENDING A FAST

class ActionStartFast(Action):
    """ 1) add a new fast to the event_db, 2) create a reminder to tell the user of his success after {hours_fasted} hours """

    def name(self) -> Text:
        return "action_start_fast"

    def run(self, 
                dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any],
            ) -> List[Dict[Text, Any]]:

        name = 'start_fast'
        created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        platform_user_id = tracker.sender_id
        platform_name = 'Telegram'
        value = created_at
        received_at = created_at

        # Actions_DB.add_action(name, created_at, platform_user_id, platform_name, value, received_at)

        # set slots and schedule a reminder
        return [SlotSet("is_fasting", 1), SlotSet("start_fast", created_at), FollowupAction("action_set_reminder_fast")]

class ActionFastingSince(Action):
    """ calculate the time since the start of the fast """

    def name(self) -> Text:
        return "action_fasting_since"

    def run(self, 
                dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any],
            ) -> List[Dict[Text, Any]]:

        
        ## check if user is currently fasting
        start_fast = tracker.get_slot('start_fast')

        # if slot is not set, get the most recent value in the database
        # if start_fast == 'None': # Rasa converts None to 'None'
        #     start_fast = Actions_DB.get_last_start_fast(415604082, 'Telegram')

        ## if user is currently fasting, set text slots
        ## calculate time_fasted        
        try:
            created_at = datetime.datetime.now()
            # make sure start_fast has the right format
            start_fast = datetime.datetime.strptime(str(start_fast), '%Y-%m-%d %H:%M:%S')

            time_fasted = created_at - start_fast
            days_fasted = time_fasted.days
            seconds_fasted = time_fasted.seconds + time_fasted.days*24*60*60

            hours_fasted = seconds_fasted//3600 # round to nearest integer
            mins_fasted = (seconds_fasted%3600)//60 # get remainder in mins

            # for singular, set values
            mins_str = f'{mins_fasted} Minute' if mins_fasted == 1 else f'{mins_fasted} Minuten'
            hours_str = f'{hours_fasted} Stunde' if hours_fasted == 1 else f'{hours_fasted} Stunden'

            ## set is_fasting to 1 since the user is fasting
            is_fasting = 1
        ## if user is currently not fasting, set slots to None
        except:
            mins_str = '0 Minuten'
            hours_str = '0 Stunden'
            ## set is_fasting to 0 since the user is not fasting
            is_fasting = 0

        return [SlotSet("is_fasting", is_fasting), SlotSet("start_fast", str(start_fast)), SlotSet("hours_fasted", hours_str), SlotSet("mins_fasted", mins_str)]


class ActionEndFast(Action):
    """ add an end_fast event """   

    def name(self) -> Text:
        return "action_end_fast"

    def run(self, 
                dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any],
            ) -> List[Dict[Text, Any]]:

        ## add end_fast to event_db
        created_at = datetime.datetime.now()
        name = 'end_fast'
        created_at = created_at.strftime('%Y-%m-%d %H:%M:%S')
        platform_user_id = tracker.sender_id
        platform_name = 'Telegram'
        value = created_at
        received_at = created_at
        # Actions_DB.add_action(name, created_at, platform_user_id, platform_name, value, received_at)

        return [SlotSet("is_fasting", 0), SlotSet("start_fast", None), SlotSet("hours_fasted", "0 Stunden"), SlotSet("mins_fasted", "0 Minuten"), FollowupAction("action_forget_reminder_fast")]


#### EXTRACT DATA
class ActionEntityExtract(Action):
    """ extract entity from msg """   

    def name(self) -> Text:
        return "action_entity_extract"

    def run(self, 
                dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any],
            ) -> List[Dict[Text, Any]]:

        ## extract entity
        entities = tracker.latest_message['entities']
        print(entities)

        for e in entities:
            if e['entity'] == 'weight_value':
                weight_value = e['value']

        return [SlotSet("weight_value", weight_value)]



#### REMINDERS

class SetReminderFast(Action):
    """ Creates a reminder to tell the user he fasted {hours_fasted} hours already """

    def name(self) -> Text:
        return "action_set_reminder_fast"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        date = datetime.datetime.now() + datetime.timedelta(seconds=10) # 16 hours
        entities = tracker.latest_message.get("entities")

        reminder = ReminderScheduled(
            "fast_reminder",
            trigger_date_time=date,
            entities=entities,
            name="fast_reminder",
            kill_on_user_message=False,
        )

        print("setting reminder")

        return [reminder]            


class ForgetReminderFast(Action):
    """Cancels fasting reminder."""

    def name(self) -> Text:
        return "action_forget_reminder_fast"

    def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:


        print("removing reminder")

        # Cancel all reminders
        return [ReminderCancelled(name="fast_reminder")]


### journalling

class ReflectDayForm(FormAction):
    """ Reflect your day """

    def name(self) -> Text:
        """Unique identifier of the form"""
        return "reflect_day_form"

    @staticmethod
    def required_slots(tracker:Tracker) -> List[Text]:
        ''' A list of required slots that the form has to fill '''

        return ["reflect_situation", "reflect_remedy"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
        or a list of them, where a first match will be picked."""
        
        return {
            "reflect_situation": [self.from_entity(entity="reflect_situation"), self.from_text()],
            "reflect_remedy": [self.from_entity(entity="reflect_remedy"), self.from_text()],
        }

    def submit(self, 
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        ''' Define what the form has to do after all required slots are filled '''

        return[SlotSet("reflect_situation", None), SlotSet("reflect_remedy", None)]