# Projet Traitement d’images - README

## Note

Lorsque vous utiliserez ce code dans votre propre environnement, assurez-vous de modifier les chemins vers les images et les cascades dans le fichier `main.py` pour correspondre à l'emplacement où vous avez stocké ces fichiers sur votre système. Les chemins actuels sont spécifiques à notre structure de répertoire de projet et doivent être ajustés en conséquence pour garantir le bon fonctionnement du programme.

## Thème: La Saint Valentin

Dans ce projet, nous avons choisi le thème de la Saint Valentin pour allier la technologie et l’émotion. Cette fête offre un large choix en terme de filtres et de masques à utiliser. Des cœurs et des fleurs, des flèches de cupidon et tant d’autres. Dans notre cas, nous avons opté pour des cœurs incrustés sur les yeux symbolisant un regard plein d’amour, un bisous sur la bouche, un filtre rose qui couvre toute la frame, un fond interactif avec le mot « Je t’aime » et un fond statique toujours avec des cœurs.

## Structure du projet

Concernant la structure de notre projet, nous avons créé un fichier principal `main.py` qui contient toutes les fonctions et l’interface que nous avons créées. Le dossier `images` contient toutes les images que nous avons utilisées et incrustées. Dans le dossier `haarcascades`, se trouvent toutes les cascades de Haar que nous avons utilisées pour la détection des visages ainsi que des parties du visage à savoir les yeux et la bouche mais aussi pour la détection du haut du corps.

Dans l’interface, si on clique sur tous les boutons, tous les filtres s’ajoutent entre eux. Il faut cliquer à nouveau dessus pour enlever un filtre. Cliquer sur la croix pour fermer la fenêtre. Pour que le filtre fond marche de manière optimale, se placer devant un fond uni clair facilite la détection du haut du corps. Il faudra aussi faire attention à la lumière ainsi qu'à l’éloignement de la caméra.

## Choix des librairies utilisées

- **OpenCV** : a permis de récupérer la capture vidéo à partir de la webcam en temps réel. Il fournit les outils nécessaires pour la détection des visages et des autres parties du corps grâce à sa capacité pour charger des classificateurs Haar pré-entraînés. Il permet aussi les incrustations des images, l’application de filtres à l’image capturée.
  Installation : `pip install opencv-python`
  
- **Tkinter** : a permis de créer un interface simple avec une fenêtre principale, des cadres pour les boutons et la zone d’affichage de la vidéo.
  Installation : `pip install tk`
  
- **PIL (Pillow)** : a permis d’effectuer des opérations sur les images en les convertissant entre différents formats, notamment entre OpenCV et Tkinter, pour les afficher dans l’interface utilisateur de Tkinter.
  Installation : `pip install Pillow`
  
- **NumPy** : a permis d’effectuer des opérations sur les tableaux d’images, notamment pour créer des masques qui seront utiles pour la détection des visages.
  Installation : `pip install numpy`
  
- **Tkinter.ttk** : a été utilisé pour ajouter du style moderne aux boutons dans notre fenêtre Tkinter.
  Installation : `pip install tk`

## Problèmes rencontrés

Nous avons rencontré quelques problèmes, notamment au niveau de l’incrustation d'un fond en arrière-plan tout en mettant les personnes au premier plan. Nous avons essayé plusieurs techniques pour résoudre ce problème. Voici les étapes que nous avons suivies :

1. Nous avons d'abord essayé d'utiliser un seuillage avec un fond blanc, mais cette méthode était imprécise et ne fonctionnait pas bien avec différents éclairages.
  
2. Ensuite, nous avons tenté de parcourir chaque pixel pour changer les pixels seuillés par le nouveau fond, mais cela a conduit à une lenteur extrême de traitement.
  
3. Finalement, nous avons décidé de faire une copie du visage détecté avant d’appliquer le filtre. Ensuite, nous avons créé un masque pour les zones où se trouvent les visages et inversé celui pour les zones sans visages. Ces zones sans visages ont été remplacées par le nouveau fond. Pour obtenir le résultat final, nous avons combiné le fond sans visages et la frame avec les visages, et collé le visage copié initialement à sa place.

Nous avons également rencontré des problèmes avec la détection des parties du visage, notamment lorsqu'il y avait des vêtements de couleur claire qui pouvaient être confondus avec le fond.

Pour améliorer le rendu visuel, nous avons décidé de détecter tout le haut du corps plutôt que seulement le visage, et d'encadrer les hauts des corps détectés dans un rectangle rouge pour créer un effet de cadre sur le fond.

## Note

Ce projet a été réalisé dans le cadre d'un travail pratique et pourrait nécessiter des ajustements et des améliorations supplémentaires pour une utilisation plus professionnelle.
