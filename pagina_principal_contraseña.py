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
        self.botonRegresar.clicked.connect(self.regresar_a_principal)
        self.linePassword.clear()

    def regresar_a_principal(self):
        from pagina_principal import PaginaPrincipal
        self.nav.mostrar("principal", PaginaPrincipal, self.controlador)

    def verificar_contrasena(self):
        if self.linePassword.text() == "1234":
            from pagina_principal_admin import PaginaAdmin
            self.nav.login_administrador()
            self.nav.mostrar("admin_panel", PaginaAdmin, self.controlador)
        else:
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
