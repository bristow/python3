#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  GeoCodage_Photon.py
#  
#  Copyright 2017 Bristow
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

## Ce programme permet, à partir d'un fichier CSV du type :
## nom_etablissement,commune,Nom,Prenom,Courriel
## un nouveau fichier CSV avec GEOCODAGE de la forme
## nom_etablissement,commune,Lon,Lat,Nom,Prenom,Courriel
## Le GeoCodage se fait via une requête sur le nom établissement et sa commune.
## Nom,Prenom,Courriel peut être n'importe quoi d'autre

import json
import urllib.request as ur
from pprint import pprint
import csv
from requests.utils import quote
import sys
import os
import glob

#Ouverture du fichier CSV, en lecture seule

chemin_fic = sys.path[0] #recup chemin du fichier Python

print("Voici les fichiers contenus dans le dossier :", chemin_fic)

print("*****************************************")

#liste les fichiers .csv
Liste_Fich = glob.glob("*.csv")

for i in range(len(Liste_Fich)):
	print("\t") #pour élaguer
	print(Liste_Fich[i])

print("*****************************************")
FicCSV = input("Quel est le nom du fichier csv avec l'extension ? ")

MonFichierCSV = open(
    file     = FicCSV,
    mode     = "r",
    encoding = "utf-8")

MonFichierCSVGeocode = open(FicCSV[:-4]+"_GeoCode.csv", "w")

reader = csv.reader(MonFichierCSV)
#next(reader) #permet d'exclure la première ligne


try:
    for ligne in reader:
        if reader.line_num == 1:
            #Ajout première ligne du CSV dans le fichier de sortie (identique au fichier de départ)
            #permet d'ajouter 'Lon' et 'Lat' pour insérer cela dans uMap
            print('Ecriture de la première ligne')
            MonFichierCSVGeocode.write('{},{},{},{},{},{},{}\n'.format(ligne[0],ligne[1],'Lon','Lat',ligne[2],ligne[3],ligne[4]))
        else:
            print('Récupération {} à {}'.format(ligne[0],ligne[1]))
            url_requete = 'http://photon.komoot.de/api/?q='+ligne[0]+' '+ligne[1]+'&lang=fr'
        
            #print(url_requete)
        
            # Normalisation de l'url
            url_requete = quote(
                string = url_requete,
                safe   = "/:#&?=")
        
            s1 = ur.urlopen(url_requete)
            #print(s1)
            mon_json = s1.read()
            data = json.loads(str(mon_json.decode("utf-8")))
            print("Coordonnées GPS : Long. = {}, Lat. = {}".format(data['features'][0]['geometry']['coordinates'][0],data['features'][0]['geometry']['coordinates'][1]))
            MonFichierCSVGeocode.write('{},{},{},{},{},{},{}\n'.format(ligne[0],ligne[1],data['features'][0]['geometry']['coordinates'][0],data['features'][0]['geometry']['coordinates'][1],ligne[2],ligne[3],ligne[4]))
except IndexError:
    print("Pas de résultat sur la requête précédente !")


##----- Fermeture du fichier précédendemment ouvert -----##
MonFichierCSV.close()
MonFichierCSVGeocode.close()
