# Medical Diagnosis - API

## How to run

```
# build image
docker build . -t "md-api"

# start
docker run -d -p 5000:5000 --name md-api md-api
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
