import googlemaps
from datetime import datetime
import json
import sys
import numpy as np
gmaps = googlemaps.Client(key='AIzaSyDZ2JmlQU6FeQobRyrfD4qWwuWea_TNyyQ')

if(len(sys.argv) != 2):
    print "Argumento invalido"
    print "Exemplo de entrada:python principal.py 480"
    sys.exit()
else:
    nome_cidade = raw_input("Digite o nome da cidade:")
    tamanho_matriz = int(sys.argv[1])
    fator = float(sys.argv[1])/10000
    print fator

# Geocoding an address
geocode_result = gmaps.geocode(nome_cidade)
if(len(geocode_result) == 0):
    print "Nome de cidade invalido"
    sys.exit()

lat = geocode_result[0]["geometry"]["location"]["lat"]
lng = geocode_result[0]["geometry"]["location"]["lng"]




recuo_lat = lat - (fator * tamanho_matriz)
recuo_lng = lng - (fator * tamanho_matriz)

print fator
matriz_gerada = []

for i in range(tamanho_matriz):
    for j in range(tamanho_matriz):
        altura = gmaps.elevation((recuo_lat,recuo_lng))
        print altura[0]["elevation"]
        recuo_lng += fator

    recuo_lat += fator
