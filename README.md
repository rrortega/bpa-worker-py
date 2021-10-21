BPA WORKER  
===
Crawler para ejecutar tareas dentro de
https://bancaremota.bpa.cu

#AUTOUPDATES 
Para mantenerlo actualizado ejecutar en un crontab cada 1 min el ./crontab.sh

Abre un terminal unix y escribe
` crontab -e`

Luego escribe `* * * * * /path/to/crontab.sh >/dev/null 2>&1` modificando el path donde esta ubicado el script de forma absoluta

Guarda el crontab y listo! ya esta corriendo.



#VARIABLES DE ENTORNO

Crea un fichero con el nombre.env dentro del directorio del proyecto y ponle dentro las variables de entrono siguientes
#.env
    RETHINKDB_HOST="127.0.0.1" #El ip donde esta rethinkDB
    RETHINKDB_DATABASE="database" #El nombre de la base de datos
    RETHINKDB_PASSWORD="L4cl4v3*RethinkDb" #La contrasena de la base de datos