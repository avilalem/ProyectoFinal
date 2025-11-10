import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication, QListWidgetItem, QMessageBox
from PyQt6.QtCore import Qt
from database import SQLiteDatabase
from navigation import NavigationManager
from models import ListaCompras


class PaginaListaCompras(QMainWindow):
    def __init__(self, controlador, lista_compras: ListaCompras = None):
        super().__init__()
        uic.loadUi("pagina_lista_compras.ui", self)

        self.db = SQLiteDatabase()
        self.controlador = controlador
        self.nav = NavigationManager.get_instance()

        if lista_compras is None:
            self.lista_compras = ListaCompras(self.db)
        else:
            self.lista_compras = lista_compras

        # Conectar señales
        self.borrarTodo.clicked.connect(self.borrar_lista)
        self.guardarLista.clicked.connect(self.generar_pdf)
        self.selectTodo.clicked.connect(self.marcar_todo)
        self.botonSalir.clicked.connect(self.confirmar_salida)
        self.botonInfo.clicked.connect(lambda: self.open_info("pagina_lista_compras"))
        self.botonRegresar.clicked.connect(self.regresar_a_busqueda)
        self.botonCerrarS.clicked.connect(self.cerrar_sesion)

        # NUEVO: Botón para actualizar lista
        if hasattr(self, 'botonCambiosLista'):
            self.botonCambiosLista.clicked.connect(self.aplicar_cambios_lista)

        self.actualizar_botones_administrador()
        self.cargar_lista_compras_completa()

    def cargar_lista_compras_completa(self):
        """Carga tanto las recetas como los ingredientes compilados"""
        self.cargar_lista_recetas()
        self.cargar_lista_ingredientes_compilados()

    def cargar_lista_recetas(self):
        """Carga la lista de recetas agregadas con checkboxes"""
        self.listaRecetas.clear()

        if not hasattr(self.lista_compras, 'recetas_agregadas') or not self.lista_compras.recetas_agregadas:
            item = QListWidgetItem("No hay recetas en la lista")
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsUserCheckable)
            self.listaRecetas.addItem(item)
            return

        for receta_data in self.lista_compras.recetas_agregadas:
            receta = receta_data['receta']
            multiplicador = receta_data['multiplicador']

            item_text = f"{receta.nombre} (x{multiplicador})"
            item = QListWidgetItem(item_text)
            item.setCheckState(Qt.CheckState.Checked)  # Marcado por defecto
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setData(Qt.ItemDataRole.UserRole, receta_data)
            self.listaRecetas.addItem(item)

    def cargar_lista_ingredientes_compilados(self):
        """Carga los ingredientes compilados sin duplicados y con unidades convertidas"""
        self.listaCompras.clear()

        if self.lista_compras.esta_vacia():
            item = QListWidgetItem("No hay ingredientes en la lista")
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsUserCheckable)
            self.listaCompras.addItem(item)
            return

        # Compilar ingredientes de recetas seleccionadas
        ingredientes_compilados = self.compilar_ingredientes()

        for nombre, cantidad, unidad in ingredientes_compilados:
            item_text = f"{cantidad} {unidad} de {nombre}"
            item = QListWidgetItem(item_text)
            item.setCheckState(Qt.CheckState.Checked)  # Marcado por defecto
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            self.listaCompras.addItem(item)

    def compilar_ingredientes(self):
        """Compila ingredientes de recetas seleccionadas, suma cantidades y convierte unidades"""
        ingredientes_totales = {}

        # Obtener recetas seleccionadas
        recetas_seleccionadas = []
        for i in range(self.listaRecetas.count()):
            item = self.listaRecetas.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                receta_data = item.data(Qt.ItemDataRole.UserRole)
                if receta_data:
                    recetas_seleccionadas.append(receta_data)

        # Sumar ingredientes
        for receta_data in recetas_seleccionadas:
            for ingrediente_data in receta_data['ingredientes_ajustados']:
                ingrediente = ingrediente_data['ingrediente']
                cantidad = ingrediente_data['cantidad']
                unidad_original = ingrediente.unidad

                clave = f"{ingrediente.nombre}_{unidad_original}"

                if clave in ingredientes_totales:
                    ingredientes_totales[clave]['cantidad'] += cantidad
                else:
                    ingredientes_totales[clave] = {
                        'nombre': ingrediente.nombre,
                        'cantidad': cantidad,
                        'unidad_original': unidad_original
                    }

        # Convertir unidades
        ingredientes_convertidos = []
        for clave, datos in ingredientes_totales.items():
            cantidad_convertida, unidad_convertida = self.convertir_unidad(
                datos['cantidad'],
                datos['unidad_original']
            )
            ingredientes_convertidos.append((
                datos['nombre'],
                cantidad_convertida,
                unidad_convertida
            ))

        return ingredientes_convertidos

    def convertir_unidad(self, cantidad, unidad_original):
        """Convierte unidades a formatos más convenientes"""
        unidad = unidad_original.upper()

        # Conversiones de peso
        if unidad in ['GRAMOS', 'G', 'GR']:
            if cantidad >= 453.592:  # 1 libra en gramos
                return round(cantidad / 453.592, 2), 'lb'
            elif cantidad >= 28.3495:  # 1 onza en gramos
                return round(cantidad / 28.3495, 2), 'oz'
            else:
                return round(cantidad, 2), 'g'

        elif unidad in ['LIBRAS', 'LB', 'LBS']:
            if cantidad < 1:
                return round(cantidad * 16, 2), 'oz'
            else:
                return round(cantidad, 2), 'lb'

        elif unidad in ['ONZAS', 'OZ']:
            if cantidad >= 16:
                return round(cantidad / 16, 2), 'lb'
            else:
                return round(cantidad, 2), 'oz'

        # Conversiones de volumen
        elif unidad in ['MILILITROS', 'ML', 'MILILITRO']:
            if cantidad >= 236.588:  # 1 taza en ml
                return round(cantidad / 236.588, 2), 'tazas'
            else:
                return round(cantidad, 2), 'ml'

        elif unidad in ['LITROS', 'L', 'LT']:
            if cantidad < 1:
                return round(cantidad * 1000, 2), 'ml'
            else:
                return round(cantidad, 2), 'L'

        elif unidad in ['TAZAS', 'TAZA']:
            if cantidad < 0.25:
                return round(cantidad * 236.588, 2), 'ml'
            else:
                return round(cantidad, 2), 'tazas'

        # Para otras unidades, mantener original
        else:
            return round(cantidad, 2), unidad_original

    def aplicar_cambios_lista(self):
        """Aplica los cambios de selección a la lista de ingredientes"""
        self.cargar_lista_ingredientes_compilados()
        QMessageBox.information(self, "Lista actualizada", "La lista de ingredientes ha sido actualizada")

    def marcar_todo(self):
        """Marca o desmarca todos los ingredientes"""
        if self.listaCompras.count() == 0:
            return

        todos_marcados = all(
            self.listaCompras.item(i).checkState() == Qt.CheckState.Checked
            for i in range(self.listaCompras.count())
        )

        nuevo_estado = Qt.CheckState.Unchecked if todos_marcados else Qt.CheckState.Checked

        for i in range(self.listaCompras.count()):
            self.listaCompras.item(i).setCheckState(nuevo_estado)

    def borrar_lista(self):
        """Limpia toda la lista de compras"""
        from confirm_dialog import ConfirmDialog
        dlg = ConfirmDialog(
            self,
            title="Borrar lista de compras",
            text="¿Estás seguro de que deseas borrar toda la lista de compras?",
            on_confirm=self._limpiar_lista
        )
        dlg.exec()

    def _limpiar_lista(self):
        self.lista_compras.limpiar()
        if hasattr(self.lista_compras, 'recetas_agregadas'):
            self.lista_compras.recetas_agregadas.clear()
        self.listaRecetas.clear()
        self.listaCompras.clear()
        QMessageBox.information(self, "Lista borrada", "La lista de compras ha sido borrada correctamente")

    def generar_pdf(self):
        """Genera PDF con recetas e ingredientes seleccionados"""
        # Obtener recetas seleccionadas
        recetas_seleccionadas = []
        for i in range(self.listaRecetas.count()):
            item = self.listaRecetas.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                receta_data = item.data(Qt.ItemDataRole.UserRole)
                if receta_data:
                    recetas_seleccionadas.append(receta_data)

        # Obtener ingredientes seleccionados
        ingredientes_seleccionados = []
        for i in range(self.listaCompras.count()):
            item = self.listaCompras.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                ingredientes_seleccionados.append(item.text())

        if not recetas_seleccionadas and not ingredientes_seleccionados:
            QMessageBox.warning(self, "Lista vacía", "No hay elementos seleccionados para generar el PDF")
            return

        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter

            nombre_archivo = "lista_compras_final.pdf"
            c = canvas.Canvas(nombre_archivo, pagesize=letter)
            c.setFont("Helvetica-Bold", 14)

            # Título
            c.drawString(100, 750, "LISTA DE COMPRAS FINAL")
            c.line(100, 745, 500, 745)

            y_pos = 720

            # Recetas seleccionadas
            if recetas_seleccionadas:
                c.setFont("Helvetica-Bold", 12)
                c.drawString(100, y_pos, "RECETAS SELECCIONADAS:")
                y_pos -= 20
                c.setFont("Helvetica", 10)

                for receta_data in recetas_seleccionadas:
                    receta = receta_data['receta']
                    multiplicador = receta_data['multiplicador']
                    if y_pos < 100:
                        c.showPage()
                        c.setFont("Helvetica", 10)
                        y_pos = 750

                    c.drawString(120, y_pos, f"• {receta.nombre} (x{multiplicador})")
                    y_pos -= 15

                y_pos -= 10

            # Ingredientes
            if ingredientes_seleccionados:
                c.setFont("Helvetica-Bold", 12)
                c.drawString(100, y_pos, "INGREDIENTES:")
                y_pos -= 20
                c.setFont("Helvetica", 10)

                for ingrediente in ingredientes_seleccionados:
                    if y_pos < 100:
                        c.showPage()
                        c.setFont("Helvetica", 10)
                        y_pos = 750
                        c.drawString(100, 730, "INGREDIENTES (continuación):")
                        y_pos = 710

                    c.drawString(120, y_pos, f"• {ingrediente}")
                    y_pos -= 15

            c.save()

            QMessageBox.information(
                self,
                "PDF Generado",
                f"Lista de compras guardada como:\n{nombre_archivo}\n\n"
                f"Recetas: {len(recetas_seleccionadas)}\n"
                f"Ingredientes: {len(ingredientes_seleccionados)}\n"
                f"El archivo se encuentra en la carpeta de la aplicación."
            )

        except ImportError:
            QMessageBox.critical(
                self,
                "Error",
                "No se pudo generar el PDF. Asegúrate de tener reportlab instalado:\n"
                "pip install reportlab"
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo generar el PDF: {str(e)}")

    # ... (los métodos restantes se mantienen igual)
    def confirmar_salida(self):
        from confirm_dialog import ConfirmDialog
        dlg = ConfirmDialog(
            self,
            title="Salir de la aplicación",
            text="¿Estás seguro de que deseas salir?",
            on_confirm=lambda: QApplication.quit()
        )
        dlg.exec()

    def regresar_a_busqueda(self):
        from pagina_lista import PaginaLista
        ventana_lista = PaginaLista(self.controlador)
        self.controlador.mostrar(ventana_lista)

    def open_info(self, page_key):
        from message_dialog import MessageDialog
        msg = (
            "Esta es la lista de Compras.\n\n"
            "Desde aquí puedes descargar una lista con los ingredientes que necesitas. "
            "Puedes desmarcar los ingredientes que NO necesites."
        )
        dlg = MessageDialog(self, title="Ayuda - Lista de Compras", text=msg, editable=False)
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