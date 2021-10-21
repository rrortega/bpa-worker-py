Worker de BPA para ejecutar en Cuba debajo de la red nacional con acceso a https://bancaremota.bpa.cu
===


AUTOUPDATES
---
Para mantenerlo actualizado ejecutar en un crontab cada 1 min el ./crontab.sh

Abre un terminal unix y escribe
` crontab -e`

Luego escribe `* * * * * /path/to/crontab.sh >/dev/null 2>&1` modificando el path donde esta ubicado el script de forma absoluta

Guarda el crontab y listo! ya esta corriendo.


