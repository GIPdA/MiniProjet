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


###Fonctionnalité ?

D'une fonctionnalité résulte un type d'affichage. Un capteur TOR s'affichera sous la forme d'un bouton radio, un capteur analogique peut être affiché avec une barre de progression.

Mais une fonctionnalité n'est pas qu'un affichage, cela peut également être une commande: un curseur, un potar, etc, ou des assemblages plus complexes.

Une fonctionnalité est totalement 'customisable' via les données de configuration, et vous pouvez en créer de nouvelles selon vos besoins.


###Communication

La communication est basé sur un principe de *messages*, sans accusés de réception.
Les messages sont au format [JSON][1], format simple à utiliser et nativement disponible avec Python (et également disponible avec nombre d'autres languages).

[1]: http://www.json.org "JSON"

Actuellement seule la communication sur port série est gérée.

---

##TODO list

* Ajouter protocole internet (udp ?)
* Créer une classe 'abstraite' pour la communication
* Lister les ports 'en continu' (thread)
* Fonctionnalités :
 - Ajouter réglage de taille
 - Ajouter la sauvegarde de position des groupes