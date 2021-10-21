#!/bin/sh
source .env
# Take from https://stackoverflow.com/a/3278427/3384529
git fetch

UPSTREAM=${1:-'@{u}'}
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse "$UPSTREAM")
BASE=$(git merge-base @ "$UPSTREAM")

#checar si hay cambios y actualizar codigo
if [ $LOCAL = $REMOTE ]; then
    echo "!!!EL REPO ESTA AL DIA!!!"
elif [ $LOCAL = $BASE ]; then
    echo "SE HAN DETECTADO NUEVOS CAMBIOS!"
    echo "> Deteniendo el container..."
    echo "> Actualizando cambios..."
    git pull
    docker-compose down
    echo "!!!CODIGO ACTUALIZADO!!!"
elif [ $REMOTE = $BASE ]; then
    echo "Has modificado codigo en local, comunicate con el administrador del repo o crea un fork para que puedas subir tus cambios"
fi


#mandar a correr
echo "> Mandar a correr el container..."
sh ./run.sh