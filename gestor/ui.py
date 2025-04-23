from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from .database import Clientes
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

        # Botones
        frame_botones = Frame(self)
        frame_botones.pack(pady=10)

        btn_borrar = Button(frame_botones, text="Borrar Cliente", command=self.borrar_cliente)
        btn_borrar.pack(side=LEFT, padx=5)

        btn_cerrar = Button(frame_botones, text="Cerrar", command=self.destroy)
        btn_cerrar.pack(side=LEFT, padx=5)

        # Cargar datos
        self.cargar_datos()

    def cargar_datos(self):
        for cliente in Clientes.lista:
            self.tree.insert("", END, values=(cliente.dni, cliente.nombre, cliente.apellido))

    def borrar_cliente(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un cliente para borrar")
            return

        valores = self.tree.item(seleccionado[0])["values"]
        dni = valores[0]

        # Confirmación
        confirmacion = messagebox.askyesno("Confirmar", f"¿Seguro que deseas borrar al cliente {dni}?")
        if not confirmacion:
            return

        # Eliminar de base de datos y CSV
        Clientes.borrar(dni)

        # Eliminar de la tabla
        self.tree.delete(seleccionado[0])
