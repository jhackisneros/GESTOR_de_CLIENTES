from datetime import datetime

def registrar(accion: str, cliente):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("historial.log", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {accion.upper()}: {cliente.dni} - {cliente.nombre} {cliente.apellido}\n")
