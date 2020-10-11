<!-- basic stories -->
## start
* start
  - utter_start
* mood_great
  - utter_happy

## how are you
* greet
  - utter_greet
* how_are_you
  - utter_I_am_fine
* affirm
  - utter_ok

## happy path
* greet
  - utter_greet
* mood_great
  - utter_happy

## sad path yes
* greet
  - utter_greet
* mood_unhappy
  - utter_express_empathy
  - utter_ask_talk
* affirm
  - reflect_day_form
  - form{"reflectsituation": "reflect_day_form"}
  - action_deactivate_form
  - form{"reflectsituation": null}
  - utter_thank_you

## sad path no
* greet
  - utter_greet
* mood_unhappy
  - utter_express_empathy
  - utter_ask_talk
* deny
  - utter_ok

## say no problem
* no_problem
  - utter_no_problem

## say goodbye
* goodbye
  - utter_goodbye

<!-- fasting-specific stories -->
## fast start yes
* fast_start
  - action_fasting_since
  - slot{"is_fasting" : 0}
  - utter_ask_fast
* affirm
  - utter_start_fast
  - action_start_fast
  - slot{"is_fasting" : 1}

## fast start no
* fast_start
  - action_fasting_since
  - slot{"is_fasting" : 0}
  - utter_ask_fast
* deny
  - utter_ok

## fast start while fasting
* fast_start
  - action_fasting_since
  - slot{"is_fasting" : 1}
  - utter_info_fast

## fast length while fasting
* fast_length_so_far
  - action_fasting_since
  - slot{"is_fasting" : 1}
  - utter_info_fast

## fast length without fasting yes
* fast_length_so_far
  - action_fasting_since
  - slot{"is_fasting" : 0}
  - utter_info_not_fasting_ask_fast
* affirm
  - action_start_fast
  - slot{"is_fasting" : 1}
  - utter_start_fast

## fast length without fasting no
* fast_length_so_far
  - action_fasting_since
  - slot{"is_fasting" : 0}
  - utter_info_not_fasting_ask_fast
* deny
  - utter_ok

## fast end 1
* fast_end
  - action_fasting_since
  - slot{"is_fasting" : 1}
  - utter_ask_end_fast
* affirm
  - utter_end_fast
  - action_end_fast
  - slot{"is_fasting" : 0}

## fast end 2
* fast_end
  - action_fasting_since
  - slot{"is_fasting" : 1}
  - utter_ask_end_fast
* deny
  - utter_ok

## fast reminder
* fast_reminder
  - action_fasting_since
  - utter_reminder_fast

<!-- health-data-specific stories -->
## weight add yes
* weight_add
  - utter_ask_weight
* affirm
  - utter_ask_weight_value
* weight_value
  - action_entity_extract
  - utter_noted  

## weight add no
* weight_add
  - utter_ask_weight
* deny
  - utter_ok

## weight value
* weight_value
  - action_entity_extract
  - utter_noted  

<!-- journal-specific stories -->
## reflect day yes
* reflect_day
  - utter_ask_talk
* affirm
  - reflect_day_form
  - form{"reflect_situation": "reflect_day_form"}
  - action_deactivate_form
  - form{"reflect_situation": null}
  - utter_thank_you

## reflect day no
* reflect_day
  - utter_ask_talk
* deny
  - utter_ok

<!-- ## reflect day stop but continue
* reflect_day
  - reflect_day_form
  - form{"reflect_situation": "reflect_day_form"}
  - form{"reflect_situation": null}
  - utter_thank_you -->

<!-- ## reflect day stop
* reflect_day
  - reflect_day_form
  - form{"reflect_situation": "reflect_day_form"}
  - form{"reflect_situation": null}
  - utter_thank_you -->