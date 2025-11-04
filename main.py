import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
from message_dialog import MessageDialog   # importa la clase que creamos
from database import SQLiteDatabase
from models import Receta, Ingrediente

class AppController:
    def __init__(self):
        self.ventana_actual = None

    def mostrar(self, ventana):
        if self.ventana_actual:
            self.ventana_actual.close()
        self.ventana_actual = ventana
        ventana.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PaginaPrincipal()
    window.show()
    sys.exit(app.exec())
