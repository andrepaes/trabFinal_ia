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
    print "Exemplo de entrada:python principal.py 480 480"
    sys.exit()
else:
    nome_cidade = raw_input("Digite o nome da cidade:")
    tamanho_matriz_x = int(sys.argv[1])
    tamanho_matriz_y = int(sys.argv[2])
    fator_x = float(sys.argv[1])/10000
    fator_y = float(sys.argv[2])/10000
    tamanho_total = tamanho_matriz_x * tamanho_matriz_y
    print tamanho_total
    quantidade_suportada = float(quantidade_total_keys * 2000)
    ratio_coordenadas = round(tamanho_total / quantidade_suportada)
    if(ratio_coordenadas == 0):
        ratio_coordenadas = 1
    print ratio_coordenadas



geocode_result = gmaps[0].geocode(nome_cidade)
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
key_number = 0
quantidade_ciclos = 0
alturas = []
for i in range(tamanho_matriz_x):
    alturas.append([])
# zera toda a matriz com excecao dos pontos escolhidos para calcular altura
for i in range(tamanho_matriz_x):
    linha = []
    for j in range(tamanho_matriz_y):
        print recuo_lat,recuo_lng
        if((quantidade_ciclos % ratio_coordenadas) == 0):
            try:
                altura = gmaps[key_number].elevation((recuo_lat, recuo_lng))
                alturas[i].append(altura[0]["elevation"])
            except googlemaps.exceptions.Timeout:
                print "trocando chave"
                key_number += 1
                if(key_number >= quantidade_total_keys):
                    print "Quantidade de chaves insuficiente"
                    sys.exit()
                continue
        else:
            altura[0]["elevation"] = 0

        if(altura[0]["elevation"] < 0):
            altura[0]["elevation"] = 0

        print altura[0]["elevation"]
        linha.append(altura[0]["elevation"])
        recuo_lng += fator_y
        quantidade_ciclos += 1
    matriz_gerada.append(linha)
    recuo_lat += fator_x

matriz_convertida = np.array(matriz_gerada)
matrix = np.matrix(matriz_convertida)
with open("teste.mat",'w') as f:
    for line in matrix:
        np.savetxt(f, line, fmt='%.2f')

quantidade_ciclos = 0
if(ratio_coordenadas > 1):
    for i in range(tamanho_matriz_x):
        j_alturas = 1
        for j in range(tamanho_matriz_y):
            if(quantidade_ciclos % ratio_coordenadas == 0):
                if (j_alturas < len(alturas[i])):
                    media_alturas = (alturas[i][j_alturas - 1] - alturas[i][j_alturas]) / ratio_coordenadas
                    j_alturas += 1
            else:
                if (j_alturas == len(alturas[i])):
                    media_alturas = (alturas[i][j_alturas])
                if (j == 0):
                    media_alturas = alturas[i][j_alturas-1] / ratio_coordenadas
                    j_alturas += 1

                matriz_gerada[i][j] = alturas[i][j_alturas - 1] + media_alturas




matriz_convertida = np.array(matriz_gerada)
matrix = np.matrix(matriz_convertida)
with open(nome_arquivo,'a') as f:
    for line in matrix:
        np.savetxt(f, line, fmt='%.2f')