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

        # Cree les scroll bar
        self.v_scrollbar = tk.Scrollbar(self.canvas, orient="vertical", command=self.canvas.yview)
        self.h_scrollbar = tk.Scrollbar(self.canvas, orient="horizontal", command=self.canvas.xview)

        # Configurer le canva pour utiliser les scroll bar
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)

        self.v_scrollbar.pack(side="right", fill="y")
        self.h_scrollbar.pack(side="bottom", fill="x")

        # Creer image PIL pour dessiner
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

        # varibele pour l'emplacement de text.
        self.text_entry = None
        self.texte_a_afficher="" ## pour enregistrer le text taper 
        self.font_styles = [] ## pour entregistrer les styles de text 
        self.text_color = "black" ## text couleur par default 
        self.text_size = 50 ## text taille par default 


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
        if evenement.state & 0x4:
            if evenement.delta > 0:
                self.zoom_in()
            else:
                self.zoom_out()

    def zoom_in(self):
        self.canvas.scale("all", 0, 0, 1.1, 1.1)

    def zoom_out(self):
        self.canvas.scale("all", 0, 0, 0.9, 0.9)

    def redimensionner_icone(self, chemin_icone, largeur=20, hauteur=20):
        icone_originale = Image.open(chemin_icone)
        icone_redimensionnee = icone_originale.resize((largeur, hauteur), resample=Image.LANCZOS)
        return ImageTk.PhotoImage(icone_redimensionnee)

    def configurer_sidebar(self):
        sidebar = tk.Frame(self.fenetre, width=250, relief="raised",bg="#738BD7")
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
        icone_carre = self.redimensionner_icone("icone/square.png")
        icone_parallelogramme = self.redimensionner_icone("icone/parallelogram.png")
        icone_clear =self.redimensionner_icone("icone/broom.png")
        icone_gomme =self.redimensionner_icone("icone/eraser.png")
        icone_text =self.redimensionner_icone("icone/text.png")
        icone_choisir_couleur =self.redimensionner_icone("icone/rgb.png")
        icone_fleshs =self.redimensionner_icone("icone/four-arrows.png")
        icone_ligne_discontinue =self.redimensionner_icone("icone/dashed-line.png")
        

        # Ajoutez les boutons avec les icônes dans outils_forme2
        lblFormes = tk.Label(outils_forme2, text="Formes",font=("Arial",10,"bold"))
        lblFormes.pack(pady=5, padx=90, anchor=tk.W)
        lblFormes.grid(row=0, column=4, pady=5, padx=10)

        bouton_cercle = tk.Button(outils_forme2,width=25,height=25, image=icone_cercle,relief=tk.RAISED, command=lambda: self.definir_outil("cercle"),cursor="tcross")
        bouton_cercle.image = icone_cercle
        bouton_cercle.grid(row=1, column=0, pady=5, padx=10)

        bouton_rectangle = tk.Button(outils_forme2, width=25,height=25,image=icone_rectangle,relief=tk.RAISED, command=lambda: self.definir_outil("rectangle"),cursor="tcross")
        bouton_rectangle.image = icone_rectangle
        bouton_rectangle.grid(row=1, column=2, pady=5, padx=10)

        bouton_triangle = tk.Button(outils_forme2, width=25,height=25,image=icone_triangle,relief=tk.RAISED, command=lambda: self.definir_outil("triangle"),cursor="tcross")
        bouton_triangle.image = icone_triangle
        bouton_triangle.grid(row=1, column=4, pady=5, padx=10)

        bouton_rectangle_arrondie = tk.Button(outils_forme2, width=25,height=25,image=icone_carre,relief=tk.RAISED, command=lambda: self.definir_outil("rectangle_arrondi"),cursor="tcross")
        bouton_rectangle_arrondie.image = icone_carre
        bouton_rectangle_arrondie.grid(row=1, column=6, pady=5, padx=10)

        bouton_parallelogramme = tk.Button(outils_forme2,width=25,height=25, image=icone_parallelogramme,relief=tk.RAISED, command=lambda: self.definir_outil("parallelogramme"),cursor="tcross")
        bouton_parallelogramme.image = icone_parallelogramme
        bouton_parallelogramme.grid(row=1, column=8, pady=5, padx=10)

        fleshs = tk.Button(outils_forme2, width=25,height=25,image=icone_fleshs,relief=tk.RAISED, command=lambda: self.definir_outil("fleshs"),cursor="tcross")
        fleshs.image = icone_fleshs
        fleshs.grid(row=2, column=4, pady=5, padx=10)

        # Ajoutez les boutons avec les icônes dans outils_forme1
        lblOutils = tk.Label(outils_forme1, text="Outils",font=("Arial",10,"bold"))
        lblOutils.pack(pady=5, padx=90, anchor=tk.W)
        lblOutils.grid(row=0, column=4, pady=5, padx=10)

        bouton_ligne_pliee = tk.Button(outils_forme1,width=25,height=25, image=icone_ligne_pliee,relief=tk.RAISED, command=lambda: self.definir_outil("ligne_pliee"),cursor="pencil")
        bouton_ligne_pliee.image = icone_ligne_pliee
        bouton_ligne_pliee.grid(row=1, column=0, pady=5, padx=10)

        bouton_ligne_courbee = tk.Button(outils_forme1, width=25,height=25,image=icone_ligne_courbee,relief=tk.RAISED, command=lambda: self.definir_outil("ligne_courbee"),cursor="pencil")
        bouton_ligne_courbee.image = icone_ligne_courbee
        bouton_ligne_courbee.grid(row=1, column=2, pady=5, padx=10)

        ligne_discontinue = tk.Button(outils_forme1, width=25,height=25,image=icone_ligne_discontinue,relief=tk.RAISED, command=lambda: self.definir_outil("ligne_discontinue"),cursor="tcross")
        ligne_discontinue.image = icone_ligne_discontinue
        ligne_discontinue.grid(row=1, column=4, pady=5, padx=10)

        bouton_gomme = tk.Button(outils_forme1,width=25,height=25, image=icone_gomme,relief=tk.RAISED, command=lambda: self.definir_outil("gomme"),cursor="circle")
        bouton_gomme.image = icone_gomme
        bouton_gomme.grid(row=1, column=6, pady=5, padx=10)

        bouton_text = tk.Button(outils_forme1, width=25,height=25,image=icone_text,relief=tk.RAISED,command=lambda: self.definir_outil("text"),cursor="xterm")
        bouton_text.image = icone_text
        bouton_text.grid(row=1, column=8, pady=5, padx=10)

        bouton_clear= tk.Button(outils_forme1, width=25,height=25,image=icone_clear,relief=tk.RAISED, command=self.clear_canvas)
        bouton_clear.image = icone_clear
        bouton_clear.grid(row=2, column=4, pady=5, padx=10)

        # Initialiser la valeur du epaisseur pour le stylo
        self.pen_width = tk.DoubleVar(value=1.0)

        # Créer le widget Scale pour ajuster l'epaisseur pour le stylo
        self.width_scale_label = ttk.Label(outils_forme1_1, text="Epaisseur :",font=("Arial",10,"bold"))
        self.width_scale_label.pack(pady=5, padx=100, anchor=tk.W)
        self.width_scale = ttk.Scale(outils_forme1_1, from_=1.0, to=30.0, variable=self.pen_width, orient=tk.HORIZONTAL)
        self.width_scale.pack(pady=10, padx=95, anchor=tk.W)

        # Lier les fonctions de mise à jour du width à l'événement de mouvement du curseur
        self.width_scale.bind("<B1-Motion>", self.modifier_epaisseur)

        # Créer le cadre palette de couleur
        self.outils_forme3 = tk.Frame(sidebar, borderwidth=2, width=250,  relief="raised", bg="#eee")
        self.outils_forme3.pack(side=tk.TOP, fill=tk.BOTH, pady=10, padx=20)

        etiquette = tk.Label(self.outils_forme3, text="Couleurs",font=("Arial",10,"bold"))
        etiquette.grid(row=0, column=0,padx=100)

        # Créer le cadre extérieur
        cadre_interieur = tk.Frame(self.outils_forme3,width=250,  bg="#eee",relief="sunken")
        cadre_interieur.grid(row=1, column=0)

        # Créer le cadre de couleur
        cadre_couleur = tk.Frame(cadre_interieur, bg='#eee', width=300, borderwidth=1, relief='sunken', padx=10, pady=10)
        cadre_couleur.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        # Définir les couleurs et les boutons correspondants
        couleurs = ['black', 'grey', 'brown', 'orange', 'yellow', 'red', 'green', 'turquoise',
                'indigo', 'purple', 'blue', 'white', 'lime', 'pink', 'gold', 'cyan']

        # Calculer le nombre de colonnes et de lignes
        num_colonnes = 8
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
            self.points_courbe = [self.start_x, self.start_y]
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
        elif self.outil_actuel == "text" : 
            self.canvas.config(cursor="xterm")
            if self.canvas.type(tk.CURRENT) == "text":
                # Afficher une boîte de dialogue avec le texte stocké
                current_text = self.canvas.itemcget(tk.CURRENT, "text")
                # Demandez à l'utilisateur de modifier le texte
                new_text = tk.simpledialog.askstring("Modifier le texte", "Nouveau texte :", initialvalue=current_text)
                if new_text:
                    # Mettez à jour le texte sur le canevas
                    self.canvas.itemconfig(tk.CURRENT, text=new_text)

            else:
            # Sinon, créer un nouveau texte sur le canevas
                self.ajouter_texte()    
        elif self.outil_actuel=="ligne_discontinue":
            self.forme_actuelle = self.canvas.create_line(self.start_x, self.start_y, self.start_x, self.start_y, fill=self.couleur, smooth=True,width=self.epesseure,dash=(10,1))
            self.points_courbe = [self.start_x, self.start_y]

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
        elif self.outil_actuel == "ligne_discontinue":
            self.points_courbe.extend([cur_x, cur_y])
            self.canvas.coords(self.forme_actuelle, *self.points_courbe)

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

    def modifier_epaisseur(self, evenement):
            new_width = int(self.width_scale.get())
            self.width_scale_label.config(text="Epaisseur : "+str(new_width))
            self.epesseure = new_width

    def ouvrir_choix_couleur(self):
        couleur_choisie = colorchooser.askcolor()[1]  # Obtenir le code couleur hexadécimal
        if couleur_choisie:
            changerCouleurStylo(self,couleur_choisie)

    def changer_couleur_arrier_plan(self):
        couleur = colorchooser.askcolor()[1]  # Obtenir le code couleur hexadécimal
        if couleur:
            self.canvas_arriere_plan = couleur
            self.canvas.configure(bg=self.canvas_arriere_plan) 

    def ajouter_texte(self):
        fenetre = tk.Toplevel()
        fenetre.title("Fenêtre Personnalisée")
        fenetre.geometry("450x350") 
        fenetre.configure(bg="#eee")
        fenetre.minsize(450, 350)
        fenetre.iconbitmap("icone/icon.ico")
        label_texte = tk.Label(fenetre, text="Texte :",font=("Arial",25,"bold"))
        label_texte.grid(row=0, column=0, padx=5, pady=5)
        icon_rgb = self.redimensionner_icone("icone/rgb.png")

        entry_texte = tk.Entry(fenetre,width=20,font=("Arial",20,"bold"))
        entry_texte.grid(row=0, column=1, padx=5, pady=5, columnspan=2)

        bold_var = tk.BooleanVar()
        italic_var = tk.BooleanVar()
        underline_var = tk.BooleanVar()

        checkbutton_bold = tk.Checkbutton(fenetre, text="Gras", variable=bold_var, height=2, width=4, font=("Arial", 15,"bold"))
        checkbutton_italic = tk.Checkbutton(fenetre, text="Italique", variable=italic_var , height=2, width=6, font=("Arial", 15,"bold"))
        checkbutton_underline = tk.Checkbutton(fenetre, text="Souligné", variable=underline_var , height=2, width=6, font=("Arial", 15,"bold"))

        checkbutton_bold.grid(row=1, column=0, padx=20, pady=15)
        checkbutton_italic.grid(row=1, column=1, padx=20, pady=15)
        checkbutton_underline.grid(row=1, column=2, padx=20, pady=15)
        
        button_color = tk.Button(fenetre,relief=tk.RAISED, image=icon_rgb, command=self.choisir_couleur)
        button_color.image = icon_rgb
        button_color.grid(row=2, column=1, padx=5, pady=5)

        taille_controller = tk.Scale(fenetre, from_=12,to=100,bg="#738BD7",fg="white", orient=tk.HORIZONTAL,command=lambda val: self.choisir_taille(int(val)))
        taille_controller.set(self.text_size)  # Définir la taille par défaut
        taille_controller.grid(row=3, column=1, padx=5, pady=5)

        button_ok = tk.Button(fenetre,text="Accepter", fg="white",width=10 ,font=("Arial",15,"bold"), bg="#738BD7" ,command=lambda: self.ok_pressed(entry_texte, bold_var.get(), italic_var.get(), underline_var.get()), height=2)
        button_ok.grid(row=4, column=1, pady=10)
        
    def choisir_couleur(self):
        couleur = colorchooser.askcolor()[1]
        if couleur:
            # Mise à jour de la couleur du texte
            self.text_color = couleur
        self.fenetre.wait_window(self.fenetre)

    def choisir_taille(self, taille):
        self.text_size = taille

    def ok_pressed(self, entry_texte, bold, italic, underline):
        texte_saisi = entry_texte.get()
        if texte_saisi:
            self.font_styles = []  # Réinitialiser la liste des styles de police
            if bold:
                self.font_styles.append("bold")
            if italic:
                self.font_styles.append("italic")
            if underline:
                self.font_styles.append("underline")

            # Utilisez une liste pour spécifier les styles de police
            font_tuple = ("Arial", self.text_size, " ".join(self.font_styles))

            # Utilisez self.font_styles pour définir le style de police
            self.canvas.create_text(
                self.start_x, self.start_y,
                text=texte_saisi, fill=self.text_color,
                font=font_tuple
            )
            
            self.texte_a_afficher = texte_saisi
            entry_texte.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ApplicationDessin(root)
    root.mainloop()