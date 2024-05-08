#!/bin/bash

# Check if there's an argument
if [ -z "$1" ]; then
  echo "Error: Please provide an argument."
  exit 1
fi

case $1 in
  help)
    echo "up|down|nginx|primary|replica"
    ;;
  nginx)
    docker compose -f litefs/docker-compose.yml up -d nginx
    ;;
  primary)
    docker compose -f litefs/docker-compose.yml up -d primary
    ;;
  replica)
    docker compose -f litefs/docker-compose.yml up -d nginx
    ;;
  up)
    docker compose -f litefs/docker-compose.yml up -d
    ;;
  down)
    docker compose -f litefs/docker-compose.yml down
    ;;
  *)
    echo "Invalid argument: '$1'"
    ;;
esac

