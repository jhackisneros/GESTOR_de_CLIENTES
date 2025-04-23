from tkinter import *
from .helpers import limpiar_pantalla

class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title('Gestor de Clientes')
        self.geometry("600x400")
        self.build()

    def build(self):
        label = Label(self, text="¡Hola desde la GUI!", font=("Arial", 16))
        label.pack(pady=20)

        boton = Button(self, text="Cerrar", command=self.destroy)
        boton.pack()
