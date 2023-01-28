#!/usr/bin/python3
import requests
import json
from flask import Flask, render_template, request
from datetime import date

app = Flask(__name__)
host="http://10.11.5.81:5001"

@app.route('/')
@app.route('/index')
@app.route('/index/')
def index():
    return render_template("index.html")

@app.route('/library')
@app.route('/library/')
def library():
    r = requests.get(host+"/library/")
    data = json.loads(r.text)   
    return render_template("library.html", data=data, name=None)

@app.route('/library/<name>', methods=['GET'])
@app.route('/library/<name>/', methods=['GET'])
def libraryName(name=None):
    r = requests.get(host+"/library/"+str(name))
    data = json.loads(r.text)
    return render_template("library.html", data=data, name=name)

#Va afficher tous les films présentes sur les vidéothèques.
@app.route('/film', methods=['GET'])
@app.route('/film/', methods=['GET'])
def film():
    r = requests.get(host+"/film")
    data = json.loads(r.text)
    return render_template("film.html",data=data, name=None)

@app.route('/film/<name>', methods=['GET'])
@app.route('/film/<name>/', methods=['GET'])
def filmReal(name=None):
    r = requests.get(host+"/film/"+str(name))
    data = json.loads(r.text)
    return render_template("film.html",data=data,name=name)

@app.route('/addFilm', methods=['POST'])
def addFilm():
    #On récupère les données obligatoires. (Données propriétaires vidéothèques, Réalisateur, nom Film, date)
    nomProp = request.form.get("nomProp")
    pnomProp = request.form.get("pnomProp")
    nomFilm = request.form.get("filmName")
    datePar = request.form.get("datePar") #Sous la forme de type str : 'aaaa-mm-dd'
    anneePar = (datePar.split('-'))[0] #On ne récupère que l'année puisqu'il n'y a que celle ci qui est nécessaire.
    nomReal = request.form.get("nomReal")
    pnomReal = request.form.get("pnomReal")
    nomAct1 = request.form.get("nomAct1")
    pnomAct1 = request.form.get("pnomAct1")
    nomAct2 = request.form.get("nomAct2")
    pnomAct2 = request.form.get("pnomAct2")
    nomAct3 = request.form.get("nomAct3")
    pnomAct3 = request.form.get("pnomAct3")
    ajd = str(date.today()) #Date de la dernière modif. Même format que date de parution.
    listAjd = ajd.split('-')
    dateAjd = listAjd[2]+'/'+listAjd[1]+'/'+listAjd[0]
    #On implémentera nos données du formulaire dans un dictionnaire.
    dataForm = {
        "proprietaire" : {
            "nom" : nomProp,
            "prénom" : pnomProp
        },
        "dernière_modif":dateAjd,
        "film":{
            "titre":nomFilm,
            "année":anneePar,
            "nomRéal": nomReal,
            "pnomRéal": pnomReal,
            "nomAct1": nomAct1,
            "pnomAct1": pnomAct1,
            "nomAct2": nomAct2,
            "pnomAct2": pnomAct2,
            "nomAct3": nomAct3,
            "pnomAct3": pnomAct3
        }
    }
    #On envoie nos données à l'API.
    resultat = requests.post(host+"/addFilm/",json=dataForm)
    #On récupère les données
    resultat = resultat.json()
    #On copie le code dans dataForm
    dataForm["code"]=resultat["code"]
    return render_template("addFilm.html",data=dataForm)

@app.route('/actor')
@app.route('/actor/<name>', methods=['GET'])
def actor(name=None):
    return render_template("actor.html", data=name)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)