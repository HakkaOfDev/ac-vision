FROM python:3.9-buster

RUN mkdir app
WORKDIR /app

ENV PATH="${PATH}:/root/.local/bin"
ENV PYTHONPATH="/app/src"
ENV PYTHONUNBUFFERED=1
ENV TZ Europe/Paris

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y tcpdump

COPY src/ .

CMD python3 src/main.py

