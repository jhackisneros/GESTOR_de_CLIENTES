from openpyxl import Workbook
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from .database import Clientes

def exportar_a_excel(nombre_archivo="clientes.xlsx"):
    wb = Workbook()
    ws = wb.active
    ws.title = "Clientes"
    ws.append(["DNI", "Nombre", "Apellido"])
    for cliente in Clientes.lista:
        ws.append([cliente.dni, cliente.nombre, cliente.apellido])
    wb.save(nombre_archivo)

def exportar_historial_pdf(nombre_archivo="historial.pdf"):
    c = canvas.Canvas(nombre_archivo, pagesize=LETTER)
    c.setFont("Helvetica", 10)
    _, alto = LETTER  # solo usamos 'alto'

    try:
        with open("historial.log", "r", encoding="utf-8") as f:
            lineas = f.readlines()
    except FileNotFoundError:
        lineas = ["No hay historial registrado."]

    y = alto - 40
    c.drawString(50, y, "Historial de acciones:")
    y -= 20

    for linea in lineas:
        if y < 40:
            c.showPage()
            c.setFont("Helvetica", 10)
            y = alto - 40
        c.drawString(50, y, linea.strip())
        y -= 15

    c.save()
