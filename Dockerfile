FROM python:3-buster

WORKDIR /usr/src/app

RUN pip install -U pip \
  && pip install neo4j Flask Flask-Cors gunicorn

COPY ./backend .

CMD gunicorn --bind 0.0.0.0:$PORT api:app
