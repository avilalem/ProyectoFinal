from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QListWidgetItem, QApplication
from PyQt6.QtCore import Qt
from database import SQLiteDatabase
from message_dialog import MessageDialog
from navigation import NavigationManager


class PaginaAdmin(QMainWindow):
    def __init__(self, controlador):
        super().__init__()
        uic.loadUi("pagina_lista.ui", self)
        self.db = SQLiteDatabase()
        self.controlador = controlador
        self.botonCerrarS.clicked.connect(self.cerrar_sesion)
        self.botonAgregar.clicked.connect(self.agregar_receta)
        self.botonVer.clicked.connect(self.ver_recetas)
        self.botonBuscar.clicked.connect(self.buscar_receta)
        self.botonInfo.clicked.connect(lambda: self.open_info("pagina_lista"))

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

    def agregar_receta(self):
        print("PaginaPrincipal: agregar_receta llamado")
        from pagina_agregar_receta import PaginaAgregarReceta
        self.nav.mostrar("agregar receta", PaginaAgregarReceta, self.controlador)

    def ver_receta(self):
        print("PaginaReceta: ver_receta llamado")
        from pagina_receta import PaginaReceta
        self.nav.mostrar("recetas", PaginaReceta, self.controlador)

    def buscar_receta(self):
        print("PaginaBuscar: buscar_receta llamado")
        from pagina_busqueda import PaginaBusqueda
        self.nav.mostrar("busqueda", PaginaBusqueda, self.controlador)

    def cerrar_sesion(self):
        from navigation import NavigationManager
        from message_dialog import MessageDialog

        nav = NavigationManager.get_instance()
        if nav.es_administrador:
            nav.logout_administrador()
            dlg = MessageDialog(self,
                                title="Sesión Cerrada",
                                text="Sesión de administrador cerrada correctamente",
                                editable=False)
            dlg.exec()
        else:
            dlg = MessageDialog(self,
                                title="Información",
                                text="No hay sesión de administrador activa",
                                editable=False)
            dlg.exec()