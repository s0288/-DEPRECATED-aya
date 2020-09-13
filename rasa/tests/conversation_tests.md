#### This file contains tests to evaluate that your bot behaves as expected.
#### If you want to learn more, please see the docs: https://rasa.com/docs/rasa/user-guide/testing-your-assistant/

## start
* start: /start
  - utter_start
* mood_great: gut
  - utter_happy

## fast end 1
* fast_end: ende
  - action_fasting_since
  - slot{"is_fasting" : 1}
  - utter_ask_end_fast
* affirm: ja
  - utter_end_fast
  - action_end_fast
  - slot{"is_fasting" : 0}

## fast start yes
* fast_start: start
  - action_fasting_since
  - slot{"is_fasting" : 0}
  - utter_ask_fast
* affirm: jo
  - utter_start_fast
  - action_start_fast
  - slot{"is_fasting" : 1}