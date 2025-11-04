import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication
from database import SQLiteDatabase
from models import Receta
from navigation import NavigationManager

class PaginaEditarReceta(QMainWindow):
    def __init__(self, controlador, receta_id):
        super().__init__()
        uic.loadUi("pagina_editar_receta.ui", self)

        self.db = SQLiteDatabase()
        self.receta_id = receta_id
        self.receta = Receta.obtener_por_id(self.db, receta_id)
        self.controlador = controlador
        self.botonGuardar.setText("Guardar cambios")
        self.botonEliminar.setText("Eliminar receta")

        self.botonGuardar.clicked.connect(self.guardar_cambios)
        self.botonEliminar.clicked.connect(self.eliminar_receta)
        self.botonRegresar.clicked.connect(self.volver)
        self.botonSalir.clicked.connect(self.confirmar_salida)

        if self.receta:
            self.cargar_datos()

    def confirmar_salida(self):
        from confirm_dialog import ConfirmDialog
        dlg = ConfirmDialog(
            self,
            title="Salir de la aplicación",
            text="¿Estás seguro de que deseas salir?",
            on_confirm=lambda: QApplication.quit()
        )
        dlg.exec()

    def cargar_datos(self):
        self.lineCategoria.setText(self.receta.categoria)
        self.lineNombre.setText(self.receta.nombre)
        self.textIngredientes.setPlainText(self.receta.obtener_ingredientes_texto())
        self.textProcedimiento.setPlainText(self.receta.procedimiento)

    def guardar_cambios(self):
        from message_dialog import MessageDialog
        self.receta.nombre = self.lineNombre.text().strip()
        self.receta.categoria = self.lineCategoria.text().strip()
        self.receta.procedimiento = self.textProcedimiento.toPlainText().strip()
        ingredientes_texto = self.textIngredientes.toPlainText().strip()

        self.receta.actualizar_ingredientes_desde_texto(ingredientes_texto)
        self.receta.guardar()

        MessageDialog(self, title="Guardado", text="Los cambios se han guardado correctamente.").exec()

    def eliminar_receta(self):
        from message_dialog import MessageDialog
        self.receta.eliminar()
        MessageDialog(self, title="Eliminada", text="La receta ha sido eliminada exitosamente.").exec()
        self.close()

    def volver(self):
        print("Regresando")
        from pagina_receta import PaginaReceta
        self.nav.mostrar("receta", PaginaReceta, self.controlador)


