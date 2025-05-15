# Bienvenue sur le projet BobbyLock !

Ce projet a été réalisé en 8h dans le cadre d'un cours d'IoT. 

Il est composé de : 
* Un broker mqtt
* Une application React Native + expo
* Une application python, à ajouter sur un raspberry pi comportant un hat grovepi, et sur lequel a été installé paho-mqtt ainsi que les applications nécessaires. La distribution raspberry pi a été générée grâce à l'outil Buildroot. 


## Pour lancer le broker mqtt 
- s'assurer d'avoir les dossiers suivants dans le dossier mqtt : 
   - config 
   - data
   - log

Puis lancer la commande suivante depuis le dossier mqtt : 
```
docker run -it -d --name mosquitto \
  -p 1883:1883 -p 9001:9001 \
  -v ./mosquitto/config:/mosquitto/config \
  -v ./mosquitto/data:/mosquitto/data \
  -v ./mosquitto/log:/mosquitto/log \
  eclipse-mosquitto
```

## Pour lancer l'app expo
* S'assurer d'avoir npm et npx d'installés
* Se placer dans app/BobbyLock puis:
```
npm install
npx expo start --web
```

