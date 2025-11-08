import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox
from database import SQLiteDatabase
from navigation import NavigationManager
from models import Receta, Ingrediente, ListaCompras


class PaginaReceta(QMainWindow):
    def __init__(self, controlador, receta_id: int):
        super().__init__()
        uic.loadUi("pagina_receta.ui", self)
        self.db = SQLiteDatabase()
        self.nav = NavigationManager.get_instance()
        self.receta_id = receta_id
        self.controlador = controlador
        self.receta = Receta.obtener_por_id(self.db, self.receta_id)

        if not self.receta:
            QMessageBox.critical(self, "Error", "Receta no encontrada")
            self.close()
            return

        self.Titulo.setText(self.receta.nombre)
        self.textProcedimiento.setPlainText(self.receta.instrucciones)
        self.lista_compras = ListaCompras(self.db)

        self.mostrar_ingredientes()

        self.botonSalir.clicked.connect(self.confirmar_salida)
        self.botonEditar.clicked.connect(self.abrir_editar)
        self.botonCarritoCompras.clicked.connect(self.agregar_a_lista_compras)  # ¡CORREGIDO!
        self.botonEliminar.clicked.connect(self.confirmar_eliminar)
        self.lineCantidad.textChanged.connect(self.actualizar_cantidades)
        self.botonRegresar.clicked.connect(self.regresar)
        self.botonAgregarReceta.clicked.connect(self.abrir_agregar_receta)
        self.actualizar_botones_administrador()
        self.botonInfo.clicked.connect(lambda: self.open_info("receta_general"))
        self.infoCantidad.clicked.connect(lambda: self.open_info("receta_cantidad"))
        self.infoMetric.clicked.connect(lambda: self.open_info("receta_metricas"))

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
        texto = self.receta.mostrar_ingredientes_ajustados(1.0)
        self.textIngredientes.setPlainText(texto)

    def actualizar_cantidades(self):
        try:
            factor_text = self.lineCantidad.text().strip()
            if not factor_text:  # Si está vacío, usar 1
                factor = 1.0
            else:
                factor = float(factor_text)

            if factor <= 0:
                factor = 1.0  # Valor por defecto si es negativo

        except ValueError:
            factor = 1.0  # Valor por defecto si hay error

        texto = self.receta.mostrar_ingredientes_ajustados(factor)
        self.textIngredientes.setPlainText(texto)

    def agregar_a_lista_compras(self):
        try:
            factor_text = self.lineCantidad.text().strip()
            if not factor_text:
                multiplicador = 1.0
            else:
                multiplicador = float(factor_text)

            if multiplicador <= 0:
                QMessageBox.warning(self, "Error", "El multiplicador debe ser mayor que 0")
                return
            self.lista_compras.agregar_receta(self.receta, multiplicador)

            QMessageBox.information(
                self,
                "Agregado a lista de compras",
                f"✅ '{self.receta.nombre}' agregada a lista de compras\n"
                f"Multiplicador: x{multiplicador}\n"
                f"Total de ingredientes en lista: {len(self.lista_compras.items)}"
            )

        except ValueError:
            QMessageBox.warning(self, "Error", "Por favor ingresa un número válido para la cantidad")

    def abrir_editar(self):
        from pagina_editar_receta import PaginaEditarReceta
        ventana_editar = PaginaEditarReceta(self.controlador, self.receta_id)
        self.controlador.mostrar(ventana_editar)

    def abrir_lista_compras(self):
        from pagina_lista_compras import PaginaListaCompras
        ventana_compras = PaginaListaCompras(self.controlador, self.lista_compras)
        self.controlador.mostrar(ventana_compras)

    def confirmar_eliminar(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Eliminar Receta")
        msg.setText(f"¿Seguro que deseas eliminar '{self.receta.nombre}'?")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        respuesta = msg.exec()
        if respuesta == QMessageBox.StandardButton.Yes:
            self.db.execute("DELETE FROM recetas WHERE id = ?", (self.receta_id,))
            QMessageBox.information(self, "Eliminado", "Receta eliminada correctamente")
            self.regresar()

    def regresar(self):
        from pagina_busqueda import PaginaBusqueda
        ventana_busqueda = PaginaBusqueda(self.controlador)
        self.controlador.mostrar(ventana_busqueda)

    def actualizar_botones_administrador(self):
        from navigation import NavigationManager
        nav = NavigationManager.get_instance()
        es_admin = nav.es_administrador
        botones_admin = ['botonEditar', 'botonEliminar', 'botonAgregarReceta', 'botonCerrarS']
        for boton_name in botones_admin:
            if hasattr(self, boton_name):
                getattr(self, boton_name).setVisible(es_admin)

    def abrir_agregar_receta(self):
        from pagina_busqueda import PaginaBusqueda
        self.nav.mostrar("busqueda", PaginaBusqueda, self.controlador)

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