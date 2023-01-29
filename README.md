### Projet 704 Thibaut ALLART / Paul BILLARD

## Routes Application
# GET
- Index ('/', '/index', '/index/') : Accès à la page d'accueil
- Library : Lecture des vidéothèques existantes
	- Vue sur toutes les vidéothèques ('/library', '/library/')
	- Vue des informations d'une vidéothèque ('/library/<name>', /library/<name>/)
- Film : Lecture des informatiions des films existants dans au moins une vidéothèque
	- Vue sur tous les films ('/film/<name>')
	- Vue des informations d'un film ('/film/<name>/')
- Acteur : Lecture des informations des acteurs présents dans au moins un film d'une vidéothèque
	- NOM IMPLEMENTE (Renvoie toujours 'No Actor Found')

# POST
- Film : Ajout d'un film dans une vidéothèque
	- Champs :
		- Nom propriétaire/Prénom propriétaire
		- Nom du film/Date de réalisation
		- Nom réalisateur/Prénom réalisateur
		- Acteurs (3 au maximum) : Nom acteur/Prénom acteur
	- Si le nom du propriétaire n'existe pas : Création d'une vidéothèque

# PUT
- A VOIR

# DELETE
- Film ('/deleteFilm/<name>', '/deleteFilm/<name>/'): Supprime un film d'une vidéothèque
- Library ('/deleteLibrary/<name>', '/deleteLibrary/<name>/'): Supprime une vidéothèque complète