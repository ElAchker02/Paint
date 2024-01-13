import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageGrab,ImageDraw
from tkinter import colorchooser
from tkinter import filedialog

def changerCouleurStylo(self,couleur):
        self.couleur = couleur

class ApplicationDessin:
    def __init__(self, fenetre):
        self.fenetre = fenetre
        self.fenetre.title("Paint")
        self.fenetre.geometry('1200x600')
        self.fenetre.minsize(1200, 600)
        self.fenetre.iconbitmap("icone/icon.ico")

        self.epesseure = 1
        self.couleur = "black"

        self.menu = tk.Menu(fenetre)
        fenetre.config(menu=self.menu)

        # Ajouter des boutons de test au menu
        self.menu.add_command(label="Nouveau", command=self.nouveau_dessin)
        self.menu.add_command(label="Enregistrer", command=self.enregistrer_dessin)
        self.menu.add_command(label="Arrière-plan", command=self.changer_couleur_arrier_plan)
        self.menu.add_command(label="Quitter", command=self.quitter_application)

        # Cree le canvas
        self.canvas_arriere_plan = "white"
        self.canvas = tk.Canvas(fenetre, bg=self.canvas_arriere_plan, width=800, height=600)
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Create vertical and horizontal scrollbars
        self.v_scrollbar = tk.Scrollbar(self.canvas, orient="vertical", command=self.canvas.yview)
        self.h_scrollbar = tk.Scrollbar(self.canvas, orient="horizontal", command=self.canvas.xview)

        # Configure the canvas to use the scrollbars
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)

        # Pack the scrollbars to the right and bottom of the canvas
        self.v_scrollbar.pack(side="right", fill="y")
        self.h_scrollbar.pack(side="bottom", fill="x")

        # Create a PIL Image to draw on
        self.image = Image.new("RGB", (800, 600), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.configurer_sidebar()

        self.outil_actuel = "ligne_courbee"
        self.forme_actuelle = None
        self.start_x = None
        self.start_y = None

        # les évenements apliquer sur la souris
        self.canvas.bind("<ButtonPress-1>", self.on_appui_bouton)
        self.canvas.bind("<B1-Motion>", self.on_glissement_souris)
        self.canvas.bind("<ButtonRelease-1>", self.on_relachement_bouton)
        self.canvas.bind("<MouseWheel>", self.on_scroll_souris)
        self.fenetre.protocol("WM_DELETE_WINDOW", self.quitter_application)

    def quitter_application(self):
            reponse = tk.messagebox.askyesnocancel("Quitter", "Voulez-vous enregistrer les modifications avant de quitter ?")

            if reponse is True:
                self.enregistrer_dessin()
                self.fenetre.destroy()
            if reponse is False:
                self.fenetre.destroy()
            else:
                return
            
    def on_scroll_souris(self, evenement):
        # Check if the Ctrl key is pressed
        if evenement.state & 0x4:
            # Zoom in or out based on the direction of the mouse wheel
            if evenement.delta > 0:
                self.zoom_in()
            else:
                self.zoom_out()

    def zoom_in(self):
        # Increase the scale factor for zooming in
        self.canvas.scale("all", 0, 0, 1.1, 1.1)

    def zoom_out(self):
        # Decrease the scale factor for zooming out
        self.canvas.scale("all", 0, 0, 0.9, 0.9)

    def redimensionner_icone(self, chemin_icone, largeur=20, hauteur=20):
        icone_originale = Image.open(chemin_icone)
        icone_redimensionnee = icone_originale.resize((largeur, hauteur), resample=Image.LANCZOS)
        return ImageTk.PhotoImage(icone_redimensionnee)

    def configurer_sidebar(self):
        sidebar = tk.Frame(self.fenetre, width=250, relief="raised",bg="#62C5FE")
        sidebar.pack(side=tk.LEFT, fill=tk.BOTH)

        outils_forme1 = tk.Frame(sidebar,height=100, borderwidth=2, width=250,  relief="raised", bg="#eee")
        outils_forme1.pack(side=tk.TOP, fill=tk.BOTH, pady=10, padx=20)

        outils_forme1_1 = tk.Frame(sidebar, height=100, borderwidth=2, width=250,  relief="raised", bg="#eee")
        outils_forme1_1.pack(side=tk.TOP,  fill=tk.BOTH, pady=10, padx=20)
        

        outils_forme2 = tk.Frame(sidebar,borderwidth=2, width=250,  relief="raised", bg="#eee")
        outils_forme2.pack(side=tk.TOP, fill=tk.BOTH, pady=10, padx=20)


        # Chargez les icônes pour les boutons
        icone_cercle = self.redimensionner_icone("icone/circle.png")
        icone_rectangle = self.redimensionner_icone("icone/rectangle.png")
        icone_triangle = self.redimensionner_icone("icone/triangle.png")
        icone_ligne_pliee = self.redimensionner_icone("icone/straightLine.png")
        icone_ligne_courbee = self.redimensionner_icone("icone/drawing.png")
        icone_rectangle_arrondie = self.redimensionner_icone("icone/rounded-rectangle.png")
        icone_parallelogramme = self.redimensionner_icone("icone/parallelogram.png")
        icone_clear =self.redimensionner_icone("icone/broom.png")
        icone_gomme =self.redimensionner_icone("icone/eraser.png")
        icone_text =self.redimensionner_icone("icone/text.png")
        icone_choisir_couleur =self.redimensionner_icone("icone/rgb.png")
        icone_fleshs =self.redimensionner_icone("icone/four-arrows.png")
        

        # Ajoutez les boutons avec les icônes dans outils_forme2
        bouton_cercle = tk.Button(outils_forme2,width=25,height=25, image=icone_cercle,relief=tk.RAISED, command=lambda: self.definir_outil("cercle"),cursor="tcross")
        bouton_cercle.image = icone_cercle
        bouton_cercle.grid(row=0, column=0, pady=5, padx=10)

        bouton_rectangle = tk.Button(outils_forme2, width=25,height=25,image=icone_rectangle,relief=tk.RAISED, command=lambda: self.definir_outil("rectangle"),cursor="tcross")
        bouton_rectangle.image = icone_rectangle
        bouton_rectangle.grid(row=0, column=2, pady=5, padx=10)

        bouton_triangle = tk.Button(outils_forme2, width=25,height=25,image=icone_triangle,relief=tk.RAISED, command=lambda: self.definir_outil("triangle"),cursor="tcross")
        bouton_triangle.image = icone_triangle
        bouton_triangle.grid(row=0, column=4, pady=5, padx=10)

        bouton_rectangle_arrondie = tk.Button(outils_forme2, width=25,height=25,image=icone_rectangle_arrondie,relief=tk.RAISED, command=lambda: self.definir_outil("rectangle_arrondi"),cursor="tcross")
        bouton_rectangle_arrondie.image = icone_rectangle_arrondie
        bouton_rectangle_arrondie.grid(row=0, column=6, pady=5, padx=10)

        bouton_parallelogramme = tk.Button(outils_forme2,width=25,height=25, image=icone_parallelogramme,relief=tk.RAISED, command=lambda: self.definir_outil("parallelogramme"),cursor="tcross")
        bouton_parallelogramme.image = icone_parallelogramme
        bouton_parallelogramme.grid(row=0, column=8, pady=5, padx=10)

        flesh_haut = tk.Button(outils_forme2, width=25,height=25,image=icone_fleshs,relief=tk.RAISED, command=lambda: self.definir_outil("fleshs"),cursor="tcross")
        flesh_haut.image = icone_fleshs
        flesh_haut.grid(row=1, column=4, pady=5, padx=10)

        # Ajoutez les boutons avec les icônes dans outils_forme1
        bouton_ligne_pliee = tk.Button(outils_forme1,width=25,height=25, image=icone_ligne_pliee,relief=tk.RAISED, command=lambda: self.definir_outil("ligne_pliee"),cursor="pencil")
        bouton_ligne_pliee.image = icone_ligne_pliee
        bouton_ligne_pliee.grid(row=0, column=0, pady=5, padx=10)

        bouton_ligne_courbee = tk.Button(outils_forme1, width=25,height=25,image=icone_ligne_courbee,relief=tk.RAISED, command=lambda: self.definir_outil("ligne_courbee"),cursor="pencil")
        bouton_ligne_courbee.image = icone_ligne_courbee
        bouton_ligne_courbee.grid(row=0, column=2, pady=5, padx=10)

        bouton_clear= tk.Button(outils_forme1, width=25,height=25,image=icone_clear,relief=tk.RAISED, command=self.clear_canvas)
        bouton_clear.image = icone_clear
        bouton_clear.grid(row=0, column=4, pady=5, padx=10)

        bouton_gomme = tk.Button(outils_forme1,width=25,height=25, image=icone_gomme,relief=tk.RAISED, command=lambda: self.definir_outil("gomme"),cursor="circle")
        bouton_gomme.image = icone_gomme
        bouton_gomme.grid(row=0, column=6, pady=5, padx=10)

        # xterm
        bouton_text = tk.Button(outils_forme1, width=25,height=25,image=icone_text,relief=tk.RAISED,)
        bouton_text.image = icone_text
        bouton_text.grid(row=0, column=8, pady=5, padx=10)


        # Initialiser la valeur du width pour le pen
        self.pen_width = tk.DoubleVar(value=1.0)
        # Créer le widget Scale pour ajuster le width du pen
        self.width_scale_label = ttk.Label(outils_forme1_1, text="Width Pen:")
        self.width_scale_label.pack(pady=5, padx=90, anchor=tk.W)
        self.width_scale = ttk.Scale(outils_forme1_1, from_=1.0, to=30.0, variable=self.pen_width, orient=tk.HORIZONTAL)
        self.width_scale.pack(pady=10, padx=75, anchor=tk.W)

        # Lier les fonctions de mise à jour du width à l'événement de mouvement du curseur
        self.width_scale.bind("<B1-Motion>", self.update_width)
        # self.eraser_width_scale.bind("<B1-Motion>", self.update_eraser_width)

         # Créer le cadre palette de couleur
        self.outils_forme3 = tk.Frame(sidebar, borderwidth=2, width=250,  relief="raised", bg="#eee")
        self.outils_forme3.pack(side=tk.TOP, fill=tk.BOTH, pady=10, padx=20)

        # Créer d'autres éléments dans tbframe (par exemple, des étiquettes, des boutons)...
        etiquette = tk.Label(self.outils_forme3, text="Couleurs")
        etiquette.grid(row=0, column=0)

        # Créer le cadre extérieur
        cadre_interieur = tk.Frame(self.outils_forme3,width=250,  bg="black",relief="sunken")
        cadre_interieur.grid(row=1, column=0)

        # Créer le cadre de couleur
        cadre_couleur = tk.Frame(cadre_interieur, bg='#eee', width=300, borderwidth=1, relief='sunken', padx=10, pady=10)
        cadre_couleur.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        # Définir les couleurs et les boutons correspondants
        couleurs = ['black', 'grey', 'brown', 'orange', 'yellow', 'red', 'green', 'turquoise',
                'indigo', 'purple', 'blue', 'white', 'lime', 'pink', 'gold', 'cyan']

        # Calculer le nombre de colonnes et de lignes
        num_colonnes = 8
        # num_lignes = len(couleurs) // num_colonnes + (1 if len(couleurs) % num_colonnes != 0 else 0)

        # boutons = []
        for i, couleur in enumerate(couleurs):
            bouton = tk.Button(cadre_couleur, bg=couleur, width=2, height=1,relief=tk.RAISED, command=lambda c=couleur: changerCouleurStylo(self,c))
            ligne = i // num_colonnes
            colonne = i % num_colonnes
            bouton.grid(row=ligne, column=colonne, padx=2, pady=2)

        bouton_choix_couleur = tk.Button(cadre_interieur,relief=tk.RAISED, image=icone_choisir_couleur, command=self.ouvrir_choix_couleur)
        bouton_choix_couleur.image = icone_choisir_couleur
        bouton_choix_couleur.grid(row=1, column=0, pady=5, padx=10)

    def definir_outil(self, outil):
        self.outil_actuel = outil

    def on_appui_bouton(self, evenement):
        self.start_x = self.canvas.canvasx(evenement.x)
        self.start_y = self.canvas.canvasy(evenement.y)

        if self.outil_actuel == "cercle":
            self.forme_actuelle = self.canvas.create_oval(self.start_x, self.start_y, self.start_x, self.start_y ,outline=self.couleur,width=self.epesseure )
            self.canvas.config(cursor="tcross")
        elif self.outil_actuel == "rectangle":
            self.forme_actuelle = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y ,outline=self.couleur,width=self.epesseure)
            self.canvas.config(cursor="tcross")
        elif self.outil_actuel == "triangle":
            self.forme_actuelle = self.canvas.create_polygon(self.start_x, self.start_y, self.start_x, self.start_y,fill="" ,outline=self.couleur,width=self.epesseure)
            self.canvas.config(cursor="tcross")
        elif self.outil_actuel == "ligne_pliee":
            self.forme_actuelle = self.canvas.create_line(self.start_x, self.start_y, self.start_x, self.start_y, fill=self.couleur, smooth=True,width=self.epesseure)
            self.canvas.config(cursor="pencil")
        elif self.outil_actuel == "ligne_courbee":
            self.forme_actuelle = self.canvas.create_line(self.start_x, self.start_y, self.start_x, self.start_y, fill=self.couleur, smooth=True,width=self.epesseure)
            self.points_courbe = [self.start_x, self.start_y]  # Liste pour stocker les points de contrôle pour la courbe
            self.canvas.config(cursor="pencil")
        elif self.outil_actuel == "rectangle_arrondi":
            self.forme_actuelle = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline=self.couleur,width=self.epesseure)
            self.canvas.config(cursor="tcross")
        elif self.outil_actuel == "gomme":
            self.forme_actuelle = self.canvas.create_line(self.start_x, self.start_y, self.start_x, self.start_y, fill="white", smooth=True,width=self.epesseure)
            self.points_courbe = [self.start_x, self.start_y]  
            self.canvas.config(cursor="circle")
        elif self.outil_actuel == "parallelogramme":  
            self.forme_actuelle = self.canvas.create_polygon(self.start_x, self.start_y, self.start_x, self.start_y, fill="", outline=self.couleur, width=self.epesseure)
            self.canvas.config(cursor="tcross")
        elif self.outil_actuel == "fleshs":
            self.forme_actuelle = self.canvas.create_line(self.start_x, self.start_y, self.start_x, self.start_y, fill=self.couleur, arrow=tk.LAST, width=3)
            self.canvas.config(cursor="tcross")

    def on_glissement_souris(self, evenement):
        cur_x = self.canvas.canvasx(evenement.x)
        cur_y = self.canvas.canvasy(evenement.y)

        if self.outil_actuel in ["cercle", "rectangle"]:
            self.canvas.coords(self.forme_actuelle, self.start_x, self.start_y, cur_x, cur_y)
        elif self.outil_actuel == "triangle":
            self.canvas.coords(self.forme_actuelle, self.start_x, self.start_y, cur_x, cur_y, 2 * self.start_x - cur_x, cur_y)
        elif self.outil_actuel == "ligne_pliee":
            self.canvas.coords(self.forme_actuelle, self.start_x, self.start_y, cur_x, cur_y)
        elif self.outil_actuel == "ligne_courbee":
            self.points_courbe.extend([cur_x, cur_y])
            self.canvas.coords(self.forme_actuelle, *self.points_courbe)
        elif self.outil_actuel == "rectangle_arrondi":
            self.canvas.coords(self.forme_actuelle, self.start_x, self.start_y, cur_x, cur_y)
        elif self.outil_actuel == "gomme":
            self.points_courbe.extend([cur_x, cur_y])
            self.canvas.coords(self.forme_actuelle, *self.points_courbe)
        elif self.outil_actuel == "parallelogramme": 
            self.canvas.coords(self.forme_actuelle, self.start_x, self.start_y, cur_x, self.start_y, cur_x + (cur_x - self.start_x), cur_y, self.start_x + (cur_x - self.start_x), cur_y)
        elif self.outil_actuel == "fleshs":
            self.canvas.coords(self.forme_actuelle, self.start_x, self.start_y, cur_x, cur_y)

    def on_relachement_bouton(self, evenement):
        pass

    def nouveau_dessin(self):
        file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            self.clear_canvas()
            self.image = Image.open(file_path)
            self.draw = ImageDraw.Draw(self.image)
            self.tk_image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def enregistrer_dessin(self):
            self.v_scrollbar.pack_forget()
            self.h_scrollbar.pack_forget()

            x = self.fenetre.winfo_rootx() + self.canvas.winfo_x()
            y = self.fenetre.winfo_rooty() + self.canvas.winfo_y()
            x1 = self.canvas.winfo_width()
            y1 = self.canvas.winfo_height()

            self.path = filedialog.asksaveasfilename(initialdir='C:/Users', title='Save', defaultextension=".png")
            captured_image = ImageGrab.grab().crop((x, y, x + x1, y + y1))
            resized_image = captured_image.resize((1200, 800), Image.LANCZOS)
            resized_image.save(self.path, format="PNG")
            
            self.v_scrollbar.pack(side="right", fill="y")
            self.h_scrollbar.pack(side="bottom", fill="x")

    def clear_canvas(self):
        self.canvas.delete("all")

    def update_width(self, evenement):
            # Fonction appelée lors du déplacement du curseur du width du pen
            new_width = int(self.width_scale.get())
            self.width_scale_label.config(text="Width : "+str(new_width))
            self.epesseure = new_width

    def ouvrir_choix_couleur(self):
        couleur_choisie = colorchooser.askcolor()[1]  # Obtenir le code couleur hexadécimal
        if couleur_choisie:
            changerCouleurStylo(self,couleur_choisie)

    def changer_couleur_arrier_plan(self):
        couleur = colorchooser.askcolor()[1]  # Opens a color picker dialog
        if couleur:
            self.canvas_arriere_plan = couleur
            self.canvas.configure(bg=self.canvas_arriere_plan) 



if __name__ == "__main__":
    root = tk.Tk()
    app = ApplicationDessin(root)
    root.mainloop()