'''

tests for Rasa actions server

'''

import pytest
from datetime import datetime, timedelta

from rasa.actions import ActionSendFastingLog


@pytest.mark.parametrize(
    "events, expected", [
        (
            [
                {"event": "slot", "timestamp": datetime.timestamp(datetime(datetime.now().year, 
                    datetime.now().month, datetime.now().day, 11, 0) - timedelta(days=3)), 
                    "name": "total_hours_fasted", "value": 22.616666666666667}, 
                {'event': 'slot', 'timestamp': 1600619208.9505951, 'name': 'mins_fasted', 'value': '53 Minuten'}, 
                {'event': 'slot', 'timestamp': 1600619208.9506164, 'name': 'is_fasting', 'value': 1}, 
                {"event": "slot", "timestamp": datetime.timestamp(datetime(datetime.now().year, 
                    datetime.now().month, datetime.now().day, 11, 0) - timedelta(days=1)), 
                    "name": "total_hours_fasted", "value": 18.983333333333334}, 
                {"event": "slot", "timestamp": datetime.timestamp(datetime(datetime.now().year, 
                    datetime.now().month, datetime.now().day, 11, 0) - timedelta(days=0)), 
                    "name": "total_hours_fasted", "value": 13.9833333333334}
            ], (1, 1, 55.5833333333334, 18.5277777777778, 22.616666666666667)
        ), (
            [
                {"event": "slot", "timestamp": datetime.timestamp(datetime(datetime.now().year, 
                    datetime.now().month, datetime.now().day, 11, 0) -  timedelta(days=3)), 
                    "name": "total_hours_fasted", "value": 22.616666666666667}, 
                {"event": "slot", "timestamp": datetime.timestamp(datetime(datetime.now().year, 
                    datetime.now().month, datetime.now().day, 11, 0) -  timedelta(days=2)), 
                    "name": "total_hours_fasted", "value": 13.983333333333334}, 
                {'event': 'slot', 'timestamp': 1600619208.9505951, 'name': 'mins_fasted', 'value': '53 Minuten'}, 
                {'event': 'slot', 'timestamp': 1600619208.9506164, 'name': 'is_fasting', 'value': 1} 
            ], (0, 1, 36.6, 18.3, 22.616666666666667)
        ), (
            [
                {'event': 'slot', 'timestamp': 1600619208.9505951, 'name': 'mins_fasted', 'value': '53 Minuten'}, 
                {'event': 'slot', 'timestamp': 1600619208.9506164, 'name': 'is_fasting', 'value': 1}
            ], (0, 0, 0, 0, 0)
        )
        ], 
        ids=[
            "with_fasting_history_and_with_consecutive_streak", 
            "with_fasting_history_and_without_consecutive_streak", 
            "with_user_that_does_not_have_fasting_history"]
    )
def test_action_send_fasting_log_retrieve_fasting_log(events, expected):
    assert ActionSendFastingLog.retrieve_fasting_log(events) == expected




