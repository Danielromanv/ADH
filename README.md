# ADH
Agregador de Hosts

## Si se utiliza docker:
La aplicación requiere de:
```
Docker 17.03.1-ce +
o
Docker EE 17.03.0-ee-1 +
docker-compose
```

#### Para instalar las imágenes necesarias:
```
docker-compose build
```

#### Para ejecutar los contenedores:
```
docker-compose up -d
```
La aplicación se ejecutará en el puerto 8080: [localhost:8080](127.0.0.1:8080)

## Si se utiliza un entorno virtual:
La aplicación requiere de:

```
Python 3.5+
pip 9.0+
virtualenv 15.0+
nmap
```

#### Para instalar el entorno virtual ejecutar:
```
virtualenv -p python<version> env
```
#### Para activar el entorno virtual:
```
source env/bin/activate
```
#### Para instalar dependencias:
```
pip install -r requirements.txt
```
#### Finalmente para ejecutar la aplicación web:
```
python server.py
```
La aplicación se ejecutará en el puerto 8080: [http://localhost:8080](http://localhost:8080)
