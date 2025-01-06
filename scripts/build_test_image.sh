#!/bin/bash
sudo apt-get update
sudo apt-get -y install curl

docker build . -f .Dockerfile -t hivebox:local-ci
docker run -d -p 8000:8000 hivebox:local-ci

sleep 10

## curl -s -o /dev/null -w "%{http_code}" localhost:8000/version || { echo '/version endpoint call failed; exiting...' ; exit 1; }

STATUSCODE=$(curl -silent -output /dev/null -w "%{http_code}" http://localhost:8000/version)

if test $STATUSCODE -ne 200; then
    echo '/version endpoint call failed; exiting...'
    exit 1
fi
