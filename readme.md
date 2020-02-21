# Proyecto de aplicación de simulación de compra/ venta de criptomonedas para Bootcamp cero 4ª Edición.

La aplicación está instalada en un servidor de Amazon Web Services en la IP: 

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
4. Renombrar el archivo config_template.py a config.py; en SECRET_KEY escribir tu propia clave dentro de las comillas simples, esta clave no debe llevar comillas simples, tambien en API_KEY debes poner la key de acceso a la api de coinmarketcap; existe un tercer campo que es DB_KEY donde debes poner dentro de las comillas simples el nombre del fichero de la base de datos que viene incorporado y que es datos1.db.

5. Crear la variable de entorno `FLASK_APP` con el valor `<nombredefichero>.py`

6. Lanzar la aplicación
```
    flask run
```