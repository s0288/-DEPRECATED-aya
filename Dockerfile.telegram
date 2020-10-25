FROM python:3.7-slim

WORKDIR '/app'

# install dependencies
COPY requirements_src.txt .
RUN pip install -r requirements_src.txt
# install module
COPY setup.py .
RUN python setup.py develop

# mount relevant directories
COPY ./telegram ./telegram
COPY ./src ./src

CMD cd /app/telegram/ && python run_telegram.py