
Affichages
**********


Un affichage fait parti d'une fonctionnalité, qui possède un identifiant et une valeur.

Dans le code, un affichage est un widget dans une sous-fenêtre de la zone principale. Ce widget hérite de la classe *Display* qui implémente les fonctions de base nécessaires.

*Display* hérite de la classe *Fonctionality* qui implémente les signaux nécessaires pour l'application. Ces signaux permettent d'envoyer les valeurs modifiées au robot.

Les méthodes des classes mères doivent être utilisées dès que possible afin de garantir le bon fonctionnement du superviseur. En particulier pour les données suivantes :

* Valeur (value), envoyée vers le robot lorsqu'elle varie
* Variation (range), limites de variation de la valeur
* Identifiant (id), identifiant de la fonctionnalité

Mais également:
* Le wigdet de plus haut niveau (*setWidget()*)