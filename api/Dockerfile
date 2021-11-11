FROM python:3.9-buster

RUN mkdir app
WORKDIR ./app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY src/ .