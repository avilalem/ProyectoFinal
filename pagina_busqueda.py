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

        self.resultadosLista.itemDoubleClicked.connect(self.abrir_editar_receta)  # CAMBIADO A DoubleClicked
        self.botonSalir.clicked.connect(self.confirmar_salida)
        self.recetas = Receta.obtener_todas(self.db)
        self.actualizar_lista(self.recetas)
        self.botonTodas.clicked.connect(self.abrir_pagina_lista)
        self.botonInfo.clicked.connect(lambda: self.open_info("pagina_busqueda"))
        self.botonCerrarS.clicked.connect(self.cerrar_sesion)
        self.actualizar_botones_administrador()
        self.botonRegresar.clicked.connect(self.regresar_inteligente)

    def regresar_inteligente(self):
        if self.nav.es_administrador:
            from pagina_principal_admin import PaginaAdmin
            self.nav.mostrar("admin_panel", PaginaAdmin, self.controlador)
        else:
            from pagina_principal import PaginaPrincipal
            self.nav.mostrar("principal", PaginaPrincipal, self.controlador)

    def confirmar_salida(self):
        from confirm_dialog import ConfirmDialog
        dlg = ConfirmDialog(
            self,
            title="Salir de la aplicación",
            text="¿Estás seguro de que deseas salir?",
            on_confirm=lambda: QApplication.quit()
        )
        dlg.exec()





    def actualizar_lista(self, lista_recetas):
        self.resultadosLista.clear()

        for receta in lista_recetas:
            item = QListWidgetItem(receta.nombre)
            item.setData(Qt.ItemDataRole.UserRole, receta.id)  # GUARDAR SOLO EL ID
            self.resultadosLista.addItem(item)

    def mostrar_receta(self, item):
        receta_id = item.data(Qt.ItemDataRole.UserRole)
        receta = Receta.obtener_por_id(self.db, receta_id)
        if receta:
            texto = f"Nombre: {receta.nombre}\n"
            texto += f"Categoría: {receta.categoria}\n\n"
            texto += f"Ingredientes:\n{receta.mostrar_ingredientes_ajustados(1.0)}\n\n"
            texto += f"Instrucciones:\n{receta.instrucciones}"
            self.textEdit.setPlainText(texto)

    def abrir_editar_receta(self, item):
        if not self.nav.es_administrador:
            from message_dialog import MessageDialog
            dlg = MessageDialog(
                self,
                title="Acceso denegado",
                text="Solo los administradores pueden editar recetas",
                editable=False
            )
            dlg.exec()
            return

        receta_id = item.data(Qt.ItemDataRole.UserRole)
        from pagina_editar_receta import PaginaEditarReceta
        ventana_editar = PaginaEditarReceta(self.controlador, receta_id)
        self.controlador.mostrar(ventana_editar)

    def abrir_pagina_lista(self):
        print("Siguiente Pagina")
        from pagina_lista import PaginaLista
        self.nav.mostrar("lista", PaginaLista, self.controlador)

    def open_info(self, page_key):
        from message_dialog import MessageDialog
        msg = (
            "Esta es la ventana de Búsqueda.\n\n"
            "Funcionalidades:\n"
            "Escribe para filtrar recetas por nombre\n"
            "Haz DOBLE CLIC en una receta para editarla (solo administradores)\n"
            "Haz CLIC en una receta para ver los detalles\n"
            "Botón 'Ver Todas' para ver lista completa\n\n"
            "Modo Administrador: Puedes editar recetas existentes"
        )
        dlg = MessageDialog(self, title="Ayuda - Búsqueda", text=msg, editable=False)
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