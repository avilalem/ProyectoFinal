import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QInputDialog
from PyQt6 import uic
from database import SQLiteDatabase
from models import Receta, Ingrediente

class PaginaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("pagina_principal.ui", self)
        self.db=SQLiteDatabase()
        self.botonStart.clicked.connect(self.abrir_usuario)
        self.botonAdmin.clicked.connect(self.abrir_admin)

    def abrir_usuario(self):
        pass
    def abrir_admin(self):


if __name__=="__main__":
    app=QApplication(sys.argv)
    window=PaginaPrincipal()
    window.show()
    sys.exit(app.exec())