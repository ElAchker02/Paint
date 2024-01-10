import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Application de dessin")

        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.setup_sidebar()

        self.current_tool = None
        self.current_shape = None
        self.start_x = None
        self.start_y = None

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        
    def resize_icon(self, icon_path, width=20, height=20):
        original_icon = Image.open(icon_path)
        resized_icon = original_icon.resize((width, height), resample=Image.LANCZOS )
        return ImageTk.PhotoImage(resized_icon)
    
    def setup_sidebar(self):
        sidebar = ttk.Frame(self.root, width=200, relief="raised")
        sidebar.pack(side=tk.LEFT, fill=tk.BOTH)

        shape_tools = tk.Frame(sidebar, borderwidth=2, relief="solid", bg="red")
        shape_tools.pack(side=tk.TOP, fill=tk.BOTH,pady=10,padx=40)

        # Chargez les icônes pour les boutons
        circle_icon = self.resize_icon("icone/circle.png")
        rectangle_icon = self.resize_icon("icone/rectangle.png")
        triangle_icon = self.resize_icon("icone/rectangle.png")
        bent_line_icon = self.resize_icon("icone/rectangle.png")
        curved_line_icon = self.resize_icon("icone/rectangle.png")
        rounded_rectangle_icon = self.resize_icon("icone/rectangle.png")
        parallelogram_icon = self.resize_icon("icone/rectangle.png")

        # Ajoutez les boutons avec les icônes dans shape_tools
        circle_button = ttk.Button(shape_tools, image=circle_icon, command=lambda: self.set_tool("circle"))
        circle_button.image = circle_icon
        circle_button.grid(row=0, column=0, pady=5,padx=15)

        rectangle_button = ttk.Button(shape_tools, image=rectangle_icon, command=lambda: self.set_tool("rectangle"))
        rectangle_button.image = rectangle_icon
        rectangle_button.grid(row=0, column=2, pady=5,padx=15)

        triangle_button = ttk.Button(shape_tools, image=triangle_icon, command=lambda: self.set_tool("triangle"))
        triangle_button.image = triangle_icon
        triangle_button.grid(row=0, column=4, pady=5,padx=15)

        bent_line_button = ttk.Button(shape_tools, image=bent_line_icon, command=lambda: self.set_tool("bent_line"))
        bent_line_button.image = bent_line_icon
        bent_line_button.grid(row=1, column=0, pady=5,padx=15)

        curved_line_button = ttk.Button(shape_tools, image=curved_line_icon, command=lambda: self.set_tool("curved_line"))
        curved_line_button.image = curved_line_icon
        curved_line_button.grid(row=1, column=2, pady=5,padx=15)

        rounded_rectangle_button = ttk.Button(shape_tools, image=rounded_rectangle_icon, command=lambda: self.set_tool("rounded_rectangle"))
        rounded_rectangle_button.image = rounded_rectangle_icon
        rounded_rectangle_button.grid(row=1, column=4, pady=5,padx=15)

        parallelogram_button = ttk.Button(shape_tools, image=parallelogram_icon, command=lambda: self.set_tool("parallelogram"))
        parallelogram_button.image = parallelogram_icon
        parallelogram_button.grid(row=2, column=0, pady=5,padx=15)
        

    def set_tool(self, tool):
        self.current_tool = tool

    def on_button_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)

        if self.current_tool == "circle":
            self.current_shape = self.canvas.create_oval(self.start_x, self.start_y, self.start_x, self.start_y, outline="black")
        elif self.current_tool == "rectangle":
            self.current_shape = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="black")
        elif self.current_tool == "triangle":
            self.current_shape = self.canvas.create_polygon(self.start_x, self.start_y, self.start_x, self.start_y, outline="black", fill='')
        elif self.current_tool == "bent_line":
        # Créez la première ligne de la ligne pliée
            self.current_shape = self.canvas.create_line(self.start_x, self.start_y, self.start_x, self.start_y, fill="black", smooth=True)
        elif self.current_tool == "curved_line":
        # Créez la première ligne de la ligne courbée
            self.current_shape = self.canvas.create_line(self.start_x, self.start_y, self.start_x, self.start_y, fill="black", smooth=True)
            self.curve_points = [self.start_x, self.start_y]  # Liste pour stocker les points de contrôle pour la courbe
        elif self.current_tool == "rounded_rectangle":
        # Commencez par dessiner un rectangle arrondi (non rempli)
             self.current_shape = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="black")
        
   
    def on_mouse_drag(self, event):
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)

        if self.current_tool in ["circle", "rectangle"]:
            self.canvas.coords(self.current_shape, self.start_x, self.start_y, cur_x, cur_y)
        elif self.current_tool == "triangle":
        # Mettez à jour les coordonnées du triangle en temps réel
             self.canvas.coords(self.current_shape, self.start_x, self.start_y, cur_x, cur_y, 2 * self.start_x - cur_x, cur_y)
        elif self.current_tool == "bent_line":
        # Mettez à jour la position de la deuxième extrémité de la ligne pliée
            self.canvas.coords(self.current_shape, self.start_x, self.start_y, cur_x, cur_y)
        elif self.current_tool == "curved_line":
        # Ajoutez des points de contrôle à la liste pour la ligne courbée
            self.curve_points.extend([cur_x, cur_y])
            # Mettez à jour la position de la deuxième extrémité de la ligne courbée
            self.canvas.coords(self.current_shape, *self.curve_points)
        elif self.current_tool == "rounded_rectangle":
        # Mettez à jour la position de la deuxième extrémité pour le rectangle arrondi
             self.canvas.coords(self.current_shape, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
