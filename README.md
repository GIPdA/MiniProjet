MiniProjet
==========

Mini Projet scolaire - Contrôle et Supervision d'un Robot

---
####Outils:
Python 3, Pyside et Qt 4.8

---

##Description
Ce logiciel conçu avec Python permet la supervision et le contrôle d'un robot fonctionnant sous Linux.

Il permet de gérer des *fonctionnalités* de façon très flexible : voyants, capteurs TOR, capteurs analogiques, moteurs, servomoteurs, afficheurs, etc.

Différents modèles de robots sont supportés par l'utilisation de fichiers de configuration que l'on peut charger au démarrage de l'application.

La communication est basé sur un principe de *messages*, sans accusé de réception.
Les messages sont au format [JSON][1], format simple à utiliser et nativement disponible avec Python.

[1]: http://www.json.org "JSON"

