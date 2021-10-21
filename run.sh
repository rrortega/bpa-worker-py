#!/bin/sh

STATUS=$(docker ps -a | grep bpa-worker-py)
if [[ $STATUS =~ "Exited" ]]; then
  echo "El container esta muerto";
  echo "> Despertndo el contenedor..."
  source .env
  docker-compose up -d
else
  echo "El container esta corriendo!"
fi
