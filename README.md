MiniProjet
==========

Mini Projet scolaire - Contrôle et Supervision d'un Robot

---
####Outils:
Python 3.3, PySide et Qt 4.8

---

##Description
Ce logiciel permet la supervision et le contrôle d'un robot.

Il permet de gérer des *fonctionnalités* de façon très flexible : voyants, capteurs TOR, capteurs analogiques, moteurs, servomoteurs, afficheurs, etc.

Différents modèles de robots sont supportés par l'utilisation de fichiers de configuration que l'on peut charger au démarrage de l'application.
Le robot peut également envoyer lui-même sa configuration au superviseur, permettant ainsi de se passer de fichier de configuration.

</br>
###Fonctionnalité ?

D'une fonctionnalité résulte un type d'affichage. Un capteur TOR s'affichera sous la forme d'un bouton radio, un capteur analogique peut être affiché avec une barre de progression.

Mais une fonctionnalité n'est pas qu'un affichage, cela peut également être une commande: un curseur, un potar, etc, ou des assemblages plus complexes.

Une fonctionnalité est totalement 'customisable' via les données de configuration, et vous pouvez en créer de nouvelles selon vos besoins.


###Communication

La communication est basé sur un principe de *messages*, sans accusés de réception.
Les messages sont au format [JSON][1], format simple à utiliser et nativement disponible avec Python (et également disponible avec nombre d'autres languages).

[1]: http://www.json.org "JSON"

Actuellement seule la communication sur port série est gérée.

</br>

##Fonctionnement

###Identifiants
Une fonctionnalité est définie par un identifiant unique, un type d'affichage et des options optionnelles (hum…).
Chaque 'valeur' est en fait un couple clé-valeur (type dictionnaire), les types possibles sont ceux défini par le protocole JSON.


###Valeurs
Voici la liste, l'arborescence est essentielle et doit être respectée :

*- clé : x(type de la valeur) description -*

*x: o pour obligatoire, si rien: paramètre optionnel*

* identifiant : o(string) identifiant de la fonctionnalité
* 'display' : o(string) Type d'affichage (voir liste)
* 'name' : (string) Nom de la fonctionnalité (affiché à la place de l'identifiant)
* 'group' : (int) Numéro de groupe, permet de grouper des fonctionnalités (affichées alors dans une même fenêtre)
* 'layout': (string) Pour arranger la fonctionnalité dans un layout (lorsque les fonctionnalités sont groupées)
* 'disable' : (bool) permet de modifier l'affichage (activé/désactivé)
* 'data' : dictionnaire de réglage. Valeurs : (peut être spécifique à un type d'affichage)
  * 'range' : (list) variation (défaut: 0-100)
  * 'vertical' : (bool) Permet de changer l'orientation

Des exemples sont disponibles avec les fichiers .bvc, ou avec le simulateur de robot (Robot.py).


####Layout
Lorsque des fonctionnalités sont groupées, elles peuvent être arrangées dans une grille. La syntaxe est la suivante:

> rncnrsncsn

**r** pour le numéro de la rangée (row),
**c** pour le numéro de la colonne (col),
**rs** pour le nombre de rangées à couvrir (row span),
**cs** pour le nombre de colonnes à couvrir (col span).
**n** étant le nombre associé à chaque clé.

Des valeurs peuvent être omises, et suivant le cas un placement automatique est alors réalisé (en spécifiant r0, les fonctionnalités sont arrangées sur une seule rangée, avec c0 sur une seule colonne).


###Communication

Pour mettre à jour les valeurs associées aux identifiant, c'est tout simple : il suffit d'envoyer l'identifiant associé à sa nouvelle valeur sous forme d'un dictionnaire.

Par exemple:
> { 'led1':True, 'progressbar':53 }

Pour 'allumer' la led 1 et régler une barre de progression à la valeur 53.

Pour des fonctionnalités plus complexes, la valeur associée à un identifiant peut être un autre dictionnaire par exemple, pas uniquement un type de 'base'.

---

##TODO list

* Ajouter protocole internet (udp ?)
* Créer une classe 'abstraite' pour la communication
* Lister les ports 'en continu' (thread)
* Pouvoir modifier un affichage depuis l'interface superviseur
* Fonctionnalités :
 - Ajouter réglage de taille/position des groupes
 - Pouvoir modifier une fonctionnalité sans recharger toute la configuration

