
Communication
*************

*Actuellement seule la communication sur port série est gérée.*


Principe
========

La communication du superviseur fonctionne sur un principe de **messages**, sans accusés de réception.
Un message est au format JSON, sous la forme d'un dictionnaire (élément = clé + valeur), comme par exemple : ::

	{
		'led':True,
		'leftMotor':90,
		'complexData':{'button':True, 'text':Hello World!}
	}

Le nombre d'éléments minimum est de 1, il n'y a pas de maximum. Il n'est pas obligatoire d'envoyer tous les éléments correspondant aux fonctionnalités, uniquement ceux à mettre à jour.

Protocole
=========

Le dictionnaire JSON est converti en chaine de caractères afin d'être envoyé, et entouré de < > afin d'être correctement traité à la réception: ::

	<{'led':True,'leftMotor':90,'complexData':{'button':True, 'text':Hello World!}}>

La conversion en chaine du dictionnaire JSON est réalisé par le module JSON de python (*json.stringify()*), et la reconnaissance du dico JSON à la réception est faite à l'aide d'une expression régulière : ::

	(serialCom.py, SerialCom::_readSerial)

	match = re.search('^.*?(<({.*?})>)', self._dataRead)

Puis converti à nouveau en dico python à l'aide de la fonction *loads* de json.