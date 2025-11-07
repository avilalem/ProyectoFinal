from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QListWidgetItem, QApplication
from PyQt6.QtCore import Qt
from database import SQLiteDatabase
from models import Receta, Ingrediente
from navigation import NavigationManager

class PaginaLista(QMainWindow):
    def __init__(self, controlador):
        super().__init__()
        uic.loadUi("pagina_lista.ui", self)

        self.db = SQLiteDatabase()
        self.recetas = Receta.obtener_todas(self.db)
        self.controlador = controlador
        self.botonDulce.toggled.connect(self.filtrar_recetas)
        self.botonSalado.toggled.connect(self.filtrar_recetas)
        self.botonTodo.toggled.connect(self.filtrar_recetas)
        self.mostrar_recetas(self.recetas)
        self.botonSalir.clicked.connect(self.confirmar_salida)
        self.botonInfo.clicked.connect(lambda: self.open_info("pagina_lista"))
        self.botonRegresar.clicked.connect(self.regresar_a_busqueda)
        self.botonCerrarS.clicked.connect(self.cerrar_sesion)
        self.actualizar_botones_administrador()
        self.nav = NavigationManager.get_instance()


    def regresar_a_busqueda(self):
        print("Regresando")
        from pagina_busqueda import PaginaBusqueda
        self.nav.mostrar("busqueda", PaginaBusqueda, self.controlador)


    def confirmar_salida(self):
        from confirm_dialog import ConfirmDialog
        dlg = ConfirmDialog(
            self,
            title="Salir de la aplicación",
            text="¿Estás seguro de que deseas salir?",
            on_confirm=lambda: QApplication.quit()
        )
        dlg.exec()
    def filtrar_recetas(self):
        if self.botonDulce.isChecked():
            filtradas = [r for r in self.recetas if r.tipo.lower() == "dulce"]
        elif self.botonSalado.isChecked():
            filtradas = [r for r in self.recetas if r.tipo.lower() == "salado"]
        else:
            filtradas = self.recetas

        self.mostrar_recetas(filtradas)

    def mostrar_recetas(self, lista):
        self.listaRecetas.clear()
        for receta in lista:
            item = QListWidgetItem(receta.nombre)
            item.setData(Qt.ItemDataRole.UserRole, receta)
            self.listaRecetas.addItem(item)

    def open_info(self, page_key):
        from message_dialog import MessageDialog
        msg = (
            "Esta es la lista de Recetas.\n\n"
            "Desde aquí puedes aplicar un filtro para ver recetas, o verlas todas. "
            "Haz clic en una receta para verla."
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