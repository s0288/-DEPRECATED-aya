# purpose
- aya is a telegram chatbot that helps users implement fasting into their lifestyle

# service structure
- rasa: aya's core speaking capability
- actions: custom actions server for rasa
- flask: 
  - send msgs to user
- telegram: 
  - receive msgs from user or triggers
- cron: set up triggers

# local set up
- aya runs in a series of docker containers (see docker-compose.yml). For local setup, the following is recommended:
  - conda create -n aya python=3.6.12
  - pip install rasa
  - pip install pytest
  - in the base directory, run "pip install ."