# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 18:08:03 2021

@author: Ignacio Calcedo Vázquez
"""

import pandas as pandas
import math as math
import random as random
import numpy as np
import os
import copy

'''DEFINICIONES Y UTILIDADES'''


cabecera="C:\\Users\\icalc\\Documents\\TFG\\fceuxs\\fm2"
rutas=os.listdir(cabecera)

prob_cross=0.7
prob_mut=0.1

def old_or_rd(numero):
  r=random.random()
  if r<=prob_mut:
    return random.randint(0,255)
  else:
    return numero

def decimalToBinary(n): 
    s = bin(n)
    return s[:2] + s[2:].zfill(8)

def addNopes(individuo, max_l):
  return (individuo+[0 for i in range (max_l-len(individuo))])

def separaCabecera(lineas):
  indice=0
  while indice < len(lineas):
    if lineas[indice][0]=="|":
      break
    else:
      indice+=1
  return lineas[:indice], lineas[indice:]

def generaindividuo(cuerpo,mapaestados):
  individuo=[mapaestados.get(frame[3:11]) for frame in cuerpo]
  return individuo

#generación de los posibles estados: RLDUTSBA
def generaestados():
  buttons=["R","L","D","U","T","S","B","A"]
  estados_bin=[decimalToBinary(i) for i in range (0,256)]
  estados =list()
  for e in estados_bin:
    estado=""
    for i in range (8):
      if e[i+2]=="1":
        estado+=buttons[i]
      else:
        estado+="."
    estados.append(estado)

  mapa_estados=dict(zip(estados,[i for i in range (256)]))
  return estados, mapa_estados

def gen_ind_fich(ruta):
  with open(ruta,"r") as f1:
    lineas=f1.readlines()
    cabecera, cuerpo = separaCabecera(lineas)
    
    indiv = generaindividuo(cuerpo,mapaestados)
    return indiv

def genera_randoms(cantidad, longitud):
  inds_al= []
  for _ in range(cantidad):
    ind=[random.randint(0,255) for _ in range(longitud)]
    inds_al.append(ind)
  return inds_al

def genera_heuristic(individuo,cantidad):
  inds_heu=[]
  for _ in range(cantidad):
    ih=[old_or_rd(gen) for gen in individuo]
    inds_heu.append(ih)
  return inds_heu

def f_fitness(individuo):
  pass

def crucegenetico(a1,a2):
  #utilizaremos un cruce uniforme. cada gen se intercambiará con otro en función de una probabilidad
  d1=[]
  d2=[]
  for i in range(len(a1)):
    flipcoin=random.random()
    if flipcoin<0.5:
      d1.append(a1[i])
      d2.append(a2[i])
    else:
      d1.append(a2[i])
      d2.append(a1[i])
  return d1,d2

def mutacion(a1):
  comienzo_m=random.randint(0,64343-60)
  fin_m=comienzo_m+60
  a1[comienzo_m:fin_m]=random.shuffle(a1[comienzo_m:fin_m])
  return a1

def separa_idles(cromosoma):
  blanks=[]
  treat_0=True
  i=0
  s=0
  f=0
  margen=0
  while i<len(cromosoma):
    if treat_0: #si estamos en una sección de 0s --> idle state
      if cromosoma[i]!=0: #termina el idle state
        f=i
        blanks.append((s,f))
        treat_0=False
      
    else: #si estamos tratando con una zona activa
      if cromosoma[i]==0:
        if margen>=5:
          s=i
          treat_0=True
          margen=0
        else:
          margen+=1
    i+=1

  return blanks

def genera_guid():
  s1=[str(hex(random.randint(0,16)))[2:].upper() for i in range (8)]
  s2=[str(hex(random.randint(0,16)))[2:].upper() for i in range (4)]
  s3=[str(hex(random.randint(0,16)))[2:].upper() for i in range (4)]
  s4=[str(hex(random.randint(0,16)))[2:].upper() for i in range (4)]
  s5=[str(hex(random.randint(0,16)))[2:].upper() for i in range (6)]
  
  guid="guid {}-{}-{}-{}-{}".format("".join(s1),"".join(s2),"".join(s3),"".join(s4),"".join(s5))
  return guid

'''COMIENZO DEL ALGORITMO'''
estados, mapaestados= generaestados()
individuos_iniciales=[gen_ind_fich(cabecera+"\\"+ruta) for ruta in rutas]


#preparacion de los individuos para igualar la longitud de cromosomas

max_length= len(max(individuos_iniciales,key=lambda x: len(x)))
ind_iniciales_preparados= [addNopes(i,max_length) for i in individuos_iniciales]

#A partir de los individuos que sabemos que son válidos y sin errores, es necesario
#buscar las zonas en las que no se realiza ninguna actividad, pues estas no son relevantes
#para el testing



ruta_tempmovies= os.path.join(os.getcwd(),"temp_movies")

if not (os.path.exists(ruta_tempmovies) and os.path.isdir(ruta_tempmovies)):
  os.mkdir("temp_movies")

cabecera=""
cabecera+="version 3\n"
cabecera+="emuVersion 9816\n"
cabecera+="fourscore 0\n"
cabecera+="romFilename Mike Tyson's Punch-Out!! (Japan, USA) (Rev A).nes\n"
cabecera+="romChecksum base64:W8f6wG5Y/aFf2YH9A1csNA==\n"

cabecera+="microphone 0\nport0 1\nport1 0\nport2 0\n"

ind_iniciales_preparados+=genera_randoms(10,max_length)
ind_iniciales_preparados+=genera_heuristic(ind_iniciales_preparados[0],10)



numero_generacion=0
while numero_generacion<10:
    #generacion de archivos para 
    for i in range(len(ind_iniciales_preparados)):
      filename='movie'+str(i)+'.fm2'
      filename=os.path.join('temp_movies',filename)
      with open(filename,'w') as archivo:
        copy_cabecera=copy.copy(cabecera)
        copy_cabecera+=genera_guid()+'\n'
        movietext=copy_cabecera
        movietext+="|2|"+estados[ind_iniciales_preparados[i][0]]+"|||\n"
        inputs="".join(["|0|"+estados[g]+"|||\n"
          for g in ind_iniciales_preparados[i][1:]])
        movietext+=inputs
        archivo.write(movietext)
    print("Archivos generados")
    #Funciones objetivo
    for i in range(len(ind_iniciales_preparados)):
      filename='movie'+str(i)+'.fm2'
      filename=os.path.join('temp_movies',filename)
      
    numero_generacion=10


        
