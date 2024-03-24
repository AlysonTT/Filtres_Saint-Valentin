import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np
import random

#classe app, frame Tkinter
class WebcamApp:

    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.window.geometry("800x600")

        #Charger les cascades pré-entraînés
        self.face_cascade = cv2.CascadeClassifier("C:/Users/kimbe/OneDrive/Documents/GitHub/Traitement_Image/projet/haarcascades/haarcascade_frontalface_alt.xml")
        self.mouth_cascade = cv2.CascadeClassifier("C:/Users/kimbe/OneDrive/Documents/GitHub/Traitement_Image/projet/haarcascades/haarcascade_mcs_mouth.xml")
        self.eye_cascade = cv2.CascadeClassifier("C:/Users/kimbe/OneDrive/Documents/GitHub/Traitement_Image/projet/haarcascades/haarcascade_eye_tree_eyeglasses.xml")
        self.upper_body = cv2.CascadeClassifier("C:/Users/kimbe/OneDrive/Documents/GitHub/Traitement_Image/projet/haarcascades/haarcascade_mcs_upperbody.xml")

        #Initialiser l'état des filtres
        self.pink_filter_applied = False
        self.face_detection_enabled = False
        self.mouth_detection_enabled = False
        self.eye_detection_enabled = False
        self.jtm_filter_applied = False
        self.love_filter_bg_applied = False

        #Récupérer le flux vidéo depuis la webcam
        self.cap = cv2.VideoCapture(0)

        #Créer de la zone d'affichage de la vidéo
        self.canvas = tk.Canvas(window, width=800, height=480)
        self.canvas.pack()

        #Ajouter le style pour les boutons
        style = ttk.Style()
        style.configure('TButton', font =('Times New Roman', 11), borderwidth = '1', foreground='#ff1a66', highlightcolor='#ff1a66')
        style.map('TButton', foreground = [('active', '!disabled', '#3399ff')])
        
        #Ajouter des cadres en bas de la fenêtre pour afficher les boutons
        btn_frame = ttk.Frame(window)
        btn_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        #Ajouter le texte "Sélectionner un bouton" au-dessus des boutons
        self.label = ttk.Label(btn_frame, text="Cliquez sur un filtre pour l'appliquer :",
                                foreground='#3399ff', font=('Times New Roman', 13))
        self.label.grid(row=0, column=0, columnspan=6, sticky=tk.W, padx=12, pady=20)

        #Ajouter les boutons pour chacun des filtres dans le cadre
        self.btn1 = ttk.Button(btn_frame, text="Filtre yeux coeur", command=self.yeux_coeur_click)
        self.btn2 = ttk.Button(btn_frame, text="Filtre rose", command=self.rose_click)
        self.btn3 = ttk.Button(btn_frame, text="Filtre baiser", command=self.baiser_click)
        self.btn4 = ttk.Button(btn_frame, text="Filtre fond amour", command=self.fond_amour_click)
        self.btn5 = ttk.Button(btn_frame, text="Filtre fond je t'aime", command=self.fond_jtm_click)
        self.btn6 = ttk.Button(btn_frame, text="Filtre detection visage", command=self.visage_click)

        #Placer les boutons dans le cadre
        self.btn1.grid(row=1, column=0, sticky=tk.W, padx=12, pady=0)
        self.btn2.grid(row=1, column=1, sticky=tk.W, padx=12, pady=0)
        self.btn3.grid(row=1, column=2, sticky=tk.W, padx=12, pady=0)
        self.btn4.grid(row=1, column=3, sticky=tk.W, padx=12, pady=0)
        self.btn5.grid(row=1, column=4, sticky=tk.W, padx=12, pady=0)
        self.btn6.grid(row=1, column=5, sticky=tk.W, padx=12, pady=0)

        #Mettre à jour la vidéo dans la zone d'affichage
        self.update()

        #Fermer la webcam lors de la fermeture de la fenêtre
        self.window.protocol("WM_DELETE_WINDOW", self.quit)

        #Afficher la fenêtre Tkinter principale
        self.window.mainloop()
    
    #Fonction click sur le bouton 1 pour le filtre coeur sur les yeux
    def yeux_coeur_click(self):
        self.eye_detection_enabled = not self.eye_detection_enabled

    #Fonction click sur le bouton 2 pour le filtre rose sur toute la frame
    def rose_click(self):
        self.pink_filter_applied = not self.pink_filter_applied

    #Fonction click sur le bouton 3 pour le filtre baiser sur la bouche
    def baiser_click(self):
        self.mouth_detection_enabled = not self.mouth_detection_enabled

    #Fonction click sur le bouton 4 pour le filtre fond amour
    def fond_amour_click(self):
        self.love_filter_bg_applied = not self.love_filter_bg_applied

    #Fonction click sur le bouton 5 pour le filtre fond je t'aime
    def fond_jtm_click(self):
        self.jtm_filter_applied = not self.jtm_filter_applied

    #Fonction click sur le bouton 6 pour le filtre detection de visage dans un rectangle rose
    def visage_click(self):
        self.face_detection_enabled = not self.face_detection_enabled

    #Fonction pour détetcter le visage, les yeux et la bouche dans le flux vidéo
    def detect_face(self, frame):        
        #Convertir l'image en niveaux de gris pour la détection de visage
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #Détecter les visages dans l'image
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        #Dessiner un rectangle autour de chaque visage détecté
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 255), 2)

            #Région d'intérêt (ROI) pour les yeux dans le visage détecté
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]

            # Détecter les yeux et la bouche à l'aide des classificateurs en cascade sur les régions d'intérêts en niveaux de gris
            eyes = self.eye_cascade.detectMultiScale(roi_gray)
            mouth = self.mouth_cascade.detectMultiScale(roi_gray)

            #Pour chaque paire d'yeux détectée
            for (ex, ey, ew, eh) in eyes:
                # Dessiner une ellipse autour de l'œil
                center = (int(x + ex + ew / 2), int(y + ey + eh / 2))
                axes = (int(ew / 2), int(eh / 2))
                color = (0, 182, 240, 0.8)
                thickness = 1  # Épaisseur de la ligne de l'ellipse
                frame = cv2.ellipse(frame, center, axes, 0, 0, 360, color, thickness)

            #Pour chaque bouche détectée
            if len(mouth) == 1: #Permet de poser une contion supplémentaire afin de limiter les erreurs, demandant de mettre une seule bouche par visage détécté
                for (mx, my, mw, mh) in mouth:
                    #Dessiner une ellipse autour de la bouche
                    mouth_center = (int(x + mx + mw / 2), int(y + my + mh / 2))
                    mouth_axes = (int(mw / 2), int(mh / 2))
                    mouth_color = (56, 245, 78, 0.8)
                    thickness = 1  # Épaisseur de la ligne de l'ellipse
                    frame = cv2.ellipse(frame, mouth_center, mouth_axes, 0, 0, 360, mouth_color, thickness)

        return frame

    #Fonction pour détecter le visage et la bouche et appliquer le filtre baiser sur la bouche
    def mouth_filter(self, frame):
        #Charger l'image de baiser à superposer sur la bouche
        baiser = cv2.imread("C:/Users/kimbe/OneDrive/Documents/GitHub/Traitement_Image/projet/images/kiss.png", -1)

        #Convertir la frame en niveaux de gris
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Détecter le visage à l'aide du classificateur en cascade sur les régions d'intérêts en niveaux de gris
        faces = self.face_cascade.detectMultiScale(gray_frame, 1.1, 4)

        #Pour chaque visage détecté
        for (x, y, w, h) in faces:

            #Région d'intérêt (ROI) pour la bouche dans le visage détecté
            roi_gray = gray_frame[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]

            # Détecter la bouche à l'aide du classificateur en cascade sur les régions d'intérêts en niveaux de gris
            mouth = self.mouth_cascade.detectMultiScale(roi_gray, scaleFactor=1.8, minNeighbors=5)

            #Vérifier s'il y a une seule bouche détectée
            if len(mouth) == 1:

                #Pour chaque bouche détectée
                for (mx, my, mw, mh) in mouth:
                        
                    #Redimensionner l'image à la taille de la bouche
                    resized_baiser = cv2.resize(baiser, (mw, mh))

                    #Superposer l'image sur la bouche
                    x_offset, y_offset = mx, my
                    y1, y2 = y_offset, y_offset + resized_baiser.shape[0]
                    x1, x2 = x_offset, x_offset + resized_baiser.shape[1]

                    # Calcul du canal alpha normalisé de l'image du baiser
                    alpha_s = resized_baiser[:, :, 3] / 255.0
                    # Calcul du complément du canal alpha pour l'image de l'arrière-plan
                    alpha_l = 1.0 - alpha_s
                    # Boucle sur les canaux de couleur
                    for c in range(0, 3):
                        # Combinaison des canaux de couleur de l'image du baiser et de l'arrière-plan
                        roi_color[y1:y2, x1:x2, c] = (alpha_s * resized_baiser[:, :, c] + alpha_l * roi_color[y1:y2, x1:x2, c])

        return frame
    
    #Fonction pour détecter le visage et les yeux et appliquer le filtre coeur sur les yeux
    def eye_filter(self, frame):
        #Charger l'image du coeur à superposer sur les yeux
        heart = cv2.imread("C:/Users/kimbe/OneDrive/Documents/GitHub/Traitement_Image/projet/images/heart.png", -1)

        #Convertir la frame en niveaux de gris
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Détecter le visage à l'aide du classificateur en cascade sur les régions d'intérêts en niveaux de gris
        faces = self.face_cascade.detectMultiScale(gray_frame, 1.1, 4)

        #Pour chaque visage détecté
        for (x, y, w, h) in faces:

            #Région d'intérêt (ROI) pour les yeux dans le visage détecté
            roi_gray = gray_frame[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]

            # Détecter les yeux à l'aide du classificateur en cascade sur les régions d'intérêts en niveaux de gris
            eyes = self.eye_cascade.detectMultiScale(roi_gray)

            #Pour chaque paire d'yeux détectée
            for (ex, ey, ew, eh) in eyes:

                #Redimensionner les coeurs à la taille de l'œil
                resized_coeur = cv2.resize(heart, (ew, eh))

                #Superposer le coeur sur les yeux
                x_offset, y_offset = ex, ey
                y1, y2 = y_offset, y_offset + resized_coeur.shape[0]
                x1, x2 = x_offset, x_offset + resized_coeur.shape[1]

                # Calcul du canal alpha normalisé de l'image du coeur
                alpha_s = resized_coeur[:, :, 3] / 255.0
                # Calcul du complément du canal alpha pour l'image de l'arrière-plan
                alpha_l = 1.0 - alpha_s
                # Boucle sur les canaux de couleur
                for c in range(0, 3):
                    # Combinaison des canaux de couleur de l'image du coeur et de l'arrière-plan
                    roi_color[y1:y2, x1:x2, c] = (alpha_s * resized_coeur[:, :, c] + alpha_l * roi_color[y1:y2, x1:x2, c])

        return frame
    
    #Fonction pour détecter le visage et appliquer le filtre fond je t'aime
    def jtm_filter(self, frame):

        #Charger la police de caractères
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        font_thickness = 2

        #Convertir l'image en niveaux de gris pour la détection de visage
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #Détecter les visages dans l'image à l'aide du classificateur en cascade sur les régions d'intérêts en niveaux de gris
        faces = self.face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        #Récupérer les dimensions de la frame
        height, width, _ = frame.shape

        #Dessiner "Je t'aime" à des positions aléatoires, en évitant les zones de visage détectées
        num_occurrences = 5
        for _ in range(num_occurrences):
            text = "Je t'aime"
            text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]

            #Position aléatoire sur la frame
            text_x = random.randint(0, width - text_size[0])
            text_y = random.randint(text_size[1], height)

            #Vérifier si la position du texte chevauche un visage détecté
            text_overlaps_face = any(
                x - text_size[0] < text_x < x + w and y - text_size[1] < text_y < y + h
                for (x, y, w, h) in faces
            )

            #Si le texte ne chevauche pas un visage, le dessiner
            if not text_overlaps_face:
                text_color = (0, 0, 255)  # Rouge en format BGR
                cv2.putText(frame, text, (text_x, text_y), font, font_scale, text_color, font_thickness, cv2.LINE_AA)

        return frame
    
    def love_filter_bg(self, frame):
        #Chargement de l'image de fond
        background = cv2.imread("C:/Users/kimbe/OneDrive/Documents/GitHub/Traitement_Image/projet/images/valentines-day.jpg")
        width, height = int(self.cap.get(3)), int(self.cap.get(4))
        background = cv2.resize(background, (width, height))

        #Conversion de la frame en niveaux de gris
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #Détection des haut du corps dans la frame à l'aide du classificateur en cascade sur les régions d'intérêts en niveaux de gris
        upper = self.upper_body.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)

        #Copie du haut du corp avant d'appliquer le filtre
        upper_copied = frame.copy()

        #Création d'un masque pour les zones où se trouvent les haut des corps
        mask = np.zeros_like(gray_frame, dtype=np.uint8)
        for (ux, uy, uw, uh) in upper:
            cv2.rectangle(mask, (ux, uy), (ux + uw, uy + uh), (255, 255, 255), -1)
            #Dessiner une bordure rouge autour de la zone des haut du corps avec bordure épaisse rouge pour un effet visuel plus jolie, comme si c'était un cadre
            cv2.rectangle(upper_copied, (ux, uy), (ux + uw, uy + uh), (0, 0, 255), 4)
            
        #Inversion du masque pour les zones sans haut du corps
        inverted_mask = cv2.bitwise_not(mask)
        
        #Remplacement du fond dans les zones sans les haut du corps
        frame_without_upper = cv2.bitwise_and(frame, frame, mask=mask)
        background_without_upper = cv2.bitwise_and(background, background, mask=inverted_mask)

        #Combinaison du fond sans haut du corps et de la frame avec visages
        result_frame = cv2.add(frame_without_upper, background_without_upper)

        #Coller le haut du corps copié à sa place
        for (ux, uy, uw, uh) in upper:
            result_frame[uy:uy+uh, ux:ux+uw] = upper_copied[uy:uy+uh, ux:ux+uw]
        
        return result_frame

    #Mettre à jour l'image de la webcam en continue
    def update(self):
        #Lire la prochaine frame depuis la webcam
        ret, frame = self.cap.read()

        #Appliquer le filtre rose si l'état est activé
        if self.pink_filter_applied:
            pink_filter = np.zeros_like(frame)
            pink_filter[:, :, 0] = 180
            pink_filter[:, :, 1] = 105
            pink_filter[:, :, 2] = 255
            frame = cv2.addWeighted(frame, 1, pink_filter, 0.5, 0)

        #Détecter la bouche et mettre le filtre baiser sur la bouche si la détection de la bouche est activée
        if self.mouth_detection_enabled:
            frame = self.mouth_filter(frame)

        #Détecter les visages et dessiner le rectangle si la détection de visage est activée
        if self.face_detection_enabled:
            frame = self.detect_face(frame)

        #Détecter les yeux et mettre le filtre yeux coeur si la détection des yeux est activée
        if self.eye_detection_enabled:
            frame = self.eye_filter(frame)

        #Détecter les visages et mettre le filtre fond je t'aime
        if self.jtm_filter_applied:
            frame = self.jtm_filter(frame)

        #Détecter les visages et mettre le filtre fond amour
        if self.love_filter_bg_applied:
            frame = self.love_filter_bg(frame)

        #Convertir la frame en image Tkinter
        if ret:
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            photo = ImageTk.PhotoImage(image=image)
            self.canvas.create_image(400, 240, anchor=tk.CENTER, image=photo)
            self.canvas.image = photo

        #Mettre à jour la fenêtre après un délai de 10 ms
        self.window.after(10, self.update)

    def quit(self):
        # Arrêter la capture vidéo et fermer la fenêtre
        self.cap.release()
        self.window.destroy()

# Créer la fenêtre Tkinter et l'application WebcamApp
root = tk.Tk()
app = WebcamApp(root, "Thème: Saint Valentin")
