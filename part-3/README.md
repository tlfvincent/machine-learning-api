# PART 3: Monitoring your Machine Learning API with Prometheus

## Usage

1. Build Docker image and tag as ml-api

```
docker-compose -f docker-compose.yml -f docker-compose-infra.yml build
```


```
docker-compose -f docker-compose.yml -f docker-compose-infra.yml up -d --scale api=7
```


port `9090` will show the Prometheus graph