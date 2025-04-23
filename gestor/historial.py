def registrar(accion: str, cliente):
    with open("historial.log", "a", encoding="utf-8") as f:
        f.write(f"{accion.upper()}: {cliente.dni} - {cliente.nombre} {cliente.apellido}\n")
