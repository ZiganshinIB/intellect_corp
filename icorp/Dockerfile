FROM python:3.9
LABEL authors="ilmir.ziganshin"

RUN apt-get update -y && pip install --upgrade pip
WORKDIR /opt/project
COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN python manage.py migrate
COPY . .