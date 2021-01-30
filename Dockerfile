FROM python:3-buster

WORKDIR /usr/src/app

RUN pip install -U pip \
  && pip install neo4j Flask Flask-Cors

COPY . .

CMD [ "python", "backend/api.py" ]
