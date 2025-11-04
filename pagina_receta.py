import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox
from database import SQLiteDatabase
from models import Receta, Ingrediente


class PaginaReceta(QMainWindow):
    def __init__(self, controlador,receta_id: int):
        super().__init__()
        uic.loadUi("pagina_receta.ui", self)
        self.db = SQLiteDatabase()
        self.receta_id = receta_id
        self.controlador=controlador
        self.receta = self.db.cargar_receta_con_ingredientes(self.receta_id)
        self.Titulo.setText(self.receta.nombre)
        self.textProcedimiento.setPlainText(self.receta.procedimiento)
        self.mostrar_ingredientes()
        ####
        self.botonSalir.clicked.connect(self.confirmar_salida)
        self.botonEditar.clicked.connect(self.abrir_editar)
        self.botonCarritoCompras.clicked.connect(self.abrir_lista_compras)
        self.botonEliminar.clicked.connect(self.confirmar_eliminar)
        self.lineCantidad.textChanged.connect(self.actualizar_cantidades)
        self.botonRegresar.clicked.connect(self.regresar)
        self.botonAgregarReceta.clicked.connect(self.abrir_agregar_receta)

        self.botonInfo.clicked.connect(lambda: self.open_info("receta_general"))
        self.infoCantidad.clicked.connect(lambda: self.open_info("receta_cantidad"))
        self.infoMetric.clicked.connect(lambda : self.open_info("receta_metricas"))

    def confirmar_salida(self):
        from confirm_dialog import ConfirmDialog
        dlg = ConfirmDialog(
            self,
            title="Salir de la aplicación",
            text="¿Estás seguro de que deseas salir?",
            on_confirm=lambda: QApplication.quit()
        )
        dlg.exec()
    def mostrar_ingredientes(self):
        texto = ""
        for ir in self.receta.ingredientes:
            texto += f"{ir.cantidad} {ir.ingrediente.unidad} de {ir.ingrediente.nombre}\n"
        self.textIngredientes.setPlainText(texto)

    def actualizar_cantidades(self):
        try:
            factor = float(self.lineCantidad.text())
        except ValueError:
            factor = 1.0

        texto = ""
        for ir in self.receta.ingredientes:
            nueva_cantidad = round(ir.cantidad * factor, 2)
            texto += f"{nueva_cantidad} {ir.ingrediente.unidad} de {ir.ingrediente.nombre}\n"
        self.textIngredientes.setPlainText(texto)

    def abrir_editar(self):
        from pagina_editar_receta import PaginaEditarReceta
        ventana_editar=PaginaEditarReceta(self.controlador)
        self.controlador.mostrar(ventana_editar)

    def abrir_lista_compras(self):
        from pagina_lista_compras import PaginaListaCompras
        ventana_compras=PaginaListaCompras(self.controlador)
        self.controlador.mostrar(ventana_compras)

    def confirmar_eliminar(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Eliminar Receta")
        msg.setText(f"¿Seguro que deseas eliminar '{self.receta.nombre}'?")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        respuesta = msg.exec()
        if respuesta == QMessageBox.StandardButton.Yes:
            self.db.eliminar_receta(self.receta_id)
            self.close()

    def regresar(self):
        from pagina_busqueda import PaginaBusqueda
        ventana_busqueda=PaginaBusqueda(self.controlador)
        self.controlador.mostrar(ventana_busqueda)

    def abrir_agregar_receta(self):
        from pagina_agregar_receta import PaginaAgregarReceta
        ventana_agregar=PaginaAgregarReceta
        self.controlador.mostrar(ventana_agregar)

    def open_info(self, page_key: str):
        from message_dialog import MessageDialog
        if page_key == "receta_general":
            msg = (
                "Esta es la página de detalles de la receta.\n\n"
                "Aquí puedes ver los ingredientes, procedimiento y opciones para editar o eliminar."
            )
        elif page_key == "receta_cantidad":
            msg = (
                "Aquí puedes ajustar la cantidad de porciones.\n"
                "Por ejemplo, si escribes '2', se duplicarán los ingredientes."
            )
        elif page_key == "receta_metricas":
            msg = (
                "Las unidades métricas indican en qué medida se expresan los ingredientes.\n"
                "Ejemplo: gramos, mililitros, cucharadas, etc."
            )
        else:
            msg = "Ayuda general para esta sección."

        dlg = MessageDialog(self, title="Ayuda", text=msg, editable=False)
        dlg.exec()