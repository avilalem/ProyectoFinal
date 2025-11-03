#import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
from message_dialog import MessageDialog
from database import SQLiteDatabase
from models import Receta, Ingrediente


class PaginaPassword(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/pagina_principal_contraseña.ui", self)
        self.db = SQLiteDatabase()

        self.linePassword.setEchoMode(QLineEdit.EchoMode.Password)
        self.botonIngresar.clicked.connect(self.verificar_contrasena)
        self.botonSalir.clicked.connect(self.confirmar_salida)
        self.botonInfo.clicked.connect(lambda: self.open_info("pagina_principal_contraseña"))
        self.botonRegresar.clicked.connect(self.regresar_a_principal)

    def confirmar_salida(self):
        dlg = ConfirmDialog(
            self,
            title="Salir de la aplicación",
            text="¿Estás seguro de que deseas salir?",
            on_confirm=lambda: QApplication.quit()
        )
        dlg.exec()

    def regresar_a_principal(self):
        self.ventana_principal = PaginaPrincipal()
        self.ventana_principal.show()
        self.close()

    def verificar_contrasena(self):
        contrasena_ingresada = self.textContrasena.text()

        # Ejemplo: validación simple
        if contrasena_ingresada == "1234":
            print("Contraseña correcta. Abriendo panel de administración...")
            # Aquí puedes abrir otra ventana, por ejemplo:
            # self.abrir_panel_admin()
        else:
            print("Contraseña incorrecta.")

    def open_info(self, page_key):
        msg = (
            "Esta es la ventana de Ingreso.\n\n"
            "Desde aquí puedes ingresar la contraseña para acceder a las funciones del administrador. "
            "Ingresa la contraseña y haz clic en 'Ingresar' para comenzar."
            "Si no tienes una contraseña o la tuya no sirve, envia un correo a am.amendez@udeo.edu.gt"
        )
        dlg = MessageDialog(self, title="Ayuda - Ingreso Administrador", text=msg, editable=False)
        dlg.exec()
