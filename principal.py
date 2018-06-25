import googlemaps
import sys
import numpy as np

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
    fator_x = float(sys.argv[1])/100000
    fator_y = float(sys.argv[2])/100000
    tamanho_total = tamanho_matriz_x * tamanho_matriz_y
    print tamanho_total
    quantidade_suportada = float(quantidade_total_keys * 2000)
    ratio_coordenadas = round(tamanho_total / quantidade_suportada)
    if(ratio_coordenadas == 0):
        ratio_coordenadas = 1
    ratio_coordenadas=10
    print ratio_coordenadas



geocode_result = gmaps[0].geocode(nome_cidade)
if(len(geocode_result) == 0):
    print "Nome de cidade invalido"
    sys.exit()

lat = geocode_result[0]["geometry"]["location"]["lat"]
lng = geocode_result[0]["geometry"]["location"]["lng"]

nome_arquivo = "" + nome_cidade + ".mat"
recuo_lat = lat + abs(fator_x * (tamanho_matriz_x / 2))
recuo_lng = lng - abs(fator_y * (tamanho_matriz_y / 2))
aux_lng = recuo_lng
arquivo = open(nome_arquivo,"w")
cabecalho = "c " + str(tamanho_matriz_x) + " " + str(tamanho_matriz_y) + "\n"
arquivo.write(cabecalho)
arquivo.close()
matriz_gerada = []
linha = []
contador_keys = 0
key_number = 1
quantidade_ciclos = 0
alturas = []
i = 0
while(i < tamanho_matriz_x):
    alturas.append([])
    i += 1

i = 0
# zera toda a matriz com excecao dos pontos escolhidos para calcular altura
while(i < tamanho_matriz_x):
    linha = []
    recuo_lng = aux_lng
    j = 0
    while (j < tamanho_matriz_y):
        if((quantidade_ciclos % ratio_coordenadas) == 0):
            try:
                altura = gmaps[key_number].elevation((recuo_lat, recuo_lng))
                print "antes"
                alturas[i].append(altura[0]["elevation"])
                print i,j
                print "depois"
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

        linha.append(altura[0]["elevation"])
        recuo_lng += abs(fator_y)
        quantidade_ciclos += 1
        j += 1
    matriz_gerada.append(linha)
    recuo_lat -= abs(fator_x)
    i += 1

print "Gerando matriz"

i = 0
quantidade_ciclos = 0
print alturas
flag = 0
# popular os valores da matriz que nao foram preenchidos no processo anterior
if(ratio_coordenadas > 1):
    while(i < tamanho_matriz_x):
        # variavel que percorre a matriz de alturas
        j_alturas = 1

        j = 0
        while(j < tamanho_matriz_y):
            print i,j
            if(quantidade_ciclos % ratio_coordenadas == 0):
                if (j_alturas < (len(alturas[i])) and len(alturas[i]) > 1):
                    media_alturas = (alturas[i][j_alturas] - alturas[i][j_alturas - 1]) / ratio_coordenadas

                    flag = 1
                    j_alturas += 1
            else:
                if (j == 0 and len(alturas[i]) >= 2):
                    media_alturas = (alturas[i][j_alturas] - alturas[i][j_alturas - 1]) / (ratio_coordenadas - 1)
                    matriz_gerada[i][j] = alturas[i][j_alturas - 1] - (media_alturas * (ratio_coordenadas - 1))
                    if (matriz_gerada[i][j] < 0):
                        matriz_gerada[i][j] = 0
                    flag = 0
                    quantidade_ciclos += 1
                    j += 1
                    continue
                if(flag == 1):
                    matriz_gerada[i][j] = alturas[i][j_alturas - 2] + media_alturas
                    if(matriz_gerada[i][j] < 0):
                        matriz_gerada[i][j] = 0
                    flag = 0
                else:
                    matriz_gerada[i][j] = matriz_gerada[i][j-1] + media_alturas
                    if (matriz_gerada[i][j] < 0):
                        matriz_gerada[i][j] = 0

            j += 1
            quantidade_ciclos += 1
        print "mudou de linha"
        i += 1



print "Gravando matriz"

matriz_convertida = np.array(matriz_gerada)
matrix = np.matrix(matriz_convertida)
with open(nome_arquivo,'a') as f:
    for line in matrix:
        np.savetxt(f, line, fmt='%.2f')

