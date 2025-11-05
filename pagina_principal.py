from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication
from message_dialog import MessageDialog
from database import SQLiteDatabase
from navigation import NavigationManager

class PaginaPrincipal(QMainWindow):
    def __init__(self, controlador):
        super().__init__()

        # Ajusta la ruta si tus .ui están dentro de carpeta 'ui/'
        # prueba primero con "ui/pagina_principal.ui", si tu .ui está en la raíz usa "pagina_principal.ui"
        uic.loadUi("pagina_principal.ui", self)

        self.db = SQLiteDatabase()
        self.controlador = controlador
        self.nav = NavigationManager.get_instance()
        # Conectar señales
        self.botonSalir.clicked.connect(self.confirmar_salida)
        self.botonStart.clicked.connect(self.abrir_usuario)
        self.botonAdmin.clicked.connect(self.abrir_admin)
        self.botonInfo.clicked.connect(lambda: self.open_info("pagina_principal"))

    def abrir_usuario(self):
        print("PaginaPrincipal: abrir_usuario llamado")
        from pagina_busqueda import PaginaBusqueda
        # clave 'busqueda' y pasar controlador si lo requiere la página
        self.nav.mostrar("busqueda", PaginaBusqueda, self.controlador)

    def abrir_admin(self):
        print("PaginaPrincipal: abrir_admin llamado")
        from pagina_principal_contraseña import PaginaPassword
        self.nav.mostrar("admin", PaginaPassword, self.controlador)

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
            "Esta es la ventana principal.\n\n"
            "Desde aquí puedes acceder al modo usuario o administrador. "
            "Haz clic en 'Ingresar' para comenzar."
        )
        dlg = MessageDialog(self, title="Ayuda - Página Principal", text=msg, editable=False)
        dlg.exec()
