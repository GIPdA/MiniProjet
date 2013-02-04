.. role:: underlined
.. role:: through

Mini Projet - Superviseur de robot
**********************************

Ce logiciel permet la supervision et le contrôle d'un robot.

Il permet de gérer des *fonctionnalités* de façon très flexible : voyants, capteurs TOR, capteurs analogiques, moteurs, servomoteurs, afficheurs, etc.

Différents modèles de robots sont supportés par l'utilisation de fichiers de configuration que l'on peut charger au démarrage de l'application. Le robot peut également envoyer lui-même sa configuration au superviseur, permettant ainsi de se passer de fichier de configuration.


Fonctionnalité ?
================

Une fonctionnalité est en fait un type d'affichage. Un capteur TOR peut être un bouton radio, un capteur analogique peut être affiché avec une barre de progression.

Mais ce n'est pas qu'un affichage, cela peut également être une commande: un curseur, un potar, etc, ou des assemblages plus complexes.

Elles sont également totalement 'customisable' via les données de configuration, et vous pouvez en créer de nouvelles selon vos besoins.

Voir section ?? pour plus de détails.


Communication
=============

La communication est basé sur un principe de messages, sans accusés de réception. Les messages sont au format JSON, format simple à utiliser et nativement disponible avec Python (et également disponible avec nombre d'autres languages).

Actuellement seule la communication sur port série est gérée.

Section ??


Utilisation
===========

L'utilisation du superviseur est très simple et ne nécessite que quelques clics. Voici les étapes :

1. Lancer le superviseur via le script *botvisor* ou directement BotVisor.py avec Python (attention nécessite Python 3.3 !),
2. Sélectionner un port via le menu *Ports* si nécessaire (le dernier port ouvert au dernier lancement est automatiquement ré-ouvert si possible),
3. Charger un fichier de configuration (*File* > *Open Robot...*) ou bien attendre que le robot envoi sa configuration.
4. :through:`Faire joujou !` Superviser...


