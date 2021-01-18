# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/

from typing import Any, Text, Dict, List, Union

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, ReminderScheduled, ReminderCancelled, FollowupAction
from rasa_sdk.executor import CollectingDispatcher

import datetime 

#### helper funcs
def _calc_fasting_since(start_fast):
    '''
        Subtract the start_fast (a timestamp) from the current time.
        Parameters:
            start_fast: timestamp
        Returns:
            hours_fasted: integer
            mins_fasted: integer
    '''
    created_at = datetime.datetime.now()
    time_fasted = created_at - start_fast
    seconds_fasted = time_fasted.seconds + time_fasted.days*24*60*60
    hours_fasted = seconds_fasted//3600 # round to nearest integer
    mins_fasted = (seconds_fasted%3600)//60 # get remainder in mins
    return hours_fasted, mins_fasted

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

        created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

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
        
        if start_fast is None or start_fast == "None": # if user is currently not fasting, set slots to None
            is_fasting = 0 # set is_fasting to 0 since the user is not fasting
            mins_str = '0 Minuten'
            hours_str = '0 Stunden'
        else: # if user is currently fasting, set text slots
            is_fasting = 1 # set is_fasting to 1 since the user is fasting
            start_fast_dt = datetime.datetime.strptime(str(start_fast), '%Y-%m-%d %H:%M:%S')
            hours_fasted, mins_fasted = _calc_fasting_since(start_fast_dt)
            # if singular, set values
            mins_str = f'{mins_fasted} Minute' if mins_fasted == 1 else f'{mins_fasted} Minuten'
            hours_str = f'{hours_fasted} Stunde' if hours_fasted == 1 else f'{hours_fasted} Stunden'

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

        start_fast = datetime.datetime.strptime(str(tracker.get_slot('start_fast')), '%Y-%m-%d %H:%M:%S')
        hours_fasted, mins_fasted = _calc_fasting_since(start_fast)
        total_hours_fasted = hours_fasted + mins_fasted/60

        return [SlotSet("total_hours_fasted", total_hours_fasted), SlotSet("is_fasting", 0), SlotSet("start_fast", None), SlotSet("hours_fasted", "0 Stunden"), SlotSet("mins_fasted", "0 Minuten"), FollowupAction("action_forget_reminder_fast")]


#### Fasting log
class ActionSendFastingLog(Action):
    """ send fasting log """

    def name(self) -> Text:
        return "action_send_fasting_log"

    def run(self, 
                dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any],
            ) -> List[Dict[Text, Any]]:
        
        consecutive_cnt, max_cnt, total_fasted_7d, avg_fasted_7d, max_fasted_7d = ActionSendFastingLog.retrieve_fasting_log(tracker.events)
        if consecutive_cnt == 1:
            str_consecutive = f"{consecutive_cnt} Tag"
        else:
            str_consecutive = f"{consecutive_cnt:,} Tagen"

        dispatcher.utter_message(text = f"Du fastest seit {str_consecutive} in Folge. Dein Rekord liegt bei {max_cnt:,} Tagen.\n \nHier ist deine Übersicht der letzten 7 Tage:\n  - du hast {total_fasted_7d:,.2f} Stunden gefastet\n  - durchschn. hast du {avg_fasted_7d:,.2f} Stunden gefastet\n  - dein längstes Fasten war {max_fasted_7d:,.2f} Stunden")

    @staticmethod
    def retrieve_fasting_log(events, days_to_subtract=7):
        '''
            get summary stats for fasting_log
        '''
        # consecutive days until today
        fasting_log = [{"value": event["value"], "date_end": datetime.datetime.fromtimestamp(event["timestamp"]).date(), "date_start": (datetime.datetime.fromtimestamp(event["timestamp"]) -  datetime.timedelta(hours=event["value"])).date()} for event in events if event["event"] == "slot" if event["name"] == "total_hours_fasted"]
        if len(fasting_log) > 0: # if no fast has been finished so far, there is no relevant event 
            consecutive_list = [(log["date_end"].toordinal(), log["date_start"].toordinal()) for log in fasting_log]
            consecutive_cnt = 0
            max_cnt = 0
            for (first_event, second_event) in zip(consecutive_list, consecutive_list[1:]): # compare two adjacent fasting events: did one start at the end of the other? Important: reverse the list because the tracker shows the most recent value first
                if max(first_event) == min(second_event):
                    consecutive_cnt += 1
                    if consecutive_cnt > max_cnt:
                        max_cnt = consecutive_cnt
                else:
                    consecutive_cnt = 0
            if datetime.datetime.now().toordinal() - max(max(consecutive_list))>1: # if the user has not started a fast today or yesterday, set to 0
                consecutive_cnt = 0
    
            # stats for relevant period
            start_of_period = datetime.datetime.now().date() -  datetime.timedelta(days=days_to_subtract)
            fasting_log = [event["value"] for event in fasting_log if event["date_start"] > start_of_period]
            total_fasted_7d, avg_fasted_7d, max_fasted_7d = (0, 0, 0)
            if len(fasting_log) > 0: # if no fast has been finished within the relevant period, there is no relevant event 
                total_fasted_7d = sum(fasting_log)
                avg_fasted_7d = sum(fasting_log) / len(fasting_log)
                max_fasted_7d = max(fasting_log)
            return consecutive_cnt, max_cnt, total_fasted_7d, avg_fasted_7d, max_fasted_7d
        else:
            return 0, 0, 0, 0, 0

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

        # based on fasting time, set reminder (e.g. hours=16, if at start of fast)
        start_fast = tracker.get_slot('start_fast')

        if start_fast is None: # if user is currently not fasting, assume he is at start of fast
            reminder_in_x_hours = 16
        else:
            start_fast_dt = datetime.datetime.strptime(str(start_fast), '%Y-%m-%d %H:%M:%S')
            hours_fasted, _ = _calc_fasting_since(start_fast_dt)
            if hours_fasted < 16:
                reminder_in_x_hours = 16
            elif hours_fasted < 20: 
                reminder_in_x_hours = 4
            elif hours_fasted < 24: 
                reminder_in_x_hours = 4
            elif hours_fasted < 48:
                reminder_in_x_hours = 24

        date = datetime.datetime.now() + datetime.timedelta(hours=reminder_in_x_hours)
        
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
