# GESTOR_de_CLIENTES
https://github.com/jhackisneros/GESTOR_de_CLIENTES.git



gestor_clientes/           # Carpeta raíz del proyecto
│
├── gestor/                # Código fuente
│   ├── __init__.py        # (opcional, para tratarlo como paquete)
│   ├── run.py             # Script principal
│   ├── menu.py            # Menú de texto para consola
│   ├── database.py        # Lógica de cliente y CRUD
│   ├── helpers.py         # Funciones auxiliares (limpiar pantalla, leer texto, etc.)
│   ├── config.py          # Ruta del archivo CSV para producción y testing
│   └── ui.py              # Interfaz gráfica con Tkinter
│
├── tests/                 # Pruebas automatizadas con pytest
│   ├── __init__.py        # Marca la carpeta como paquete de pruebas
│   ├── test_database.py   # Tests para el módulo de base de datos
│   └── clientes_test.csv  # CSV usado sólo para las pruebas
│
├── clientes.csv           # CSV principal con los datos reales
├── README.md              # Documentación del proyecto
└── requirements.txt   
