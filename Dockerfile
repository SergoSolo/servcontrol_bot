FROM python:3.10-slim

WORKDIR /app_bot

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .
