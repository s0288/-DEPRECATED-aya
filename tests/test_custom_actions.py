'''

Unit tests

'''

import unittest
import datetime
from rasa.actions import ActionSendFastingLog

class TestActionSendFastingLog(unittest.TestCase):
    # tests for ActionSendFastingLog
    def test_retrieve_fasting_log_with_fasting_history_and_with_consecutive_streak(self):
        events = [{"event": "slot", "timestamp": datetime.datetime.timestamp(datetime.datetime.now() -  datetime.timedelta(days=3)), "name": "total_hours_fasted", "value": 22.616666666666667}, {'event': 'slot', 'timestamp': 1600619208.9505951, 'name': 'mins_fasted', 'value': '53 Minuten'}, {'event': 'slot', 'timestamp': 1600619208.9506164, 'name': 'is_fasting', 'value': 1}, {"event": "slot", "timestamp": datetime.datetime.timestamp(datetime.datetime.now() -  datetime.timedelta(days=1)), "name": "total_hours_fasted", "value": 18.983333333333334}, {"event": "slot", "timestamp": datetime.datetime.timestamp(datetime.datetime.now() -  datetime.timedelta(days=0)), "name": "total_hours_fasted", "value": 13.983333333333334}] # test events
        self.assertEqual((1, 55.583333333333336, 18.52777777777778, 22.616666666666667), ActionSendFastingLog.retrieve_fasting_log(events), "Should be (1, 55.583333333333336, 18.52777777777778, 22.616666666666667)")

    def test_retrieve_fasting_log_with_fasting_history_and_without_consecutive_streak(self):
        events = [{"event": "slot", "timestamp": datetime.datetime.timestamp(datetime.datetime.now() -  datetime.timedelta(days=3)), "name": "total_hours_fasted", "value": 22.616666666666667}, {"event": "slot", "timestamp": datetime.datetime.timestamp(datetime.datetime.now() -  datetime.timedelta(days=2)), "name": "total_hours_fasted", "value": 13.983333333333334}, {'event': 'slot', 'timestamp': 1600619208.9505951, 'name': 'mins_fasted', 'value': '53 Minuten'}, {'event': 'slot', 'timestamp': 1600619208.9506164, 'name': 'is_fasting', 'value': 1}] # test events
        self.assertEqual((0, 36.6, 18.3, 22.616666666666667), ActionSendFastingLog.retrieve_fasting_log(events), "Should be (0, 36.6, 18.3, 22.616666666666667)")

    def test_retrieve_fasting_log_with_user_that_does_not_have_fasting_history(self):        
        events = [{'event': 'slot', 'timestamp': 1600619208.9505951, 'name': 'mins_fasted', 'value': '53 Minuten'}, {'event': 'slot', 'timestamp': 1600619208.9506164, 'name': 'is_fasting', 'value': 1}] # test events
        self.assertEqual((0, 0, 0, 0), ActionSendFastingLog.retrieve_fasting_log(events), "Should be (0, 0, 0, 0)")


if __name__ == '__main__':
    ActionSendFastingLog = ActionSendFastingLog()
    unittest.main()


