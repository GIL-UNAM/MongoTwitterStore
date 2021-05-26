
# coding: utf-8
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from pymongo import MongoClient

import os
import tweepy
import urllib.parse
import time

streamStarted = False

# --------------------------------------------
# leer el archivo de configuracion del crawler
# --------------------------------------------

conf = []
with open("./almacena.conf","r") as f:
    for r in f:
        conf.append(r.strip('\n\t'))

# --------------------------------------------
# Se conecta al servidor remoto
# --------------------------------------------

print("conectando con mongo remoto... ",end='')
client = MongoClient(host=conf[8],username=conf[4],password=conf[5],authSource=conf[6],authMechanism=conf[7])
assert client != None
print("ok")

print("conectando con db... ",end='')
db = client.twitterdb
print("ok")

# --------------------------------------------
# Se conecta con wl api de tweeter
# --------------------------------------------

MEXICO_CONSUMER_KEY = conf[0]
MEXICO_CONSUMER_SECRET = conf[1]
MEXICO_ACCESS_TOKEN = conf[2]
MEXICO_ACCESS_TOKEN_SECRET = conf[3]



print("Autorizando Twitter API... ",end='')
auth = OAuthHandler(MEXICO_CONSUMER_KEY,MEXICO_CONSUMER_SECRET)
auth.set_access_token(MEXICO_ACCESS_TOKEN, MEXICO_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
print('ok')



class TwitterListener(StreamListener):

        k = 0
        # Funcion que procesa data y verifica si el tweet es de Mexico
        def on_status(self, tweet):
                if tweet:
                    if tweet.place.country_code == 'MX':
                        print('({} {}) = '.format(time.strftime("%c"),self.k),tweet.id,end='')                        
                        print("*",end = '');
                        try:
                            db.tweetsMexico.insert(tweet._json)
                            print(" inserted")
                            self.k = self.k+1
                        except Exception as inst:
                            print(" ignored (is duplicated?): ",inst)
                return True

        # Funcion que maneja los codigos de error
        def on_error(self, status):
                global streamStarted
                print("Error: ",end='')
                if status == 400:
                        print ('Error 400: Peticion invalida')
                elif status == 401:
                        print ('Error 401: Error en la autenticacion')
                elif status == 404:
                        print ('Error 404: Revisar a donde se hace la peticion')
                elif status == 406:
                        print ('Error 406: Error en el formato de las peticiones')
                elif status == 420:
                        print ('Error 420: Demasiadas peticiones!')
                        time.sleep(60)   
                else:
                    print(time.ctime(seconds),"desconocido...")
                streamStarted = False
                return False # kill the stream



print("TwitterListener() ... ",end='')
listener = TwitterListener()
print("ok")
print("Stream() ... ",end='')
stream = Stream(auth, listener)
print("ok")

# Mexico: -117.61,14.34,-86.38,32.67

while True:
    try:
                # https://boundingbox.klokantech.com/  format csv 
        if not streamStarted:
            print("arrancando un nuevo stream...")
            streamStarted = True
            stream.filter(locations=[-117.61,14.34,-86.38,32.67])
        print("*",end='')
    except Exception as inst:
        print("stream exception: ",inst)        
    finally:
        stream.disconnect()
        streamStarted = False
        print("Closed by finally")
        
    
        

