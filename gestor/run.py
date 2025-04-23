import sys
from . import menu
from . import ui

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "-t":
        menu.iniciar()
    else:
        app = ui.MainWindow()
        app.mainloop()
