from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QListWidgetItem, QApplication
from PyQt6.QtCore import Qt
from database import SQLiteDatabase
from models import Receta
from navigation import NavigationManager


class PaginaBusqueda(QMainWindow):
    def __init__(self, controlador):
        super().__init__()
        uic.loadUi("pagina_busqueda.ui", self)
        print("PaginaBusqueda: UI cargada")
        self.db = SQLiteDatabase()
        self.controlador = controlador
        self.nav = NavigationManager.get_instance()
        self.cajaBusqueda.textChanged.connect(self.buscar_recetas)
        self.resultadosLista.itemClicked.connect(self.mostrar_receta)
        self.botonSalir.clicked.connect(self.confirmar_salida)
        self.recetas = Receta.obtener_todas(self.db)
        self.actualizar_lista(self.recetas)
        self.botonTodas.clicked.connect(self.abrir_pagina_lista)
        self.botonInfo.clicked.connect(lambda: self.open_info("pagina_busqueda"))
        self.botonRegresar.clicked.connect(self.regresar_a_principal)
        self.botonCerrarS.clicked.connect(self.cerrar_sesion)
        self.actualizar_botones_administrador()

    def regresar_a_principal(self):
        from pagina_principal import PaginaPrincipal
        self.linePassword.clear()
        ventana_principal = PaginaPrincipal(self.controlador)
        self.nav.mostrar(PaginaPrincipal)

    def confirmar_salida(self):
        from confirm_dialog import ConfirmDialog
        dlg = ConfirmDialog(
            self,
            title="Salir de la aplicación",
            text="¿Estás seguro de que deseas salir?",
            on_confirm=lambda: QApplication.quit()
        )
        dlg.exec()

    def regresar_inteligente(self):
        if self.nav.es_administrador:
            from pagina_principal_contraseña import PaginaPassword
            self.nav.mostrar("admin", PaginaPassword, self.controlador)
        else:
            from pagina_principal import PaginaPrincipal
            self.nav.mostrar("principal", PaginaPrincipal, self.controlador)

    def buscar_recetas(self):
        texto = self.cajaBusqueda.text().strip().lower()

        if texto == "":
            coincidencias = self.recetas
        else:
            coincidencias = [
                receta for receta in self.recetas
                if texto in receta.nombre.lower()
            ]

        self.actualizar_lista(coincidencias)

    def actualizar_lista(self, lista_recetas):
        self.resultadosLista.clear()

        for receta in lista_recetas:
            item = QListWidgetItem(receta.nombre)
            item.setData(Qt.ItemDataRole.UserRole, receta)
            self.resultadosLista.addItem(item)

    def mostrar_receta(self, item):
        receta = item.data(Qt.ItemDataRole.UserRole)
        self.textEdit.setPlainText(receta.procedimiento)

    def abrir_pagina_lista(self):
        print("Siguiente Pagina")
        from pagina_lista import PaginaLista
        self.nav.mostrar("lista", PaginaLista, self.controlador)

    def open_info(self, page_key):
        from message_dialog import MessageDialog
        msg = (
            "Esta es la ventana de Busqueda.\n\n"
            "Desde aquí puedes ingresar una palabra clave del titulo de la Receta. "
            "Haz clic en la receta para verla"
        )
        dlg = MessageDialog(self, title="Ayuda - Página Principal", text=msg, editable=False)
        dlg.exec()

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

    def actualizar_botones_administrador(self):
        from navigation import NavigationManager
        nav = NavigationManager.get_instance()
        es_admin = nav.es_administrador
        botones_admin = ['botonCerrarS']
        for boton_name in botones_admin:
            if hasattr(self, boton_name):
                getattr(self, boton_name).setVisible(es_admin)

        print(f"Modo administrador: {es_admin}")
