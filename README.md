## 2. Points d'amélioration possibles
- Changer le casque audio pour de vrais micro et haut-parleur.
- Faire en sorte que wikipedia ne renvoie pas de phonétique dans le résumé de la page, car piper ne parvient pas à le lire avec son modèle de voix.
- Ajouter un régulateur de tension pour éviter d'avoir 2 alimentations à brancher.
- Redimmensionner les pièces 3D, car certaines pièces ne laissent pas assez de marge, ce qui nous a contraint à limer une partie des pièces.


# WIKIBOT - projet PRONTO (projet de l'ingénieur dans un monde en transition)
Wikibot est un robot interactif capable de répondre aux questions vocales en utilisant Wikipedia, avec expressions faciales et mouvements corporels.

## 1. Description
Ce robot compagnon est conçu pour interagir naturellement avec les utilisateurs à travers :

**Reconnaissance vocale** : Écoute et comprend les requêtes (un seul mot ou groupe de mots) en français quand l'utilisateur maintient le bouton poussoir 
**Recherche sur wikipedia** : Utilise Wikipedia pour fournir un résumé en une phrase de la page correspondante à la requête de l'utilisateur.
**Synthèse vocale** : Répond avec une voix de synthèse
**Expressions faciales** : Affiche différentes expressions sur écran selon le contexte (speaking, teaching, waiting, thinking)
**Mouvements** : Gesticule avec les bras et la tête pendant les interactions

## 2. Fonctionnalités

### Interface Multimodale
**Audio** : Enregistrement lorsque le bouton poussoir est maintenu avec sounddevice, reconnaissance vocale avec Vosk, recherche sur le web avec wikipedia, synthèse vocale avec Piper pour générer la réponse.
**Visuel** : Écran avec expressions faciales animées (parlant, enseignant, attente, réflexion)
**Gestuelle** : Servomoteurs pour les 2 bras et la tête avec mouvements synchronisés.

### Modes d'Expression du visage
Mode **waiting** : Visage souriant, sans mouvement
Mode **thinking** : Sourire avec engrenages, sans mouvement
Mode **teaching** : Lunettes et animation bouche pour les réponses
Mode **speaking** : Animation bouche pendant les réponses et la phrase d'accueil.

### Etapes de l'interaction

|Etape     |Audio                                                                                          |Servomoteurs          | Expression visage |
|-----------|------------------------------------------------------------------------------------------------|-----------------------|---|
|Démarrage|Salutation et présentation                                                                     |Rotation des deux bras |speaking|
|Requête   |L'utilisateur maintient le bouton<br> poussoir et expose sa requête                             |/                     |waiting|
|Traitement|Enregistrement requête -> stt -> Recherche résumé wikipedia -> stt                              |/                     |thinking|
|Réponse*  |1. Sortie audio du résumé wikipedia<br> 2. Lecture du fichier audio disant qu'il n'a pas compris|2. Rotation de la tête|1. teaching<br> 2. speaking|

\* Dans le **cas 1.** la recherche wikipedia renvoie un résultat. <br>
Tandis que dans le **cas 2.** la recherche ne renvoie rien (cela peut être dû au fait qu'aucune requête n'a été donnée par l'utilisateur, que la connection wifi a sauté ou que la recherche n'a pas aboutie car le mot a mal été transcrit, qu'il existe plusieurs page associées ...)

## 6. Auteurs
Ce projet a été développé par 4 étudiants de l'IMT Atlantique dans le cadre du projet Pronto:

Astrid MARION
Louis BONDUELLE
Coline FELTIN
Florian THOLLOT
