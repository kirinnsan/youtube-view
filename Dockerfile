FROM python:3.9

WORKDIR /app

RUN apt-get update && apt-get install -y vim

RUN pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib pandas dash==1.18.1

COPY . .

ENV LANG=ja_JP.UTF-8 \
    LANGUAGE=ja_JP:ja \
    LC_ALL=ja_JP.UTF-8
