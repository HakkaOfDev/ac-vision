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
COPY src/ .

CMD uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
CMD uvicorn src.main:app_ws --reload --host 0.0.0.0 --port 6969