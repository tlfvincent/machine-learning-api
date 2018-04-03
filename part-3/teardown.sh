#!/bin/bash

docker rmi $(docker images -a -q)
docker rm $(docker ps -a -f status=exited -q)

docker-compose down

docker-compose stop api
docker-compose rm api

docker-compose stop db
docker-compose rm db

docker-compose stop data
docker-compose rm data

docker-compose stop loadbalancer
docker-compose rm loadbalancer

