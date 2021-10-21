#!/bin/sh

STATUS=$(docker ps -a | grep bpa-worker-py)
if [[ $STATUS =~ "Exited" ]]; then
  echo "El container esta muerto";
  echo "> Despertndo el contenedor..."
  docker-compose up -d
else
  echo "El container ya estaba corriendo!"
fi
