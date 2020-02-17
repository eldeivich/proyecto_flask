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
4. Renombrar el archivo config_template.py a config.py y en SECRET_KEY escribir tu propia clave dentro de las comillas simples, esta clave no debe llevar comillas simples, tambien en API_KEY debes poner la key de acceso a la api de coinmarketcap.

5. Crear la variable de entorno `FLASK_APP` con el valor `<nombredefichero>.py`

6. Lanzar la aplicación
```
    flask run
```