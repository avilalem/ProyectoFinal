import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication
from database import SQLiteDatabase
from models import Receta
from navigation import NavigationManager
class PaginaAgregarReceta(QMainWindow):

    def __init__(self, controlador):
        super().__init__()
        uic.loadUi("pagina_agregar_receta.ui", self)

        self.db = SQLiteDatabase()
        self.botonSalir.clicked.connect(self.confirmar_salida)
        self.controlador = controlador
        self.nav = NavigationManager.get_instance()
        self.botonGuardar.clicked.connect(self.confirmar_guardar)
        self.botonEliminar.clicked.connect(self.confirmar_eliminar)
        self.botonRegresar.clicked.connect(self.regresar)

    def confirmar_salida(self):
        from confirm_dialog import ConfirmDialog
        dlg = ConfirmDialog(
            self,
            title="Salir de la aplicación",
            text="¿Estás seguro de que deseas salir?",
            on_confirm=lambda: QApplication.quit()
        )
        dlg.exec()
    def confirmar_guardar(self):
        from message_dialog import MessageDialog
        msg = (
            "¿Deseas guardar esta receta?\n\n"
            "Si confirmas, los datos ingresados se guardarán en la base de datos."
        )
        dlg = MessageDialog(self, title="Confirmar guardado", text=msg, editable=False)
        if dlg.exec():
            self.guardar_receta()

    def confirmar_eliminar(self):
        from message_dialog import MessageDialog
        msg = (
            "¿Deseas eliminar todos los datos ingresados?\n\n"
            "Esta acción borrará todo lo que has escrito."
        )
        dlg = MessageDialog(self, title="Confirmar eliminación", text=msg, editable=False)
        if dlg.exec():
            self.limpiar_campos()

    def guardar_receta(self):
        from message_dialog import MessageDialog
        categoria = self.lineCategoria.text().strip()
        nombre = self.lineNombre.text().strip()
        ingredientes_texto = self.textIngredientes.toPlainText().strip()
        procedimiento = self.textProcedimiento.toPlainText().strip()

        if not nombre or not ingredientes_texto:
            msg = "Por favor, ingresa al menos el nombre y los ingredientes."
            dlg = MessageDialog(self, title="Datos incompletos", text=msg, editable=False)
            dlg.exec()
            return

        receta = Receta(self.db, nombre, procedimiento, categoria)
        receta.unidad = unidad
        receta.agregar_ingredientes_desde_texto(ingredientes_texto)
        receta.guardar()

        msg = f"La receta '{nombre}' se ha guardado correctamente."
        dlg = MessageDialog(self, title="Guardado exitoso", text=msg, editable=False)
        dlg.exec()

        self.limpiar_campos()

    def limpiar_campos(self):
        self.lineCategoria.clear()
        self.lineNombre.clear()
        self.spinUnidad.setValue(1)
        self.textIngredientes.clear()
        self.textProcedimiento.clear()

    def regresar(self):
        print("Regresando")
        from pagina_principal_admin import PaginaAdmin
        self.nav.mostrar("admin_panel", PaginaAdmin, self.controlador)


