# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/

from typing import Any, Text, Dict, List, Union
import numpy as np
import warnings

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, ReminderScheduled, ReminderCancelled, FollowupAction
from rasa_sdk.executor import CollectingDispatcher

from datetime import datetime, timedelta

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
    created_at = datetime.now()
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

        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

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
            start_fast_dt = datetime.strptime(str(start_fast), '%Y-%m-%d %H:%M:%S')
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

        start_fast = datetime.strptime(str(tracker.get_slot('start_fast')), '%Y-%m-%d %H:%M:%S')
        hours_fasted, mins_fasted = _calc_fasting_since(start_fast)
        total_hours_fasted = hours_fasted + mins_fasted/60

        return [SlotSet("total_hours_fasted", total_hours_fasted), SlotSet("is_fasting", 0), SlotSet("start_fast", None), SlotSet("hours_fasted", "0 Stunden"), SlotSet("mins_fasted", "0 Minuten"), FollowupAction("action_forget_reminder_fast")]


#### Fasting log
class ActionSendOverview(Action):
    """ send overview """

    def name(self) -> Text:
        return "action_send_overview"

    def run(self, 
                dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any],
            ) -> List[Dict[Text, Any]]:
        
        DAYS_IN_PERIOD = 30
        events_in_period = ActionSendOverview._get_events_for_period(tracker.events, days_in_period=DAYS_IN_PERIOD)
        avg_hours_fasted, days_w_24h_or_more, total_days_fasted = ActionSendOverview._return_overview_stats(events_in_period)
        
        events_in_period_offset = ActionSendOverview._get_events_for_period(tracker.events, days_in_period=DAYS_IN_PERIOD, days_to_offset=DAYS_IN_PERIOD)
        avg_hours_fasted_offset, days_w_24h_or_more_offset, total_days_fasted_offset = ActionSendOverview._return_overview_stats(events_in_period_offset)
        diff_avg_hours_fasted = avg_hours_fasted - avg_hours_fasted_offset
        diff_days_w_24h_or_more = days_w_24h_or_more - days_w_24h_or_more_offset
        diff_total_days_fasted = total_days_fasted - total_days_fasted_offset

        txt_msg = f"Hier ist deine Übersicht der letzten {DAYS_IN_PERIOD} Tage:\n"
        txt_msg += f" - du hast an {total_days_fasted} {'Tag' if total_days_fasted==1 else 'Tagen'} gefastet "
        txt_msg += f"({'+' if diff_total_days_fasted>=0 else ''}{diff_total_days_fasted} {'Tag' if diff_total_days_fasted==1 else 'Tage'})\n"
        txt_msg += f" - du hast durchschn. {avg_hours_fasted:,.2f} Stunden gefastet " 
        txt_msg += f"({'+' if diff_avg_hours_fasted>=0  else ''}{diff_avg_hours_fasted:,.2f} Stunden)\n"
        txt_msg += f" - du hast an {days_w_24h_or_more} {'Tag' if days_w_24h_or_more==1 else 'Tagen'} mind. 24 Stunden gefastet "
        txt_msg += f"({'+' if diff_days_w_24h_or_more>=0  else ''}{diff_days_w_24h_or_more} {'Tag' if abs(diff_days_w_24h_or_more)==1 else 'Tage'})\n\n"
        txt_msg += f"Die Zahlen in Klammern sind die Veränderung gegenüber den {DAYS_IN_PERIOD} Tagen davor."

        dispatcher.utter_message(text = txt_msg)
        
    @staticmethod
    def _get_events_for_period(events, days_in_period, days_to_offset=0):
        """
        For a given list of events, return only those events that are within a given period.

        :param events:          list of dictionaries    (rasa event list of dictionaries)
        :param days_in_period:  integer                 (days in the past to consider for event window)
        :param days_to_offset:  integer                 (number of days to offset event window into the past)

        :return:                list of dictionaries    (rasa events within requested period)
        """
        return [row for row in events \
            if datetime.fromtimestamp(row['timestamp']) > (datetime.now() - timedelta(days=days_in_period+days_to_offset)) \
            if datetime.fromtimestamp(row['timestamp']) < (datetime.now() - timedelta(days=days_to_offset))]

    @staticmethod
    def _return_overview_stats(events):
        avg_hours_fasted = ActionSendOverview._calculate_median_hours_fasted(events)
        days_w_24h_or_more = ActionSendOverview._calculate_days_w_24h_or_more(events)
        total_days_fasted = ActionSendOverview._calculate_total_days_fasted(events)
        return avg_hours_fasted, days_w_24h_or_more, total_days_fasted

    @staticmethod
    def _calculate_median_hours_fasted(events):
        warnings.filterwarnings(action='ignore', message='Mean of empty slice') # np.median or np.nanmedian will throw an irrelevant warning for np.median([])
        return np.nan_to_num(np.nanmedian([row["value"] for row in events if row["event"] == "slot" if row["name"] == "total_hours_fasted"]))

    @staticmethod
    def _calculate_days_w_24h_or_more(events):
        return len([row["value"] for row in events if row["event"] == "slot" if row["name"] == "total_hours_fasted" if row["value"]>24])

    @staticmethod
    def _calculate_total_days_fasted(events):
        return len([row["value"] for row in events if row["event"] == "slot" if row["name"] == "total_hours_fasted"])


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
            start_fast_dt = datetime.strptime(str(start_fast), '%Y-%m-%d %H:%M:%S')
            hours_fasted, _ = _calc_fasting_since(start_fast_dt)
            if hours_fasted < 16:
                reminder_in_x_hours = 16
            elif hours_fasted < 20: 
                reminder_in_x_hours = 4
            elif hours_fasted < 24: 
                reminder_in_x_hours = 4
            elif hours_fasted < 48:
                reminder_in_x_hours = 24

        date = datetime.now() + timedelta(hours=reminder_in_x_hours)
        
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
