"""
Test functions for custom actions in actions.py
"""
import pytest
from datetime import datetime, timedelta

from rasa.src.actions import ActionSendOverview


EVENTS_W_FASTING_HISTORY = [
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
            "name": "total_hours_fasted", "value": 13.9833333333334},
        {'event': 'user', 'timestamp': datetime.timestamp(datetime(datetime.now().year, 
            datetime.now().month, datetime.now().day, 10, 0) - timedelta(days=0)), 'text': 'hi', 
            'parse_data': {
                'intent': {'id': 5975626392428980550, 'name': 'greet', 'confidence': 0.9817644357681274}, 
                'entities': [], 'text': 'hi', 'message_id': 'cbe7ea58a4fb4f2cb1f04fc591104e40', 'metadata': {}, 
                'intent_ranking': [{'id': 5975626392428980550, 'name': 'greet', 'confidence': 0.9817644357681274}, 
                    {'id': 3301564811817334879, 'name': 'how_are_you', 'confidence': 0.007583854254335165}], 
                'response_selector': {'all_retrieval_intents': [], 'default': {
                    'response': {'id': None, 'response_templates': None, 'confidence': 0.0, 'intent_response_key': None, 'template_name': 'utter_None'}, 
                    'ranking': []}}}, 'input_channel': 'callback', 'message_id': 'cbe7ea58a4fb4f2cb1f04fc591104e40', 'metadata': {}}
    ]
EVENTS_WO_FASTING_HISTORY = [
        {'event': 'user', 'timestamp': datetime.timestamp(datetime(datetime.now().year, 
            datetime.now().month, datetime.now().day, 10, 0) - timedelta(days=0)), 'text': 'hi', 
            'parse_data': {
                'intent': {'id': 5975626392428980550, 'name': 'greet', 'confidence': 0.9817644357681274}, 
                'entities': [], 'text': 'hi', 'message_id': 'cbe7ea58a4fb4f2cb1f04fc591104e40', 'metadata': {}, 
                'intent_ranking': [{'id': 5975626392428980550, 'name': 'greet', 'confidence': 0.9817644357681274}, 
                    {'id': 3301564811817334879, 'name': 'how_are_you', 'confidence': 0.007583854254335165}], 
                'response_selector': {'all_retrieval_intents': [], 'default': {
                    'response': {'id': None, 'response_templates': None, 'confidence': 0.0, 'intent_response_key': None, 'template_name': 'utter_None'}, 
                    'ranking': []}}}, 'input_channel': 'callback', 'message_id': 'cbe7ea58a4fb4f2cb1f04fc591104e40', 'metadata': {}}
    ]


@pytest.mark.parametrize(
    "events, days_in_period, expected", [
        (
            EVENTS_W_FASTING_HISTORY, 
            2,
            [
                {"event": "slot", "timestamp": datetime.timestamp(datetime(datetime.now().year, 
                    datetime.now().month, datetime.now().day, 11, 0) - timedelta(days=1)), 
                    "name": "total_hours_fasted", "value": 18.983333333333334}, 
                {"event": "slot", "timestamp": datetime.timestamp(datetime(datetime.now().year, 
                    datetime.now().month, datetime.now().day, 11, 0) - timedelta(days=0)), 
                    "name": "total_hours_fasted", "value": 13.9833333333334},
                {'event': 'user', 'timestamp': datetime.timestamp(datetime(datetime.now().year, 
                    datetime.now().month, datetime.now().day, 10, 0) - timedelta(days=0)), 'text': 'hi', 
                    'parse_data': {
                        'intent': {'id': 5975626392428980550, 'name': 'greet', 'confidence': 0.9817644357681274}, 
                        'entities': [], 'text': 'hi', 'message_id': 'cbe7ea58a4fb4f2cb1f04fc591104e40', 'metadata': {}, 
                        'intent_ranking': [{'id': 5975626392428980550, 'name': 'greet', 'confidence': 0.9817644357681274}, 
                            {'id': 3301564811817334879, 'name': 'how_are_you', 'confidence': 0.007583854254335165}], 
                        'response_selector': {'all_retrieval_intents': [], 'default': {
                            'response': {'id': None, 'response_templates': None, 'confidence': 0.0, 'intent_response_key': None, 'template_name': 'utter_None'}, 
                            'ranking': []}}}, 'input_channel': 'callback', 'message_id': 'cbe7ea58a4fb4f2cb1f04fc591104e40', 'metadata': {}}
            ]
        ), (
            EVENTS_WO_FASTING_HISTORY, 
            2,
            [
                {'event': 'user', 'timestamp': datetime.timestamp(datetime(datetime.now().year, 
                    datetime.now().month, datetime.now().day, 10, 0) - timedelta(days=0)), 'text': 'hi', 
                    'parse_data': {
                        'intent': {'id': 5975626392428980550, 'name': 'greet', 'confidence': 0.9817644357681274}, 
                        'entities': [], 'text': 'hi', 'message_id': 'cbe7ea58a4fb4f2cb1f04fc591104e40', 'metadata': {}, 
                        'intent_ranking': [{'id': 5975626392428980550, 'name': 'greet', 'confidence': 0.9817644357681274}, 
                            {'id': 3301564811817334879, 'name': 'how_are_you', 'confidence': 0.007583854254335165}], 
                        'response_selector': {'all_retrieval_intents': [], 'default': {
                            'response': {'id': None, 'response_templates': None, 'confidence': 0.0, 'intent_response_key': None, 'template_name': 'utter_None'}, 
                            'ranking': []}}}, 'input_channel': 'callback', 'message_id': 'cbe7ea58a4fb4f2cb1f04fc591104e40', 'metadata': {}}
            ]
        )
    ],
        ids=[
            "w_fasting_history_and_2d_in_period",
            "wo_fasting_history_and_2d_in_period"
            ]
)
def test_action_send_overview__get_events_for_period(events, days_in_period, expected):
    assert ActionSendOverview._get_events_for_period(events, days_in_period) == expected


@pytest.mark.parametrize(
    "events, expected", [
        (EVENTS_W_FASTING_HISTORY, 18.983333333333334),
        (EVENTS_WO_FASTING_HISTORY, 0)
        ],
        ids=["w_fasting_history_and_2d_in_period",
            "wo_fasting_history_and_2d_in_period"]
)
def test_action_send_overview__calculate_median_hours_fasted(events, expected):
    assert ActionSendOverview._calculate_median_hours_fasted(events) == expected


@pytest.mark.parametrize(
    "events, expected", [
        (EVENTS_W_FASTING_HISTORY, 0),
        (EVENTS_WO_FASTING_HISTORY, 0)
        ],
        ids=["w_fasting_history_and_2d_in_period",
            "wo_fasting_history_and_2d_in_period"]
)
def test_action_send_overview__calculate_days_w_24h_or_more(events, expected):
    assert ActionSendOverview._calculate_days_w_24h_or_more(events) == expected


@pytest.mark.parametrize(
    "events, expected", [
        (EVENTS_W_FASTING_HISTORY, 3),
        (EVENTS_WO_FASTING_HISTORY, 0)],
        ids=["w_fasting_history_and_2d_in_period",
            "wo_fasting_history_and_2d_in_period"]
)
def test_action_send_overview__calculate_total_days_fasted(events, expected):
    assert ActionSendOverview._calculate_total_days_fasted(events) == expected

