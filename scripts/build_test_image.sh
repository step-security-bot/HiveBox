#!/bin/bash
sudo apt-get update
sudo apt-get -y install curl

docker build . -f .Dockerfile -t hivebox:local-ci
docker run -d -p 8000:8000 hivebox:local-ci

curl -s -o /dev/null -w "%{http_code}" localhost:8000/version || { echo '/version endpoint call failed; exiting...' ; exit 1; }
