Une fois monté, pour faire fonctionner le robot, il faut et il suffit de le connecter au wifi.<br>

Pour cela, il faut rentrer dans le terminal de la raspberry via une des méthodes suivantes:
1. (Pour changer de wifi) Se connecter à la raspberry via SSH avec l'ancien wifi auquel est connectée la raspberry via la commande suivante:
```bash
ssh grp10@rpi.local
```
2. (Si la connection wifi a sautée) 
    - Soulever délicatement la partie bleue du socle pour sortir la raspberry
    - Brancher un clavier aux ports USB de la raspberry 
    - Aller dans le terminal de a raspberry à l'aide du clavier et de l'écran du robot (si l'écran est trop petit, débrancher le câble HDMI pour brancher un autre écran)

Ensuite, il faut modifier la configuration wifi en suivant ces commandes:
```bash
sudo raspi-config
-> "System Options"
-> "Wireless LAN"
```
puis entrer le SSID et le mot de passe souhaité.

Le robot peut fonctionner !
