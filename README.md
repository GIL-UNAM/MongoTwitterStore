## Descripción general
Este es un programa que se encarga de recolectar de manera continua los twitts de una *región*y almacenarlos en un servidor Mongo (el servidor mongo empleado es 4.2.6). Por ejemplo, la *región* para México es: -117.61,14.34,-86.38,32.67.

Es importante indicar que el programa para trabajar emplea el api de twitter, la cual está limitada a recuperar una cierta cantidad de twitts por día.

Los twitts almacenado en mongo pueden ser consultados usando las bibliotecas de mongo y conectándose a el puerto correspondiente, para el caso del Grupo de Ingeniería Lingüística la información para conectarse a mongo es la siguiente:

* IP: 132.247.22.53:27017
* autenticación es SCRAM-SHA-256
* base de datos es twitterdb y la colección se llama tweetsMexico
* usuario con derechos exclusivamente de consulta es: ConsultaTwitter
* pass $Con$ulT@C0V1D. 
* Pueden emplear MongoCompas para probar la conexión o explotar la colección 

## Requisitos previos
### programas instalados
* MongoDB Community server
* Python3
* tweepy
* pymongo

### Archivo 
Requiere un archivo de configuración tipo texto  (denominado "almacen.conf") que contiene ocho renglones, la primeras cuatro las proporciona twitter para trabajar con su api y las ultimas cuatro corresponden a datos de configuración sobre el servidor

1. CONSUMER_KEY
2. CONSUMER_SECRET
3. ACCESS_TOKEN
4. ACCESS_TOKEN_SECRET

5. USUARIO_MONGO con derechos de escritura sobre la colección en la que se van a almacenar los twitts recuperados
6. PASSWORD DEL USUARIO MONGO 
7. SCRAM-SHA-256  (TIPO DE CONECCIÓN AL SERVIDOR)
8. ip y puerto de conexión al servidor mongo

## Ejecución
Para ejecutar el script es necesario que tanto el script como el archivo de configuración se encuentren en la misma carpeta.

El comando para ejecutar el programa y que qude de manera permanete, hasta que se apague la máquina o se detenga el proceso (comando *kill* de linux):

``` nohup python3 almacena.py& ```

Si se corre de manera *"normal"* 

``` python3 alamacena.py ```

El programa estará corriendo hasta que el usuario suspenda el programa (ctl-c)






