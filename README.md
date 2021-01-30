# Medical Diagnosis - API

## Dependencies

To use this project you should have docker installed.

## How to run

```
# build image
docker build . -t "md-api"

# start
docker run -d -e "PORT=5000" -p 5000:5000 --name md-api md-api
```

## How to deploy on heroku

```
# build image
docker build . -t "web"

# push container
heroku container:push web -a <HEROKU_APP_NAME>

# release container
heroku container:release web -a <HEROKU_APP_NAME>

# scale the service
heroku ps:scale web=1 -a <HEROKU_APP_NAME>
```

## Generate Script

necessário conter o modulo neo4j

```
pip3 install neo4j
```

Para popular o neo4j com dados genéricos, è utilizado o script:

```
python3 src/load_data.py
```
