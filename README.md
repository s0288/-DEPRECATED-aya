# LOCAL SETUP
- set relevant environment variables in .zshrc (in HOME): "cd ~/.zshrc"
- in .zshrc: "export VAR1=xyz"

# DOCKER-COMPOSE SETUP
- set relevant environment variables in .env (in project): "touch PROJECT_FOLDER/.env
- in .env: "VAR1=xyz"
- in docker-compose, set environment variables as below
    - environment:
        - VAR1=${VAR1}