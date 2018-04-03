#!/bin/bash

docker rmi $(docker images -a -q)
docker rm $(docker ps -a -f status=exited -q)

docker-compose down

docker-compose stop api
docker-compose rm api

docker-compose stop loadbalancer
docker-compose rm loadbalancer

