from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QListWidgetItem
from PyQt6.QtCore import Qt
from database import SQLiteDatabase
from models import Receta


class PaginaBusqueda(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/pagina_busqueda.ui", self)

        self.db = SQLiteDatabase()
        self.cajaBusqueda.textChanged.connect(self.buscar_recetas)
        self.resultadosLista.itemClicked.connect(self.mostrar_receta)
        self.botonSalir.clicked.connect(self.confirmar_salida)
        self.recetas = self.db.obtener_todas_recetas()
        self.actualizar_lista(self.recetas)
        self.botonTodas.clicked.connect(self.abrir_pagina_lista)
        self.botonInfo.clicked.connect(lambda: self.open_info("pagina_busqueda"))
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
        self.pagina_lista = PaginaLista()
        self.pagina_lista.show()
        self.close()
    def open_info(self, page_key):
        msg = (
            "Esta es la ventana de Busqueda.\n\n"
            "Desde aquí puedes ingresar una palabra clave del titulo de la Receta. "
            "Haz clic en la receta para verla"
        )
        dlg = MessageDialog(self, title="Ayuda - Página Principal", text=msg, editable=False)
        dlg.exec()
