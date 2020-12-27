'''

Unit tests for 

'''

import unittest
import datetime
from rasa.actions import ActionSendFastingLog


class TestActionSendFastingLog(unittest.TestCase):
    # tests for ActionSendFastingLog
    def test_retrieve_fasting_log_with_user_that_has_fasting_history(self):
        events = [{"event": "slot", "timestamp": 1608640640.1106675, "name": "total_hours_fasted", "value": 18.983333333333334}, {"event": "slot", "timestamp": 1608814999.6153653, "name": "total_hours_fasted", "value": 22.616666666666667}, {'event': 'slot', 'timestamp': 1600619208.9505951, 'name': 'mins_fasted', 'value': '53 Minuten'}, {'event': 'slot', 'timestamp': 1600619208.9506164, 'name': 'is_fasting', 'value': 1}] # test events
        self.assertEqual((41.6, 20.8, 22.616666666666667), ActionSendFastingLog.retrieve_fasting_log(events), "Should be (41.6, 20.8, 22.616666666666667)")

    def test_retrieve_fasting_log_with_user_that_does_not_have_fasting_history(self):        
        events = [{'event': 'slot', 'timestamp': 1600619208.9505951, 'name': 'mins_fasted', 'value': '53 Minuten'}, {'event': 'slot', 'timestamp': 1600619208.9506164, 'name': 'is_fasting', 'value': 1}] # test events
        self.assertEqual((0, 0, 0), ActionSendFastingLog.retrieve_fasting_log(events), "Should be (0, 0, 0)")


if __name__ == '__main__':
    ActionSendFastingLog = ActionSendFastingLog()
    unittest.main()