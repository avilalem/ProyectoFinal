from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication, QLineEdit
from message_dialog import MessageDialog
from database import SQLiteDatabase
from navigation import NavigationManager


class PaginaPassword(QMainWindow):
    def __init__(self, controlador):
        super().__init__()
        uic.loadUi("pagina_principal_contraseña.ui", self)

        self.db = SQLiteDatabase()
        self.controlador = controlador
        self.nav = NavigationManager.get_instance()
        self.linePassword.setEchoMode(QLineEdit.EchoMode.Password)
        self.botonIngresar.clicked.connect(self.verificar_contrasena)
        self.botonSalir.clicked.connect(self.confirmar_salida)
        self.botonInfo.clicked.connect(lambda: self.open_info("pagina_principal_contraseña"))
        self.botonRegresar.clicked.connect(self.nav.volver_atras)

    def verificar_contrasena(self):
        contrasena_ingresada = self.linePassword.text()
        if contrasena_ingresada == "1234":
            print("PaginaPassword: contraseña correcta")
            from pagina_busqueda import PaginaBusqueda
            self.nav.login_administrador()
            self.nav.mostrar("busqueda", PaginaBusqueda, self.controlador)
        else:
            print("PaginaPassword: contraseña incorrecta")
            dlg = MessageDialog(self, title="Error", text="Contraseña incorrecta.", editable=False)
            dlg.exec()

    def confirmar_salida(self):
        from confirm_dialog import ConfirmDialog
        dlg = ConfirmDialog(
            self,
            title="Salir de la aplicación",
            text="¿Estás seguro de que deseas salir?",
            on_confirm=lambda: QApplication.quit()
        )
        dlg.exec()

    def open_info(self, page_key):
        msg = (
            "Esta es la ventana de Ingreso.\n\n"
            "Desde aquí puedes ingresar la contraseña para acceder a las funciones del administrador. "
            "Ingresa la contraseña y haz clic en 'Ingresar' para comenzar."
        )
        dlg = MessageDialog(self, title="Ayuda - Ingreso Administrador", text=msg, editable=False)
        dlg.exec()
