from tkinter import *
from .helpers import limpiar_pantalla

class CenterMixin:
    def centrar(self):
        self.update_idletasks()
        ancho = self.winfo_width()
        alto = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

class MainWindow(Tk, CenterMixin):
    def __init__(self):
        super().__init__()
        self.title('Gestor de Clientes')
        self.geometry("600x400")
        self.centrar()
        self.build()

    def build(self):
        label = Label(self, text="¡Hola desde la GUI!", font=("Arial", 16))
        label.pack(pady=20)

        boton = Button(self, text="Cerrar", command=self.destroy)
        boton.pack()
