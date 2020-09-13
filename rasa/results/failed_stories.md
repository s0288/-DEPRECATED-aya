## start (/var/folders/3q/0kc97kj14bn3gr7n5vp_jb5r0000gn/T/tmprnd5nn46/c4bc11c3b47f4192baf7762551a7ce69_conversation_tests.md)
* start: /start
    - utter_start
* mood_great: gut   <!-- predicted: mood_great: [gut](happy) -->
    - utter_happy


## fast start yes (/var/folders/3q/0kc97kj14bn3gr7n5vp_jb5r0000gn/T/tmprnd5nn46/c4bc11c3b47f4192baf7762551a7ce69_conversation_tests.md)
* fast_start: start
    - action_fasting_since
    - slot{"is_fasting": 0}
    - utter_ask_fast
* affirm: jo   <!-- predicted: deny: jo -->
    - utter_start_fast   <!-- predicted: utter_ok -->
    - action_start_fast
    - slot{"is_fasting": 1}


