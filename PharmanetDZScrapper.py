from datetime import datetime
import re
from tkinter.ttk import Style
from unittest import result
import pprint
import requests
import json
import re
from bs4 import BeautifulSoup
from lxml import etree

def is_yes_or_no(variable,index):
    try:
        data = variable[index]['style']
        result =  re.search("color: (.*);",data).group(1)
        if(result == "darkgreen"):
            return "Oui"
        else:
            return "Non"    
    except:
        return "Pas d'information"    

def pas_information(variable):
    if (variable.strip() == 'N/A' or variable.strip() == 'N/D'):
        return "Pas d'information"
    else:
        return variable  

def check_fill(variable):
    if variable is None:
        return "Pas d'information"
    else:
        return variable.text   

def check_fill_notice(variable):
    if variable is None:
        return "Pas d'information"
    else:
        return "https://pharmanet-dz.com/"+variable['href']  

def check_fill_image(variable):
    if variable is None:
        return "Pas d'information"
    else:
        return "https://pharmanet-dz.com/"+variable['src'] 

def wrtie_json(new_data,totale,filename="medicaments.json"):
    with open(filename,'r+',encoding= 'utf8') as file:
        file_data = json.load(file)
        file_data["nombre_medicaments"] = totale
        file_data["medicaments"].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent = 4,ensure_ascii=False)


# designation laboratoire c_therapeutique c_pharmacologique type prod_locale commercialisé notice
# notice (ex:1086) / sans notice (ex:6093)
cpt = 0
fichier = { "medicaments" : [] }
fichier["date_mise_a_jour"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
# Serializing json 
json_object = json.dumps(fichier, indent = 4)
with open("medicaments.json", "w") as outfile:
    outfile.write(json_object)

for i in range(10000 ,20000):
    medicament = {}
    try:
        page_medicament =  requests.get(f"https://pharmanet-dz.com/medic.aspx?id={i}",headers={'User-Agent': 'Mozilla/5.0'}) 
        soup = BeautifulSoup(page_medicament.content.decode('utf-8'),"html.parser")
        titre = soup.select_one("#Form1 > div.wrap > div.content.container > div:nth-child(3) > div:nth-child(1) > div > section > div.body > div:nth-child(1) > div.col-lg-12.col-md-12.col-sm-12.col-xs-12 > div.col-lg-6.col-md-6.-col-sm-6.col-xs-12 > h3")
        if(titre is None) : raise RuntimeError
        print(f"ID : {i} {titre.text}")
        medicament["_id"] = i
        medicament["designation"] = check_fill(titre)
        medicament["lien_info"] = f"https://pharmanet-dz.com/medic.aspx?id={i}"
        medicament["laboratoire"] = pas_information(check_fill(soup.select_one("#Form1 > div.wrap > div.content.container > div:nth-child(3) > div:nth-child(1) > div > section > div.body > div:nth-child(1) > div.col-lg-8.col-md-8.col-sm-8.col-xs-12 > div.col-lg-7.col-md-7.col-sm-8.col-xs-12 > a:nth-child(1)"))).strip()
        medicament["c_pharmacologique"] = pas_information(check_fill(soup.find("img",src="img/cpharmaco.png").next_element)).strip()
        medicament["c_therapeutique"] = pas_information(check_fill(soup.find("img",src="img/ctherapeutique.png").next_sibling)).strip()
        medicament["dci"] = pas_information(check_fill(soup.find("img",src="img/dci.png").next_sibling)).strip()
        medicament["nom_commercial"] = re.search('Commercial: (.*)\r',soup.select_one("#Form1 > div.wrap > div.content.container > div:nth-child(3) > div:nth-child(1) > div > section > div.body > div:nth-child(1) > div.col-lg-8.col-md-8.col-sm-8.col-xs-12 > div.col-lg-7.col-md-7.col-sm-8.col-xs-12").text).group(1)
        medicament["code_dci"] = re.search('DCI: (.*)\r',soup.select_one("#Form1 > div.wrap > div.content.container > div:nth-child(3) > div:nth-child(1) > div > section > div.body > div:nth-child(1) > div.col-lg-8.col-md-8.col-sm-8.col-xs-12 > div.col-lg-7.col-md-7.col-sm-8.col-xs-12").text).group(1)
        medicament["forme"] = re.search('Forme: (.*)\r',soup.select_one("#Form1 > div.wrap > div.content.container > div:nth-child(3) > div:nth-child(1) > div > section > div.body > div:nth-child(1) > div.col-lg-8.col-md-8.col-sm-8.col-xs-12 > div.col-lg-7.col-md-7.col-sm-8.col-xs-12").text).group(1)
        medicament["dosage"] = re.search('Dosage: (.*)\r',soup.select_one("#Form1 > div.wrap > div.content.container > div:nth-child(3) > div:nth-child(1) > div > section > div.body > div:nth-child(1) > div.col-lg-8.col-md-8.col-sm-8.col-xs-12 > div.col-lg-7.col-md-7.col-sm-8.col-xs-12").text).group(1)
        medicament["conditionnement"] = re.search('Conditionnement: (.*)\r',soup.select_one("#Form1 > div.wrap > div.content.container > div:nth-child(3) > div:nth-child(1) > div > section > div.body > div:nth-child(1) > div.col-lg-8.col-md-8.col-sm-8.col-xs-12 > div.col-lg-7.col-md-7.col-sm-8.col-xs-12").text).group(1)
        medicament["type"] = re.search('Type: (.*)\r',soup.select_one("#Form1 > div.wrap > div.content.container > div:nth-child(3) > div:nth-child(1) > div > section > div.body > div:nth-child(1) > div.col-lg-8.col-md-8.col-sm-8.col-xs-12 > div.col-lg-5.col-md-5.col-sm-4.col-xs-12").text).group(1)
        medicament["liste"] = re.search('Liste: (.*)\r',soup.select_one("#Form1 > div.wrap > div.content.container > div:nth-child(3) > div:nth-child(1) > div > section > div.body > div:nth-child(1) > div.col-lg-8.col-md-8.col-sm-8.col-xs-12 > div.col-lg-5.col-md-5.col-sm-4.col-xs-12").text).group(1)
        medicament["commercialisation"] = is_yes_or_no(soup.find_all("i",class_="fa fa-check-circle-o"),0)
        medicament["remboursable"] = is_yes_or_no(soup.find_all("i",class_="fa fa-check-circle-o"),1)
        medicament["tarif"] = pas_information(re.search('rence: (.*)\r',soup.select_one("#Form1 > div.wrap > div.content.container > div:nth-child(3) > div:nth-child(1) > div > section > div.body > div:nth-child(1) > div.col-lg-8.col-md-8.col-sm-8.col-xs-12 > div.col-lg-5.col-md-5.col-sm-4.col-xs-12").text).group(1))
        medicament["ppa"] = pas_information(re.search(' : (.*)\r',soup.select_one("#Form1 > div.wrap > div.content.container > div:nth-child(3) > div:nth-child(1) > div > section > div.body > div:nth-child(1) > div.col-lg-8.col-md-8.col-sm-8.col-xs-12 > div.col-lg-5.col-md-5.col-sm-4.col-xs-12").text).group(1))
        medicament["num_enregistrement"] = pas_information(re.search('Enregistrement: (.*)\r',soup.select_one("#Form1 > div.wrap > div.content.container > div:nth-child(3) > div:nth-child(1) > div > section > div.body > div:nth-child(1) > div.col-lg-8.col-md-8.col-sm-8.col-xs-12 > div.col-lg-5.col-md-5.col-sm-4.col-xs-12").text).group(1))
        medicament["notice"] = check_fill_notice(soup.select_one("#Form1 > div.wrap > div.content.container > div:nth-child(3) > div:nth-child(1) > div > section > div.body > div:nth-child(1) > div.col-lg-4.col-md-4.col-sm-4.col-xs-12 > a"))
        medicament["image"] = check_fill_image(soup.select_one("#Form1 > div.wrap > div.content.container > div:nth-child(3) > div:nth-child(1) > div > section > div.body > div:nth-child(1) > div.col-lg-4.col-md-4.col-sm-4.col-xs-12 > img"))
        cpt = cpt + 1
        wrtie_json(medicament,cpt)
    except: 
        print(f"Pas de Medicament dont ID = {i}")   

