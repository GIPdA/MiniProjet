Wulka Bot
==========
Simulateur de robot

---
####Fichiers:
robot, Robot.py

---

##Description

Pour les tests de l'interface, un simulateur de robot a été réalisé. C'est un robot interactif simple, rond, avec trois roues et plusieurs capteurs.

Il se connecte à un port série et permet de 'streamer' sa configuration directement au superviseur, sans utiliser de fichier intermédiaire.

<br>
##Utilisation

Lancez simplement le script 'robot' ou bien Robot.py.

Le simulateur démarre et tente de se connecter au dernier port série utilisé lors du précédent lancement, s'il est disponible. S'il échoue, vous pouvez choisir un port à utiliser dans le menu *Ports*.

Dès le port ouvert, la configuration du robot est envoyée. Si le superviseur est ouvert et connecté à ce moment là, la configuration s'affiche automatiquement.

>Note: L'action *Stream configuration* du menu *Configuration* permet d'envoyer la configuration du robot au superviseur.

Le simulateur possède 2 types de capteurs : à contact (éléments gris en bordure de robot, cliquables) et à distance (zones à l'avant des capteurs à contact, interactifs avec la souris).

Il y a également 3 actionneurs : les deux grandes roues peuvent tourner dans les deux sens indépendamment et la petite roue arrière est directionnelle à 360°.