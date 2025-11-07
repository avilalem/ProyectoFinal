from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication
from database import SQLiteDatabase
from message_dialog import MessageDialog
from navigation import NavigationManager


class PaginaAdmin(QMainWindow):
    def __init__(self, controlador):
        super().__init__()
        uic.loadUi("pagina_principal_admin.ui", self)
        self.db = SQLiteDatabase()
        self.controlador = controlador
        self.nav = NavigationManager.get_instance()

        self.botonCerrarS.clicked.connect(self.cerrar_sesion)
        self.botonAgregar.clicked.connect(self.agregar_receta)
        self.botonVer.clicked.connect(self.ver_receta)
        self.botonBuscar.clicked.connect(self.buscar_receta)
        self.botonInfo.clicked.connect(lambda: self.open_info("admin"))
        self.botonSalir.clicked.connect(self.confirmar_salida)

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
            "Panel de Administración\n\n"
            "Desde aquí puedes:\n"
            "• Agregar nuevas recetas\n"
            "• Ver todas las recetas\n"
            "• Buscar recetas específicas\n"
            "• Cerrar sesión de administrador"
        )
        dlg = MessageDialog(self, title="Ayuda - Panel Admin", text=msg, editable=False)
        dlg.exec()

    def agregar_receta(self):
        from pagina_agregar_receta import PaginaAgregarReceta
        self.nav.mostrar("agregar_receta", PaginaAgregarReceta, self.controlador)  # ✅ Sin espacio

    def ver_receta(self):
        from pagina_lista import PaginaLista
        self.nav.mostrar("lista", PaginaLista, self.controlador)

    def buscar_receta(self):
        from pagina_busqueda import PaginaBusqueda
        self.nav.mostrar("busqueda", PaginaBusqueda, self.controlador)

    def cerrar_sesion(self):
        if self.nav.es_administrador:
            self.nav.logout_administrador()
            dlg = MessageDialog(self,
                                title="Sesión Cerrada",
                                text="Sesión de administrador cerrada correctamente",
                                editable=False)
            dlg.exec()

            from pagina_principal import PaginaPrincipal
            self.nav.mostrar("principal", PaginaPrincipal, self.controlador)

