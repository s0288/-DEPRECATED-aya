#### This file contains tests to evaluate that your bot behaves as expected.
#### If you want to learn more, please see the docs: https://rasa.com/docs/rasa/user-guide/testing-your-assistant/

## start
* start: /start
  - utter_start
* mood_great: gut
  - utter_happy

## greet
* greet: hi
  - utter_greet
* mood_great: gut
  - utter_happy

## fast end 1 // "ende"
* fast_end: ende
  - action_fasting_since
  - slot{"is_fasting" : 1}
  - utter_ask_end_fast
* affirm: ja
  - utter_end_fast
  - action_end_fast
  - slot{"is_fasting" : 0}

## fast end 2 // "stopp"
* fast_end: stopp
  - action_fasting_since
  - slot{"is_fasting" : 1}
  - utter_ask_end_fast
* affirm: ja
  - utter_end_fast
  - action_end_fast
  - slot{"is_fasting" : 0}

## fasten start yes 1 // basic
* fasten: fasten
  - action_fasting_since
  - slot{"is_fasting" : 0}
  - utter_ask_fast
* affirm: ja
  - utter_start_fast
  - action_start_fast
  - slot{"is_fasting" : 1}

## fasten start yes 2 // command
* fasten: /fasten
  - action_fasting_since
  - slot{"is_fasting" : 0}
  - utter_ask_fast
* affirm: ja
  - utter_start_fast
  - action_start_fast
  - slot{"is_fasting" : 1}

## recipes 1 // command 1
* rezepte: /rezepte
  - utter_send_recipes

## recipes 2 // command 2
* rezepte: /rezept
  - utter_send_recipes

## uebersicht 1 // command
* uebersicht: /uebersicht
  - action_send_fasting_log

## uebersicht 2 // basic
* uebersicht: Übersicht
  - action_send_fasting_log
