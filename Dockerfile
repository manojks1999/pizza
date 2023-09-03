FROM python:latest

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN pip install flask celery redis flask-sqlalchemy flask-wtf uuid python-dotenv pymysql cryptography mysql-connector-python mysql-connector

WORKDIR /app