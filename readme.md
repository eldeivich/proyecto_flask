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
4. Crear la variable de entorno `FLASK_APP` con el valor `<nombredefichero>.py`

5. Lanzar la aplicación
```
    flask run
```