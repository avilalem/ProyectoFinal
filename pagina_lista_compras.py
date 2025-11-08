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

        self.borrarTodo.clicked.connect(self.borrar_lista)
        self.guardarLista.clicked.connect(self.generar_pdf)  # ¡CORREGIDO! guardarLista genera PDF
        self.selectTodo.clicked.connect(self.marcar_todo)
        self.botonSalir.clicked.connect(self.confirmar_salida)
        self.botonInfo.clicked.connect(lambda: self.open_info("pagina_lista_compras"))
        self.botonRegresar.clicked.connect(self.regresar_a_busqueda)
        self.botonCerrarS.clicked.connect(self.cerrar_sesion)

        self.actualizar_botones_administrador()
        self.cargar_lista_compras()

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
        from pagina_busqueda import PaginaBusqueda
        ventana_busqueda = PaginaBusqueda(self.controlador)
        self.controlador.mostrar(ventana_busqueda)

    def cargar_lista_compras(self):
        """Carga los ingredientes desde la lista de compras"""
        self.listaCompras.clear()

        if self.lista_compras.esta_vacia():
            item = QListWidgetItem("La lista de compras está vacía")
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsUserCheckable)  # No checkeable
            self.listaCompras.addItem(item)
            return

        for nombre, cantidad, unidad in self.lista_compras.obtener_items():
            if cantidad.is_integer():
                cantidad_str = str(int(cantidad))
            else:
                cantidad_str = f"{cantidad:.2f}".rstrip('0').rstrip('.')

            item_text = f"{cantidad_str} {unidad} de {nombre}"
            item = QListWidgetItem(item_text)
            item.setCheckState(Qt.CheckState.Unchecked)  # No marcado por defecto
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            self.listaCompras.addItem(item)

    def marcar_todo(self):
        if self.listaCompras.count() == 0 or self.lista_compras.esta_vacia():
            return

        todos_marcados = all(
            self.listaCompras.item(i).checkState() == Qt.CheckState.Checked
            for i in range(self.listaCompras.count())
        )

        nuevo_estado = Qt.CheckState.Unchecked if todos_marcados else Qt.CheckState.Checked

        for i in range(self.listaCompras.count()):
            self.listaCompras.item(i).setCheckState(nuevo_estado)

    def borrar_lista(self):
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
        self.listaCompras.clear()
        QMessageBox.information(self, "Lista borrada", "La lista de compras ha sido borrada correctamente")

    def generar_pdf(self):
        if self.lista_compras.esta_vacia():
            QMessageBox.warning(self, "Lista vacía", "La lista de compras está vacía")
            return

        items_no_marcados = []
        for i in range(self.listaCompras.count()):
            item = self.listaCompras.item(i)
            if item.checkState() == Qt.CheckState.Unchecked:
                items_no_marcados.append(item.text())

        if not items_no_marcados:
            QMessageBox.information(
                self,
                "Lista completa",
                "¡Todos los ingredientes están marcados como comprados!\n"
                "No se generará PDF ya que no hay items pendientes."
            )
            return

        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter

            nombre_archivo = "lista_compras_pendientes.pdf"
            c = canvas.Canvas(nombre_archivo, pagesize=letter)
            c.setFont("Helvetica", 12)

            c.drawString(100, 750, "Lista de Compras Pendientes - Recetario Digital")
            c.line(100, 745, 500, 745)

            c.setFont("Helvetica", 10)
            c.drawString(100, 725, "Ingredientes faltantes por comprar:")
            c.line(100, 722, 500, 722)

            c.setFont("Helvetica", 12)
            y_pos = 690
            for item_text in items_no_marcados:
                if y_pos < 100:  # Nueva página si se acaba el espacio
                    c.showPage()
                    c.setFont("Helvetica", 12)
                    y_pos = 750
                    c.drawString(100, 730, "Lista de Compras Pendientes (continuación)")
                    c.line(100, 725, 500, 725)
                    y_pos = 700

                c.drawString(100, y_pos, f"• {item_text}")
                y_pos -= 20

            c.setFont("Helvetica", 8)
            c.drawString(100, 50, f"Total de items pendientes: {len(items_no_marcados)}")

            c.save()

            QMessageBox.information(
                self,
                "PDF Generado",
                f"Lista de compras pendientes guardada como:\n{nombre_archivo}\n\n"
                f"Items incluidos: {len(items_no_marcados)}\n"
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
            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo generar el PDF: {str(e)}"
            )

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