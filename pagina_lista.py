from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QListWidgetItem
from PyQt6.QtCore import Qt
from database import SQLiteDatabase
from models import Receta


class PaginaLista(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/pagina_lista.ui", self)

        self.db = SQLiteDatabase()
        self.recetas = self.db.obtener_todas_recetas()

        self.botonDulce.toggled.connect(self.filtrar_recetas)
        self.botonSalado.toggled.connect(self.filtrar_recetas)
        self.botonTodo.toggled.connect(self.filtrar_recetas)
        self.mostrar_recetas(self.recetas)
        self.botonSalir.toggled.connect(self.confirmar_salida)
        self.botonInfo.clicked.connect(lambda: self.open_info("pagina_principal"))


    def confirmar_salida(self):
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
        msg = (
            "Esta es la lista de Recetas.\n\n"
            "Desde aquí puedes aplicar un filtro para ver recetas, o verlas todas. "
            "Haz clic en una receta para verla."
        )
        dlg = MessageDialog(self, title="Ayuda - Página Principal", text=msg, editable=False)
        dlg.exec()