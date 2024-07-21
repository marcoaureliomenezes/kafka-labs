#!/bin/bash



# stop all running containers

docker stop $(docker ps -a -q) && docker rm $(docker ps -a -q)

# remove all containers

docker rm $(docker ps -a -q)