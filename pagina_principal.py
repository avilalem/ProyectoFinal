from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication
from pagina_principal_contraseña import PaginaPassword
from pagina_busqueda import PaginaBusqueda
from message_dialog import MessageDialog


from database import SQLiteDatabase


class PaginaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("pagina_principal.ui", self)
        self.db = SQLiteDatabase()

        self.botonSalir.clicked.connect(self.confirmar_salida)
        self.botonStart.clicked.connect(self.abrir_usuario)
        self.botonAdmin.clicked.connect(self.abrir_admin)
        self.botonInfo.clicked.connect(lambda: self.open_info("pagina_principal"))


    def confirmar_salida(self):
        from confirm_dialog import ConfirmDialog
        dlg = ConfirmDialog(
            self,
            title="Salir de la aplicación",
            text="¿Estás seguro de que deseas salir?",
            on_confirm=lambda: QApplication.quit()
        )
        dlg.exec()

    def abrir_usuario(self):
        from pagina_busqueda import PaginaBusqueda
        self.ventana_busqueda = PaginaBusqueda()
        self.ventana_busqueda.show()
        self.close()

    def abrir_admin(self):
        from pagina_principal_contraseña import PaginaPassword
        self.ventana_admin = PaginaPassword()
        self.ventana_admin.show()
        self.close()

    def open_info(self, page_key):
        msg = (
            "Esta es la ventana principal.\n\n"
            "Desde aquí puedes acceder al modo usuario o administrador. "
            "Haz clic en 'Ingresar' para comenzar."
        )
        dlg = MessageDialog(self, title="Ayuda - Página Principal", text=msg, editable=False)
        dlg.exec()
