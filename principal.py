import googlemaps
from datetime import datetime
import json
import sys
import numpy as np
import time

gmaps = []
lista_keys = open("google_keys.txt")
keys = lista_keys.read().splitlines()
lista_keys.close()
quantidade_total_keys = len(keys)
for key in keys:
    gmaps.append(googlemaps.Client(key))



if(len(sys.argv) != 3):
    print "Argumento invalido"
    print "Exemplo de entrada:python principal.py 480"
    sys.exit()
else:
    nome_cidade = raw_input("Digite o nome da cidade:")
    tamanho_matriz_x = int(sys.argv[1])
    tamanho_matriz_y = int(sys.argv[2])
    fator_x = float(sys.argv[1])/10000
    fator_y = float(sys.argv[2])/10000
    tamanho_total = tamanho_matriz_x * tamanho_matriz_y
    print tamanho_total
    quantidade_suportada = quantidade_total_keys * 2500
    print quantidade_suportada
    if(tamanho_total > quantidade_suportada):
        print "Tamanho de matriz muito grande"
        sys.exit()


geocode_result = gmaps[10].geocode(nome_cidade)
if(len(geocode_result) == 0):
    print "Nome de cidade invalido"
    sys.exit()

lat = geocode_result[0]["geometry"]["location"]["lat"]
lng = geocode_result[0]["geometry"]["location"]["lng"]

nome_arquivo = "" + nome_cidade + ".mat"
recuo_lat = lat - (fator_x * tamanho_matriz_x)
recuo_lng = lng - (fator_y * tamanho_matriz_y)
arquivo = open(nome_arquivo,"w")
cabecalho = "c " + str(tamanho_matriz_x) + " " + str(tamanho_matriz_y) + "\n"
arquivo.write(cabecalho)
arquivo.close()
matriz_gerada = []
linha = []
contador_keys = 0
key_number = 10
for i in range(tamanho_matriz_x):
    linha = []
    for j in range(tamanho_matriz_y):
        print recuo_lat,recuo_lng
        try:
            altura = gmaps[key_number].elevation((recuo_lat, recuo_lng))
        except googlemaps.exceptions.Timeout:
            print "trocando chave"
            key_number += 1
            if(key_number > quantidade_total_keys):
                print "Quantidade de chaves insuficiente"
                sys.exit()
            continue

        if(altura[0]["elevation"] < 0):
            altura[0]["elevation"] = 0
        print altura[0]["elevation"]
        linha.append(altura[0]["elevation"])
        recuo_lng += fator_y
    matriz_gerada.append(linha)
    recuo_lat += fator_x

print matriz_gerada
matriz_convertida = np.array(matriz_gerada)
matrix = np.matrix(matriz_convertida)
with open(nome_cidade,'a') as f:
    for line in matrix:
        np.savetxt(f, line, fmt='%.2f')