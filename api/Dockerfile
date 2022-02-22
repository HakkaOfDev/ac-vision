FROM python:3.9-buster

RUN mkdir app
WORKDIR /app

ENV PATH="${PATH}:/root/.local/bin"
ENV PYTHONPATH="/app/src"

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apt-get update && apt-get -y install snmp libsnmp-dev

COPY mibs/ /usr/share/snmp/mibs
COPY src/ . # ./src/main

CMD python3 ./src/main.py