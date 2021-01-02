# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 21:35:06 2020

@author: Yen Nguyen
"""
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import requests
import time 
import json


def getData():
   url = "https://www.eversports.de/widget/w/tb4wwe"
   
   driver = webdriver.Chrome(executable_path=r'C:/Users/Yen Nguyen/Downloads/chromedriver_win32/chromedriver.exe')

   options = Options()
   options.headless = True
   options.add_argument("--window-size=1920,1200")

   driver.get(url)
   sidebar = driver.find_element_by_class_name('nav-tabs')
   elementNavBar = sidebar.find_elements_by_tag_name("li")
   slot_list = {}
       # Choisir une date sur le navigateur
   date_picker = driver.find_element_by_id("datepicker");
   print("Choisir une date sur le navigateur..")
   time.sleep(20)
   date_picker.click()
   
   for i in range(len(elementNavBar)):
       element = driver.find_element_by_class_name('nav-tabs').find_elements_by_tag_name("li")[i]
       element.click()  
       name_element = element.text
              
       html = ""
       data = []
        #Pour assurer que la page est téléchargé
       time.sleep(10)
       try:
           #Récupérer html
           html = driver.page_source
           
           #Utiliser la librairie BeautifulSoup pour récupérer les données
           soup = BeautifulSoup(html,"html.parser")
           date_table = soup.find("table", attrs={"class": "date-table"})
           center_id = soup.find("body", attrs={"id": "widget"}).attrs["data-facility-short-id"]
          
            #Le premier tbody contient les données pour la date choisie
           tbody = date_table.find("tbody")
           
           rows = tbody.find_all("tr")[2:]  #Les lignes à partir de troisième ligne: l'informations de tous les terrains
           
           #Lire chaque ligne(Une ligne contient le nom de terrain et l'information de tous les créneaux horaires pour un terrain)
           for row in rows:
               cols = row.find_all("td")[1:] #Les colonnes à partir de deuxième colonne: créneaux horaires pour un terrain
               #Lire chaque colonne(Une colonne contient l'information d'un créneau horaire pour un terrain)
               for col in cols:
                   item =  {}
                   try:
                       if (col.attrs['data-state'] != "free"):
                           continue
                       dateTime = col.attrs['data-date']
                       startTime = col.attrs['data-start']
                       endTime = col.attrs['data-end']
                       #un slot
                       item['centerId'] = center_id
                       item['facilityId'] = col.attrs['data-court']
                       item['startTime'] = dateTime + "T" + startTime 
                       item['endTime'] = dateTime + "T" + endTime
                       item['isAvailable'] = True
                       data.append(item)                  
                       
                   except:
                       pass
           #Ajouter des slots de chaque sport au slot_list          
           slot_list[name_element] = data
       
       except:    
           driver.quit()
   #Ecrire liste de slots groupée par nom de sport dans un fichier
   with open("slot_list.json", "w") as writeJSON:
       json.dump(slot_list, writeJSON, ensure_ascii=False)
   #Afficher liste de slots groupée par nom de sport
   print(slot_list) 
   #Fermer le navigateur       
   driver.quit()