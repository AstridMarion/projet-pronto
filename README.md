# Robot Compagnon
Ce robot est un robot interactif capable de répondre aux questions vocales en utilisant Wikipedia, avec expressions faciales et mouvements corporels.

## Description
Ce robot compagnon est conçu pour interagir naturellement avec les utilisateurs à travers :

**Reconnaissance vocale** : Écoute et comprend les requêtes (un seul mot ou groupe de mots) en français quand l'utilisateur maintient le bouton poussoir 
**Recherche sur wikipedia** : Utilise Wikipedia pour fournir un résumé en une phrase de la page correspondante à la requête de l'utilisateur.
**Synthèse vocale** : Répond avec une voix de synthèse
**Expressions faciales** : Affiche différentes expressions sur écran selon le contexte (speaking, teaching, waiting, thinking)
**Mouvements** : Gesticule avec les bras et la tête pendant les interactions

## Fonctionnalités

### Interface Multimodale
**Audio** : Enregistrement lorsque le bouton poussoir est maintenu avec sounddevice, reconnaissance vocale avec Vosk, recherche sur le web avec wikipedia, synthèse vocale avec Piper pour générer la réponse.
**Visuel** : Écran avec expressions faciales animées (parlant, enseignant, attente, réflexion)
**Gestuelle** : Servomoteurs pour les 2 bras et la tête avec mouvements synchronisés.

### Modes d'Expression
Mode **waiting** : Visage souriant, sans mouvement
Mode **thinking** : Sourire avec engrenages, sans mouvement
Mode **teaching** : Lunettes et animation bouche pour les réponses
Mode **speaking** : Animation bouche pendant les réponses et la phrase d'accueil.

## Architecture Technique

### Structure de l'environnement

grp10/<br>                                  # Dossier utilisateur<br>
├── setup_autostart.sh                      # Fichier de démarrage automatique après allumage<br>
├── ...<br>
└── p10/                                    # Environnement virtuel Python<br>
>   ├── bin/<br>
>   ├── lib/<br>
>   ├── ...<br>
>   └── projet-pronto/                      # Dossier mère du projet<br>
>>      ├── Main.py                         # Point d'entrée et orchestration principale<br>
>>      ├── audio/<br>
>>      │   ├── AudioProcessing.py          # Acquisition, reconnaissance et synthèse vocale<br>
>>      │   ├── Speak.py                    # Lecture de fichiers audio<br>
>>      │   └── preRecordedDialogs/         # Fichiers .wav pré-enregistrés pour les réponses courantes<br>
>>      ├── screen/<br>
>>      │   └── Screen.py                   # Gestion des expressions faciales<br>
>>      ├── servo/<br>
>>      │   ├── Servo.py                    # Contrôle des servomoteurs<br>
>>      │   └── servo_preinit.sh            # Script d'initialisation pour éviter que les servomoteurs ne tournent au démarrage<br>
>>      └── lib/                            # Modèles et bibliothèques externes (à compléter avec piper et vosk)<br>


### Composants électroniques 
- **Raspberry Pi 4 model b** avec GPIO pour l'interface matérielle
- **Casque USB**
- **bouton poussoir**
- **résistance** (1 kΩ) 
- **Module de commande ADA815**
- **3 servomoteurs continues**
- **Ecran** LCD UCTRONICS B0106
- **Câbles**: alimentation raspberry avec boîtier (3A, 5.1V) / hub USB (2 ports) / câbles Dupont (x8) / HDMI-HDMI mini (pour l'écran) / USB-micro_USB (alim écran) / alim module servo / adaptateur USB-secteur 

### Configuration 
- installation de l'OS
- Activer I2C pour l'écran et le module de contrôle des servomoteurs: 
```bash
sudo raspi-config
> "Interfacing Options" 
> "I2C"
> Enable 
```

- Audio:
    sudo raspi-config > systeme option > audio > choose USB

### Librairies et model
- audio
    - **sounddevice** (python): lire et enregistrer des tableaux NumPy contenant des signaux audio
    Pour l'installer, il faut au préalable installer **portAudio** via la commande suivante:
    ```bash
    sudo apt install portaudio19-dev libasound2-dev 
    ```
    - **wikipedia** (python): rechercher des pages wikipedia et récupérer des résumés
    - **vosk** (python): pour la reconnaissance vocale
    

Vosk pour la reconnaissance vocale (français)
Piper pour la synthèse vocale
Wikipedia API pour la recherche d'informations
Pygame pour l'interface graphique
Threading pour la gestion parallèle des tâches
Installation
Prérequis Système
Raspberry Pi avec Raspbian/Raspberry Pi OS
Python 3.7+
Connexion internet pour Wikipedia
Microphone USB sur port 1
Écran pour l'affichage facial
Servomoteurs connectés via ServoKit (canaux 0, 1, 2)
Bouton poussoir sur GPIO 4
Dépendances Python
bash
pip install RPi.GPIO sounddevice numpy queue wave pygame wikipedia vosk adafruit-servokit
Modèles Requis
Placez dans le dossier lib/ :

vosk-model-small-fr-0.22 : Modèle de reconnaissance vocale française
fr_FR-siwis-medium.onnx : Modèle de synthèse vocale française
piper/ : Exécutable Piper pour la synthèse vocale
Configuration Matérielle
GPIO 4 : Bouton poussoir (pull-up interne)
GPIO 17 : Pin OE pour contrôle des servomoteurs
USB Port 1 : Microphone
Servomoteurs :
Canal 0 : Bras gauche
Canal 1 : Tête
Canal 2 : Bras droit
Utilisation
Démarrage
bash
# Initialisation des servomoteurs (optionnel)
sudo bash servo/servo_preinit.sh

# Lancement du robot
python3 Main.py
Interaction
Démarrage : Le robot se présente et explique son fonctionnement
Question : Maintenez le bouton poussoir et posez votre question
Traitement : Le robot réfléchit et recherche la réponse
Réponse : Le robot répond avec gestes et expressions appropriées
Flux d'Interaction
Présentation → Écoute → Traitement → Réponse → Écoute...
Architecture Logicielle
Threading
Le système utilise plusieurs threads parallèles :

Screen Thread : Affichage continu des expressions faciales
Audio Thread : Acquisition, traitement et synthèse audio
Servo Threads : Contrôle indépendant de chaque servomoteur
Speak Threads : Lecture des fichiers audio
Synchronisation
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
Dépannage
Problèmes Fréquents
Pas de son : Vérifiez la configuration audio de pygame
Servomoteurs inertes : Contrôlez le GPIO 17 et l'alimentation
Reconnaissance vocale défaillante : Vérifiez le microphone et le modèle Vosk
Écran noir : Vérifiez pygame et l'affichage fullscreen
Logs et Debug
Les erreurs sont affichées dans la console avec identification du thread concerné.

Licence
Ce projet est développé dans un cadre éducatif. Consultez les licences des bibliothèques tierces utilisées.

Contribution
Pour contribuer au projet :

Forkez le repository
Créez une branche pour votre fonctionnalité
Testez vos modifications sur hardware
Soumettez une merge request avec description détaillée
Auteurs
Développé par l'équipe Groupe Pronto - IMT Atlantique

Robot Compagnon - Une interface naturelle et interactive pour l'apprentissage et la découverte

# projet-pronto
