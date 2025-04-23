from tkinter import *
from tkinter import ttk, messagebox
import os
from .database import Clientes
from .helpers import dni_valido
from . import historial
from . import exportador

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
        self.geometry("800x500")
        self.centrar()
        self.build()

    def build(self):
        # Buscador
        search_frame = Frame(self)
        search_frame.pack(pady=(10, 0))
        Label(search_frame, text="Buscar por nombre o apellido:").pack(side=LEFT)
        self.search_var = StringVar()
        self.search_var.trace("w", self.filtrar_clientes)
        Entry(search_frame, textvariable=self.search_var, width=30).pack(side=LEFT, padx=5)

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
        Button(frame_botones, text="Modificar Cliente", command=self.modificar_cliente).pack(side=LEFT, padx=5)
        Button(frame_botones, text="Borrar Cliente", command=self.borrar_cliente).pack(side=LEFT, padx=5)
        Button(frame_botones, text="Ver Historial", command=self.mostrar_historial).pack(side=LEFT, padx=5)
        Button(frame_botones, text="Exportar a Excel", command=self.exportar_excel).pack(side=LEFT, padx=5)
        Button(frame_botones, text="Exportar historial a PDF", command=self.exportar_historial_pdf).pack(side=LEFT, padx=5)
        Button(frame_botones, text="Cerrar", command=self.destroy).pack(side=LEFT, padx=5)

        self.cargar_datos()

    def cargar_datos(self):
        self.tree.delete(*self.tree.get_children())
        for cliente in Clientes.lista:
            self.tree.insert("", END, values=(cliente.dni, cliente.nombre, cliente.apellido))

    def filtrar_clientes(self, *args):
        filtro = self.search_var.get().lower()
        self.tree.delete(*self.tree.get_children())
        for cliente in Clientes.lista:
            if filtro in cliente.nombre.lower() or filtro in cliente.apellido.lower():
                self.tree.insert("", END, values=(cliente.dni, cliente.nombre, cliente.apellido))

    def borrar_cliente(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un cliente para borrar")
            return
        valores = self.tree.item(seleccionado[0])["values"]
        dni = valores[0]
        cliente = Clientes.buscar(dni)
        if cliente:
            confirmacion = messagebox.askyesno("Confirmar", f"¿Seguro que deseas borrar al cliente {dni}?")
            if confirmacion:
                historial.registrar("borrado", cliente)
                Clientes.borrar(dni)
                self.tree.delete(seleccionado[0])

    def abrir_ventana_nuevo(self):
        AddClienteWindow(self)

    def modificar_cliente(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un cliente para modificar")
            return
        valores = self.tree.item(seleccionado[0])["values"]
        cliente = Clientes.buscar(valores[0])
        if cliente:
            EditClienteWindow(self, cliente)

    def mostrar_historial(self):
        top = Toplevel(self)
        top.title("Historial de acciones")
        top.geometry("500x400")
        self.centrar()
        text = Text(top, wrap=WORD)
        text.pack(expand=True, fill=BOTH, padx=10, pady=10)
        try:
            with open("historial.log", "r", encoding="utf-8") as f:
                text.insert("1.0", f.read())
        except FileNotFoundError:
            text.insert("1.0", "No hay historial registrado aún.")

    def exportar_excel(self):
        exportador.exportar_a_excel()
        ruta = os.path.abspath("clientes.xlsx")
        messagebox.showinfo("Exportación", f"Clientes exportados a Excel.\n\nUbicación:\n{ruta}")

    def exportar_historial_pdf(self):
        exportador.exportar_historial_pdf()
        ruta = os.path.abspath("historial.pdf")
        messagebox.showinfo("Exportación", f"Historial exportado correctamente.\n\nUbicación:\n{ruta}")

class AddClienteWindow(Toplevel, CenterMixin):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Nuevo Cliente")
        self.geometry("300x240")
        self.centrar()
        self.parent = parent
        self.build()

    def build(self):
        Label(self, text="DNI (ej: 12A)").pack(pady=(10, 0))
        self.dni_var = StringVar()
        self.dni_entry = Entry(self, textvariable=self.dni_var)
        self.dni_entry.pack()
        self.dni_var.trace("w", self.validar_dni)

        Label(self, text="Nombre").pack(pady=(10, 0))
        self.nombre_var = StringVar()
        self.nombre_entry = Entry(self, textvariable=self.nombre_var)
        self.nombre_entry.pack()
        self.nombre_var.trace("w", self.validar_nombre)

        Label(self, text="Apellido").pack(pady=(10, 0))
        self.apellido_var = StringVar()
        self.apellido_entry = Entry(self, textvariable=self.apellido_var)
        self.apellido_entry.pack()
        self.apellido_var.trace("w", self.validar_apellido)

        Button(self, text="Añadir", command=self.guardar_cliente).pack(pady=15)

    def validar_dni(self, *args):
        dni = self.dni_var.get().strip().upper()
        valido = dni_valido(dni, Clientes.lista)
        self.dni_entry.config(bg="#ccffcc" if valido else "#ffcccc")

    def validar_nombre(self, *args):
        nombre = self.nombre_var.get().strip()
        self.nombre_entry.config(bg="#ccffcc" if 2 <= len(nombre) <= 30 else "#ffcccc")

    def validar_apellido(self, *args):
        apellido = self.apellido_var.get().strip()
        self.apellido_entry.config(bg="#ccffcc" if 2 <= len(apellido) <= 30 else "#ffcccc")

    def guardar_cliente(self):
        dni = self.dni_var.get().strip().upper()
        nombre = self.nombre_var.get().strip().capitalize()
        apellido = self.apellido_var.get().strip().capitalize()

        if not dni or not nombre or not apellido:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if not dni_valido(dni, Clientes.lista):
            return

        cliente = Clientes.crear(dni, nombre, apellido)
        historial.registrar("añadido", cliente)
        self.parent.cargar_datos()
        self.destroy()

class EditClienteWindow(Toplevel, CenterMixin):
    def __init__(self, parent, cliente):
        super().__init__(parent)
        self.title(f"Editar Cliente: {cliente.dni}")
        self.geometry("300x240")
        self.centrar()
        self.parent = parent
        self.cliente = cliente
        self.build()

    def build(self):
        Label(self, text="DNI (no editable)").pack(pady=(10, 0))
        self.dni_entry = Entry(self)
        self.dni_entry.insert(0, self.cliente.dni)
        self.dni_entry.config(state="disabled")
        self.dni_entry.pack()

        Label(self, text="Nombre").pack(pady=(10, 0))
        self.nombre_var = StringVar(value=self.cliente.nombre)
        self.nombre_entry = Entry(self, textvariable=self.nombre_var)
        self.nombre_entry.pack()
        self.nombre_var.trace("w", self.validar_nombre)

        Label(self, text="Apellido").pack(pady=(10, 0))
        self.apellido_var = StringVar(value=self.cliente.apellido)
        self.apellido_entry = Entry(self, textvariable=self.apellido_var)
        self.apellido_entry.pack()
        self.apellido_var.trace("w", self.validar_apellido)

        Button(self, text="Guardar Cambios", command=self.guardar_cambios).pack(pady=15)

    def validar_nombre(self, *args):
        nombre = self.nombre_var.get().strip()
        self.nombre_entry.config(bg="#ccffcc" if 2 <= len(nombre) <= 30 else "#ffcccc")

    def validar_apellido(self, *args):
        apellido = self.apellido_var.get().strip()
        self.apellido_entry.config(bg="#ccffcc" if 2 <= len(apellido) <= 30 else "#ffcccc")

    def guardar_cambios(self):
        nombre = self.nombre_var.get().strip().capitalize()
        apellido = self.apellido_var.get().strip().capitalize()

        if not nombre or not apellido:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        Clientes.modificar(self.cliente.dni, nombre, apellido)
        historial.registrar("modificado", self.cliente)
        self.parent.cargar_datos()
        self.destroy()
