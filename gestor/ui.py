from tkinter import *
from tkinter import ttk
from .database import Clientes  #  Esto es lo que faltaba
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
        # Tabla
        self.tree = ttk.Treeview(self, columns=("DNI", "Nombre", "Apellido"), show="headings")
        self.tree.heading("DNI", text="DNI")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Apellido", text="Apellido")
        self.tree.pack(expand=True, fill=BOTH, padx=10, pady=10)

        # Cargar datos
        self.cargar_datos()

        # Botón cerrar
        boton = Button(self, text="Cerrar", command=self.destroy)
        boton.pack(pady=10)

    def cargar_datos(self):
        for cliente in Clientes.lista:
            self.tree.insert("", END, values=(cliente.dni, cliente.nombre, cliente.apellido))
