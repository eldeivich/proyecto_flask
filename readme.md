# Proyecto de aplicación de simulación de compra/ venta de criptomonedas para Bootcamp cero 4ª Edición.

La aplicación está instalada en un servidor de Amazon Web Services en la IP: 18.223.109.83

## Nos bajaremos la aplicación dándole a clone or download y copiándonos la dirección web, luego abrimos un terminal y nos ponemos en la ruta deseada, ejecutamos:
```
git clone <Dirección web de github copiada> <nombre que queramos dar a la aplicación>
```

### Abrimos la carpeta en nuestro Visual Studio Code y abrimos terminal.

# Instrucciones de instalación:

1. Crear el entorno virtual en el terminal a trabajar
```
    python -m venv <Nombre de entorno virtual>
```

2. Activar el entorno virtual
```
    Mac:
        . <Nombre de entono virtual>/bin/activate
    Linux:
        source/<Nombre de entorno virtual>/bin/activate
    Windows:
        <Nombre de entorno virtual>\Scripts\activate
```
3. Instalar las dependencias del fichero requirements.txt
```
    pip install -r requirements.txt
```
4. Renombrar el archivo config_template.py a config.py; en SECRET_KEY escribir tu propia clave dentro de las comillas simples, esta clave no debe llevar comillas simples; tambien en API_KEY (dentro de las comillas simples) debes poner la key de acceso a la api de coinmarketcap; existe un tercer campo que es DB_FILE donde debes poner dentro de las comillas simples el nombre del fichero de la base de datos que viene incorporado y que es datos1.db; guardamos los cambios.

4.1. También puedes optar por ponerle otro nombre al fichero de la base de datos, en DB_FILE puedes poner otro nombre acabado en .db; abrir un terminal, nos metemos en la ruta de la base de datos (en este caso datas), ejecutamos python y las siguientes instrucciones:
```
import sqlite3

conn = sqlite3.connect('<nombre que queramos dar a la base de datos terminado en .db>') [entre comillas simples]

cursor = conn.cursor()

query = """CREATE TABLE "cryptos" (
	"id"	INTEGER,
	"Symbol"	TEXT,
	"name"	TEXT,
	PRIMARY KEY("id")
);"""

query2 = """CREATE TABLE "movements" (
	"id"	INTEGER,
	"date"	TEXT,
	"time"	TEXT,
	"from_currency"	INTEGER,
	"from_quantity"	REAL,
	"to_currency"	INTEGER,
	"to_quantity"	REAL,
	PRIMARY KEY("id"),
	FOREIGN KEY("to_currency") REFERENCES "cryptos",
	FOREIGN KEY("from_currency") REFERENCES "cryptos"
);"""

cursor.execute(query)

cursor.execute(query2)

conn.commit()

conn.close()

exit()

```

5. Lanzar la aplicación
```
    flask run
```