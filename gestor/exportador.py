from openpyxl import Workbook
from .database import Clientes

def exportar_a_excel(nombre_archivo="clientes.xlsx"):
    wb = Workbook()
    ws = wb.active
    ws.title = "Clientes"

    # Cabecera
    ws.append(["DNI", "Nombre", "Apellido"])

    # Datos
    for cliente in Clientes.lista:
        ws.append([cliente.dni, cliente.nombre, cliente.apellido])

    wb.save(nombre_archivo)
