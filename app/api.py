#!/usr/bin/python3
from flask import Flask, render_template, request
from datetime import date
import requests
import json

api = Flask(__name__)

@api.route("/library", methods=["GET"])
@api.route("/library/", methods=["GET"])
@api.route("/library/<name>", methods=["GET"])
@api.route("/library/<name>/", methods=["GET"])
def getLibrary(name = None):
    with open("./video.json", encoding = 'utf-8') as file:
        d = json.load(file)

    res = []
    data = d['videotheque']

    # Si on indique un nom de propriétaire dans la recherche, on récupère la liste des films qu'il possède
    if name is not None:
        for jsonData in data:
            line = json.loads(json.dumps(jsonData))
            if line["proprietaire"]["nom"].lower() == name.lower():    
                if "films" in line:
                    for film in line["films"]:
                        res.append([film["titre"], film["année"], film["réalisateur"]["nom"], film["réalisateur"]["prénom"]])
        return json.dumps(res)
    
    # Si aucun nom mentionné, on affiche tous les noms de propriétaires
    for jsonData in data:
        line = json.loads(json.dumps(jsonData))
        # if "proprietaire" in line:
        res.append([line["proprietaire"]["nom"], line["proprietaire"]["prénom"]])

    return json.dumps(res)

@api.route("/film", methods=["GET"])
@api.route('/film/<name>', methods=['GET'])
def getFilm(name = None):
    with open("./video.json", encoding = 'utf-8') as file:
        d = json.load(file)
    #On récupère les films de toutes les vidéothèques
    resultat = []
    données = d['videotheque']

    #Cas où aucun nom n'est renseigné --> Afficher tous les films.
    if name is None:

        for proprioJson in données:
            #proprioJson --> un dict que l'on doit passer en string afin que json.loads puisse lire le code.
            proprio = json.loads(json.dumps(proprioJson))
            if "films" in proprio:
                if resultat == [] : #Si données est vide alors on rajoute tous les films de la première vidéothèque, pas besoin de vérifier les doublons
                    for j in proprio['films']:
                        resultat.append(j)
                else :
                    for j in proprio['films']:
                        if j not in resultat:
                            resultat.append(j)
    
    #Cas où nom est renseigné --> Afficher les films du réalisateur.
    else:

        for proprioJson in données:
            proprio = json.loads(json.dumps(proprioJson))
            if "films" in proprio:
                for film in proprio['films']:
                    if film['réalisateur']['nom'].lower() == name.lower() :
                        # if permettant de n'ajouter qu'une seule fois la valeur du nom et du prénom dans la liste résultat.
                        if resultat == []:
                            resultat.append(film['réalisateur']['nom'])
                            resultat.append(film['réalisateur']['prénom'])
                        resultat.append(film)        

    return json.dumps(resultat)

#Ajout d'un nouveau film
@api.route("/addFilm/",methods=['POST'])
def createFilm():

    videothequeExiste = False # Montre si la vidéothèque est dans le fichier ou non.
    iteBoucle = 0 # Nombre d'itération de la première boucle while
    indiceProprio = -1 # -1 indique que le propriétaire n'existe pas
    data = request.get_json() #Malgrè le get_json, data est bien un dictionnaire.
    dataFilm=data['film'] #On facilite accès aux données du film
    reponse={}

    #On vérifie qu'un réalisateur et une année ont été rentré

    if (dataFilm["nomRéal"]=="" or dataFilm["pnomRéal"]==""):
        print("Tentative de création de film avec données du réalisateur incorrecte.")
        reponse["code"]=1

    elif (dataFilm["année"]==""):
        print("Tentative de création de film avec donnée de l'année de sortie du film incorrecte.")
        reponse["code"]=2

    else:
        reponse["code"]=0

    #On cherche si le propriétaire de la vidéothèque existe
    nomProp = data['proprietaire']['nom']
    pnomProp = data['proprietaire']['prénom']

    if (nomProp=="" or pnomProp==""):
        print("Tentative de création de film sans données du propriétaire de la vidéothèque.")
        reponse["code"]=3

    #On cherche la ligne dans laquelle on doit écrire
    with open("./video.json", encoding = 'utf-8') as file:
        d = json.load(file)
    donneeVideo = d['videotheque']

    #Boucle pour voir si le propriétaire existe. Si oui, on donne son numéro d'indice dans donneeVideo
    while(iteBoucle<len(donneeVideo) and videothequeExiste == False):
        propBoucle = donneeVideo[iteBoucle]['proprietaire']
        nomPropBoucle = propBoucle['nom']
        pnomPropBoucle = propBoucle['prénom']

        if ( nomProp.upper()==nomPropBoucle.upper() and pnomProp.upper()==pnomPropBoucle.upper()):
            indiceProprio=iteBoucle
            videothequeExiste = True

        iteBoucle = iteBoucle + 1

    #Mise en forme du contenu à ajouter
    listeActeurs=[]

    #On vérifie si les acteurs sont renseignés. Cela évite d'avoir une case acteur dans la carte quand il n'y a pas de 2ème/3ème acteur.
    if (dataFilm["nomAct1"]!="" and dataFilm["pnomAct1"]!=""):
        acteur={"nom":dataFilm["nomAct1"],
        "prénom":dataFilm["pnomAct1"]
        }
        listeActeurs.append(acteur)

    if (dataFilm["nomAct2"]!="" and dataFilm["pnomAct2"]!=""):
        acteur={"nom":dataFilm["nomAct2"],
        "prénom":dataFilm["pnomAct2"]
        }
        listeActeurs.append(acteur)

    if (dataFilm["nomAct3"]!="" and dataFilm["pnomAct3"]!=""):
        acteur={"nom":dataFilm["nomAct3"],
        "prénom":dataFilm["pnomAct3"]
        }
        listeActeurs.append(acteur)


    #Mise en forme du contenu.
    if (reponse["code"]==0):
        contenu = {
            "titre":dataFilm['titre'],
            "année":int(dataFilm['année']),
            "réalisateur":{
                "nom":dataFilm['nomRéal'],
                "prénom":dataFilm['pnomRéal']
            },
            "acteurs":listeActeurs
        }

        #Cas où la vidéothèque du propriétaire existe :
        if indiceProprio != -1:
            donnee=donneeVideo[indiceProprio]
            donnee["dernière_modif"]=data["dernière_modif"]
            if "films" in donnee:
                listeFilms=donnee['films']
                listeFilms.append(contenu)
                donnee["films"]=listeFilms
            else:
                donnee["films"]=[]
                donnee["films"].append(contenu)
            donneeVideo[indiceProprio]=donnee

        #Cas où la vidéothèque du propriétaire n'existe pas : on créée la vidéothèque
        else :
            nouvVideo={}
            nouvVideo["proprietaire"]={
                "nom":nomProp,
                "prénom":pnomProp
            }
            nouvVideo["dernière_modif"]=data["dernière_modif"]
            nouvVideo["films"]=[]
            nouvVideo["films"].append(contenu)
            donneeVideo.append(nouvVideo)

        #Mise en json du fichier afin d'avoir une bonne présentation dans le fichier video.json
        nouvContenu={"videotheque":donneeVideo}
        objJson=json.dumps(nouvContenu,indent=4, ensure_ascii=False).encode('utf8')
        #Ecriture dans le fichier entier :
        with open('./video.json', 'w', encoding = 'utf-8') as file:
            file.write(objJson.decode())

    return json.dumps(reponse)

if __name__ == "__main__":
    api.run(debug=True, host="0.0.0.0", port=5001)