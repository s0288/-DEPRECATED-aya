<!-- basic stories -->
## start
* start
  <!-- action_add_user -->
  - utter_start
* mood_great
  - utter_happy

## happy path
* greet
  - utter_greet
* mood_great
  - utter_happy

## how are you
* greet
  - utter_greet
* how_are_you
  - utter_I_am_fine

## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_express_empathy
* affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_express_empathy
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
  - utter_ask_fast
* affirm
  - utter_start_fast
  - action_start_fast

## fast length without fasting no
* fast_length_so_far
  - action_fasting_since
  - slot{"is_fasting" : 0}
  - utter_ask_fast
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
  
## fast end 2
* fast_end
  - action_fasting_since
  - slot{"is_fasting" : 1}
  - utter_ask_end_fast
* deny
  - utter_ok

  <!-- journal-specific stories -->
