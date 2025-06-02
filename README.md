# Robot Compagnon
Ce robot est un robot interactif capable de répondre aux questions vocales en utilisant Wikipedia, avec expressions faciales et mouvements corporels.

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

\* Dans le cas 1. la recherche wikipedia renvoie un résultat. Tandis que dans le cas 2. la recherche ne renvoie rien (cela peut être dû au fait qu'aucune requête n'a été donnée par l'utilisateur, ou que la recherche n'a pas aboutie car le mot a mal été transcrit, qu'il existe plusieurs page associées ...)

1. Démarrage : Le robot salut en levant les bras puis se présente et explique son fonctionnement 
2. Question : L'utilisateur maintient le bouton poussoir et expose sa requête
3. Traitement : Le robot réfléchit et recherche la réponse
4. Réponse : Le robot répond avec gestes et expressions appropriées
Flux d'Interaction
Présentation → Écoute → Traitement → Réponse → Écoute...

Changements de mode d'expression selon l'état du système
Arrêt automatique des threads à la fin de chaque tâche
Gestion des ressources partagées avec des verrous
Développement
Extension des Fonctionnalités
Nouvelles expressions : Ajoutez des modes dans Screen.py
Autres sources de données : Modifiez AudioProcessing.py
Nouveaux gestes : Étendez Servo.py avec de nouveaux mouvements
Langues supplémentaires : Changez les modèles Vosk et Piper
Debugging
Logs détaillés dans chaque classe
Gestion d'exceptions dans tous les threads
Mode verbose pour le développement
Configuration
Personnalisation Audio
Langue : Modifiez wikipedia.set_lang() dans AudioProcessing.py
Modèles : Changez les chemins dans les variables de configuration
Qualité audio : Ajustez SAMPLE_RATE et les paramètres d'enregistrement
Personnalisation Visuelle
Taille d'écran : Le système s'adapte automatiquement (fullscreen)
Couleurs et formes : Modifiez les constantes dans Screen.py
Animations : Ajustez les paramètres d'animation

## 3. Architecture Technique
### Composants électroniques 

- **Raspberry Pi 4 model b** avec GPIO pour l'interface matérielle
- **Casque USB** (/!\ la prise jack de la raspberry ne fournie pas d'entrée audio, donc il est nécessaire )
- **bouton poussoir**
- **résistance** (1 kΩ) 
- **Module de commande ADA815**
- **3 servomoteurs continues**
- **Ecran** LCD UCTRONICS B0106
- **Câbles**: alimentation raspberry avec boîtier (3A, 5.1V) / hub USB (2 ports) / câbles Dupont (x8) / HDMI-HDMI mini (pour l'écran) / USB-micro_USB (alim écran) / alim module servo / adaptateur USB-secteur 

### Configuration Matérielle

- **GPIO 4** : Bouton poussoir (pull-up interne)
- **GPIO 17** : Pin OE pour contrôle des servomoteurs
- **USB Port 1** : Microphone
- Servomoteurs sur le module:
    - **Canal 0** : Bras gauche
    - **Canal 1** : Tête
    - **Canal 2** : Bras droit

### Configuration Raspberry

- Installation de l'OS de la raspberry via Raspberry Pi Imager:
    - Système d'exploitation:  **Raspberry Pi OS (64-bit) (En ligne)**
    - Nom d’hôte: **rpi.local**
    - Nom utilisateur: **grp10**

- Activer l'I2C pour l'écran et le module de contrôle des servomoteurs: 
```bash
sudo raspi-config
> "Interfacing Options" 
> "I2C"
> Enable 
```
Pour vérifier les adresses I2C:
```bash
i2cdetect -y 1
```

- Choisir le bon port audio:
```bash
sudo raspi-config 
> systeme option 
> audio 
> choose USB
```

### Structure de l'environnement Raspberry
```bash
grp10/                                      # Dossier utilisateur
├── setup_autostart.sh                      # Fichier de démarrage automatique après allumage
├── ...    
└── p10/                                    # Environnement virtuel Python
    ├── bin/
    ├── lib/
    ├── ...
    └── projet-pronto/                      # Dossier mère du projet
        ├── Main.py                         # Point d'entrée et orchestration principale
        ├── audio/
        │   ├── AudioProcessing.py          # Acquisition, reconnaissance et synthèse vocale
        │   ├── Speak.py                    # Lecture de fichiers audio
        │   └── preRecordedDialogs/         # Fichiers .wav pré-enregistrés pour les réponses courantes
        ├── screen/
        │   └── Screen.py                   # Gestion des expressions faciales
        ├── servo/
        │   ├── Servo.py                    # Contrôle des servomoteurs
        │   └── servo_preinit.sh            # Script d'initialisation pour éviter que les servomoteurs ne tournent au démarrage
        ├── lib/                            # Modèles et bibliothèques externes (à compléter) 
        │   ├── piper                       # librairie tts (fichier binaire à télécharger)
        │   ├── vosk-model-small-fr-0.22    # Modèle pour la reconnaissance vocale
        │   ├── fr_FR-siwis-medium.onnx     # Modèle de voix du robot
        │   └── fr_FR-siwis-medium.onnx.json
```

### Librairies et modèles

- Audio
    - **sounddevice** (python): lire et enregistrer des tableaux NumPy contenant des signaux audio
    Pour l'installer, il faut au préalable installer **portAudio** via la commande suivante:
    ```bash
    sudo apt install portaudio19-dev libasound2-dev 
    ```

    - **pygame** (python): lire des fichiers .wav

    - **wikipedia** (python): rechercher des pages wikipedia et récupérer des résumés

    - **vosk** (python): pour la reconnaissance vocale
    Pour que la librairie fonctionne, il faut également télécharger un modèle de language via https://alphacephei.com/vosk/models.  
    Pour le projet nous avons choisi le model vosk-model-small-fr-0.22, déposé dans le dossier **lib/**.

    - **piper** (fichier binaire): librairie tts pour l'enregistrement des réponses du robot.

    Pour l'installer, télécharger a version 64-bits du fichier binaire via ce lien: https://github.com/rhasspy/piper, et placer ce dossier dans le répertoire **lib/**.

    Ensuite, télécharger le modèle de voix du robot via ce lien: https://github.com/rhasspy/piper/blob/master/VOICES.md. La version choisie pour le projet est **fr_FR-siwis-medium.onnx**.
    

- Ecran
    - **pygame** (python): dessiner et afficher les expressions du visage du robot
    - **math** (python): utiliser des fonctions courantes pour le dessin des traits

- Servomoteurs
    - **adafruit-circuitpython-servokit** (python): commander les servomoteurs

- Autres
    - **RPI.GPIO** (python): gérer les GPIO de la raspberry
    - **threading** (python): interfaces haut-niveau de fils d'exécutions multiples. Le fichier Main.py gère 4 types de fils d'exécution différents pour: le traitement de l'audio, la lecture de fichiers audios, les servomoteurs et l'écran. 

### Démarrage automatique

Pour que le fichier Main.py s'exécute automatiquement à l'allumage du robot, le fichier bash setup_autostart.sh est nécessaire. De plus, pour éviter que les servomoteurs ne tournent pendant le démarrage du robot, le fichier **setup_autostart.sh** créer le fichier **/home/grp10/p10/projet-pronto/servo/servo_preinit.sh** pour éviter ce disfonctionnement.

1. Déplacer le fichier setup_autostart.sh vers le chemin **/home/grp10/setup_autostart.sh**
2. Rendre le fichier exécutable:
```bash
chmod +x setup_autostart.sh
```
3. Exécuter le fichier avec les privilège administrateur: 
```bash
sudo bash setup_autostart.sh
```

## 4. Points d'amélioration possibles
- Changer le casque audio pour de vrais micro et haut-parleur.
- Faire en sorte que wikipedia ne renvoie pas de phonétique dans le résumé de la page, car piper ne parvient pas à le lire avec son modèle de voix.
- Ajouter un régulateur de tension pour éviter d'avoir 2 alimentations à brancher.
- Redimmensionner les pièces 3D, car certaines pièces ne laissent pas assez de marge, ce qui nous a contraint à limer une partie des pièces.

## 5. Auteurs
Ce projet a été développé par 4 étudiants de l'IMT Atlantique dans le cadre du projet Pronto:

Astrid MARION
Louis BONDUELLE
Coline FELTIN
Florian THOLLOT
