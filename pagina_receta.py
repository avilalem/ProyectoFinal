import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox, QLabel
from PyQt6.QtCore import Qt
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

        # Configurar elementos de la interfaz
        self._configurar_titulo()
        self.listaIngredientes.setPlainText(self.obtener_ingredientes_texto(1.0))
        self.textProcedimiento.setPlainText(self.receta.instrucciones)
        self.lineCantidad.setText("1")

        # Inicializar lista de compras global (persistente entre ventanas)
        self.lista_compras_global = self.obtener_lista_compras_global()

        # Conectar señales
        self.botonSalir.clicked.connect(self.confirmar_salida)
        self.botonEditar.clicked.connect(self.abrir_editar)
        self.botonCarritoCompras.clicked.connect(self.mostrar_opciones_carrito)
        self.botonEliminar.clicked.connect(self.confirmar_eliminar)
        self.lineCantidad.textChanged.connect(self.actualizar_ingredientes)
        self.botonRegresar.clicked.connect(self.regresar)

        if hasattr(self, 'botonInfo'):
            self.botonInfo.clicked.connect(lambda: self.open_info("receta_general"))

        self.actualizar_botones_administrador()

    def obtener_lista_compras_global(self):
        """Obtiene o crea la lista de compras global"""
        # Usar una variable estática o almacenar en el controlador
        if hasattr(self.controlador, 'lista_compras_global'):
            return self.controlador.lista_compras_global
        else:
            lista = ListaCompras(self.db)
            self.controlador.lista_compras_global = lista
            return lista

    def mostrar_opciones_carrito(self):
        """Muestra el diálogo con opciones para el carrito"""
        from confirm_dialog import ConfirmDialog

        # Crear diálogo personalizado con dos opciones
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Agregar a Lista de Compras")
        dlg.setText(f"¿Cómo deseas agregar '{self.receta.nombre}' a la lista?")

        # Crear botones personalizados
        btn_agregar = dlg.addButton("Agregar a lista", QMessageBox.ButtonRole.AcceptRole)
        btn_agregar_ir = dlg.addButton("Agregar e ir al carrito", QMessageBox.ButtonRole.ActionRole)
        btn_cancelar = dlg.addButton("Cancelar", QMessageBox.ButtonRole.RejectRole)

        dlg.exec()

        clicked_button = dlg.clickedButton()

        if clicked_button == btn_agregar:
            self.agregar_a_lista_compras(redirigir=False)
        elif clicked_button == btn_agregar_ir:
            self.agregar_a_lista_compras(redirigir=True)

    def agregar_a_lista_compras(self, redirigir=False):
        """Agrega la receta a la lista de compras con el multiplicador actual"""
        try:
            factor_text = self.lineCantidad.text().strip()
            if not factor_text:
                multiplicador = 1.0
            else:
                multiplicador = float(factor_text)

            if multiplicador <= 0:
                QMessageBox.warning(self, "Error", "El multiplicador debe ser mayor que 0")
                return

            # Crear una copia temporal de la receta con el multiplicador
            receta_con_multiplicador = {
                'receta': self.receta,
                'multiplicador': multiplicador,
                'ingredientes_ajustados': []
            }

            # Calcular ingredientes ajustados
            for ingrediente, cantidad in self.receta.ingredientes:
                cantidad_ajustada = cantidad * multiplicador
                receta_con_multiplicador['ingredientes_ajustados'].append({
                    'ingrediente': ingrediente,
                    'cantidad': cantidad_ajustada
                })

            # Agregar a la lista global
            if not hasattr(self.lista_compras_global, 'recetas_agregadas'):
                self.lista_compras_global.recetas_agregadas = []

            # Evitar duplicados
            receta_existente = False
            for receta_guardada in self.lista_compras_global.recetas_agregadas:
                if (receta_guardada['receta'].id == self.receta.id and
                        receta_guardada['multiplicador'] == multiplicador):
                    receta_existente = True
                    break

            if not receta_existente:
                self.lista_compras_global.recetas_agregadas.append(receta_con_multiplicador)

            # Agregar ingredientes a la lista de compras
            for ingrediente, cantidad in self.receta.ingredientes:
                cantidad_ajustada = cantidad * multiplicador
                self.lista_compras_global._agregar_ingrediente(ingrediente, cantidad_ajustada)

            mensaje = f"✅ '{self.receta.nombre}' agregada a lista de compras (x{multiplicador})"

            if redirigir:
                mensaje += "\n\nRedirigiendo al carrito..."
                QMessageBox.information(self, "Agregado", mensaje)
                self.abrir_lista_compras()
            else:
                QMessageBox.information(self, "Agregado", mensaje)

        except ValueError:
            QMessageBox.warning(self, "Error", "Por favor ingresa un número válido para la cantidad")

    def abrir_lista_compras(self):
        """Abre la página de lista de compras"""
        from pagina_lista_compras import PaginaListaCompras
        ventana_compras = PaginaListaCompras(self.controlador, self.lista_compras_global)
        self.controlador.mostrar(ventana_compras)

    # ... (el resto de los métodos se mantienen igual)
    def _configurar_titulo(self):
        posibles_labels = ['labelTitulo', 'tituloLabel', 'lblTitulo', 'Titulo']
        for label_name in posibles_labels:
            if hasattr(self, label_name):
                getattr(self, label_name).setText(self.receta.nombre)
                return
        self.setWindowTitle(f"Receta: {self.receta.nombre}")

    def confirmar_salida(self):
        from confirm_dialog import ConfirmDialog
        dlg = ConfirmDialog(
            self,
            title="Salir de la aplicación",
            text="¿Estás seguro de que deseas salir?",
            on_confirm=lambda: QApplication.quit()
        )
        dlg.exec()

    def obtener_ingredientes_texto(self, multiplicador: float = 1.0):
        texto = ""
        for ingrediente, cantidad in self.receta.ingredientes:
            cantidad_ajustada = cantidad * multiplicador
            if cantidad_ajustada.is_integer():
                cantidad_str = str(int(cantidad_ajustada))
            else:
                cantidad_str = f"{cantidad_ajustada:.2f}".rstrip('0').rstrip('.')

            texto += f"• {cantidad_str} {ingrediente.unidad} de {ingrediente.nombre}\n"
        return texto

    def actualizar_ingredientes(self):
        try:
            factor_text = self.lineCantidad.text().strip()
            if not factor_text:
                factor = 1.0
            else:
                factor = float(factor_text)

            if factor <= 0:
                factor = 1.0

        except ValueError:
            factor = 1.0

        texto_ingredientes = self.obtener_ingredientes_texto(factor)
        self.listaIngredientes.setPlainText(texto_ingredientes)

    def abrir_editar(self):
        if not self.nav.es_administrador:
            QMessageBox.warning(self, "Acceso denegado", "Solo los administradores pueden editar recetas")
            return

        from pagina_editar_receta import PaginaEditarReceta
        ventana_editar = PaginaEditarReceta(self.controlador, self.receta_id)
        self.controlador.mostrar(ventana_editar)

    def confirmar_eliminar(self):
        if not self.nav.es_administrador:
            QMessageBox.warning(self, "Acceso denegado", "Solo los administradores pueden eliminar recetas")
            return

        from confirm_dialog import ConfirmDialog
        dlg = ConfirmDialog(
            self,
            title="Eliminar Receta",
            text=f"¿Estás seguro de que deseas eliminar '{self.receta.nombre}'?\n\nEsta acción no se puede deshacer.",
            on_confirm=self._eliminar_receta
        )
        dlg.exec()

    def _eliminar_receta(self):
        try:
            self.db.execute("DELETE FROM recetas WHERE id = ?", (self.receta_id,))
            QMessageBox.information(self, "Eliminado", "Receta eliminada correctamente")
            self.regresar()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo eliminar la receta: {str(e)}")

    def regresar(self):
        from pagina_lista import PaginaLista
        ventana_lista = PaginaLista(self.controlador)
        self.controlador.mostrar(ventana_lista)

    def actualizar_botones_administrador(self):
        from navigation import NavigationManager
        nav = NavigationManager.get_instance()
        es_admin = nav.es_administrador
        botones_admin = ['botonEditar', 'botonEliminar', 'botonCerrarS']
        for boton_name in botones_admin:
            if hasattr(self, boton_name):
                getattr(self, boton_name).setVisible(es_admin)

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
        else:
            msg = "Ayuda general para esta sección."

        dlg = MessageDialog(self, title="Ayuda", text=msg, editable=False)
        dlg.exec()