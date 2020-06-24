FROM python:3.7-slim

WORKDIR '/app'

COPY requirements_src.txt .
RUN pip install -r requirements_src.txt
COPY setup.py .
RUN python setup.py develop

CMD python setup.py develop