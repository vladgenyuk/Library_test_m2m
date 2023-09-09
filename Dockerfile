FROM python:3.11

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

env PYTHONDONTWRITEBYTECODE=1
env PYTHONUNBUFFERED=1

COPY . .
