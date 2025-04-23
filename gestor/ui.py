from tkinter import *
from tkinter import ttk, messagebox
from .database import Clientes
from .helpers import limpiar_pantalla, dni_valido

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

        Button(frame_botones, text="Añadir Cliente", command=self.abrir_ventana_nuevo).pack(side=LEFT, padx=5)
        Button(frame_botones, text="Borrar Cliente", command=self.borrar_cliente).pack(side=LEFT, padx=5)
        Button(frame_botones, text="Cerrar", command=self.destroy).pack(side=LEFT, padx=5)

        self.cargar_datos()

    def cargar_datos(self):
        for cliente in self.tree.get_children():
            self.tree.delete(cliente)
        for cliente in Clientes.lista:
            self.tree.insert("", END, values=(cliente.dni, cliente.nombre, cliente.apellido))

    def borrar_cliente(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un cliente para borrar")
            return
        valores = self.tree.item(seleccionado[0])["values"]
        dni = valores[0]
        confirmacion = messagebox.askyesno("Confirmar", f"¿Seguro que deseas borrar al cliente {dni}?")
        if confirmacion:
            Clientes.borrar(dni)
            self.tree.delete(seleccionado[0])

    def abrir_ventana_nuevo(self):
        AddClienteWindow(self)

class AddClienteWindow(Toplevel, CenterMixin):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Nuevo Cliente")
        self.geometry("300x200")
        self.centrar()
        self.parent = parent
        self.build()

    def build(self):
        Label(self, text="DNI (ej: 12A)").pack(pady=(10, 0))
        self.dni_entry = Entry(self)
        self.dni_entry.pack()

        Label(self, text="Nombre").pack(pady=(10, 0))
        self.nombre_entry = Entry(self)
        self.nombre_entry.pack()

        Label(self, text="Apellido").pack(pady=(10, 0))
        self.apellido_entry = Entry(self)
        self.apellido_entry.pack()

        Button(self, text="Añadir", command=self.guardar_cliente).pack(pady=15)

    def guardar_cliente(self):
        dni = self.dni_entry.get().strip().upper()
        nombre = self.nombre_entry.get().strip().capitalize()
        apellido = self.apellido_entry.get().strip().capitalize()

        if not dni or not nombre or not apellido:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if not dni_valido(dni, Clientes.lista):
            return

        Clientes.crear(dni, nombre, apellido)
        self.parent.cargar_datos()
        self.destroy()
