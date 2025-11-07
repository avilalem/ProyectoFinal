import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication, QListWidgetItem
from database import SQLiteDatabase


class PaginaListaCompras(QMainWindow):
    def __init__(self, controlador):
        super().__init__()
        uic.loadUi("pagina_lista_compras.ui", self)

        self.db = SQLiteDatabase()
        self.ingredientes_lista = {}  # {nombre: cantidad_total}
        self.controlador=controlador
        self.borrarTodo.clicked.connect(self.borrar_lista)
        self.guardarLista.clicked.connect(self.guardar_lista)
        self.selectTodo.clicked.connect(self.marcar_todo)
        self.cargar_lista_compras()
        self.botonSalir.clicked.connect(self.confirmar_salida)
        self.botonInfo.clicked.connect(lambda: self.open_info("pagina_lista_compras"))
        self.botonRegresar.clicked.connect(self.regresar_a_receta)
        self.botonCerrarS.clicked.connect(self.cerrar_sesion)
        self.actualizar_botones_administrador()


    def confirmar_salida(self):
        from confirm_dialog import ConfirmDialog
        dlg = ConfirmDialog(
            self,
            title="Salir de la aplicación",
            text="¿Estás seguro de que deseas salir?",
            on_confirm=lambda: QApplication.quit()
        )
        dlg.exec()

    def regresar_a_receta(self):
        print("Regresando")
        from pagina_receta import PaginaReceta
        self.nav.mostrar("Receta", PaginaReceta, self.controlador)

    def cargar_lista_compras(self):
        self.listaCompras.clear()
        self.ingredientes_lista.clear()

        ingredientes = self.db.fetchall("""
            SELECT i.nombre, SUM(ri.cantidad) as total, i.unidad
            FROM receta_ingrediente ri
            JOIN ingredientes i ON i.id = ri.id_ingrediente
            GROUP BY i.nombre, i.unidad
        """)

        for nombre, total, unidad in ingredientes:
            self.ingredientes_lista[nombre] = (total, unidad)

        for nombre, (total, unidad) in self.ingredientes_lista.items():
            item_text = f"{nombre}: {total:.2f} {unidad}"
            item = QListWidgetItem(item_text)
            item.setCheckState(False)  # no marcado
            self.listaCompras.addItem(item)

    def marcar_todo(self):
        marcar = all(
            self.listaCompras.item(i).checkState() == 0
            for i in range(self.listaCompras.count())
        )
        for i in range(self.listaCompras.count()):
            self.listaCompras.item(i).setCheckState(2 if marcar else 0)

    def borrar_lista(self):
        from message_dialog import MessageDialog
        dlg = MessageDialog(
            self,
            title="Borrar lista",
            text="¿Deseas borrar toda la lista de compras?",
            editable=False
        )
        dlg.exec()
        self.listaCompras.clear()
        self.ingredientes_lista.clear()

    def guardar_lista(self):
        from message_dialog import MessageDialog
        for i in range(self.listaCompras.count()):
            item = self.listaCompras.item(i)
            nombre = item.text().split(":")[0].strip()
            marcado = item.checkState() == 2
            self.db.execute(
                "INSERT OR REPLACE INTO lista_compras (nombre, completado) VALUES (?, ?)",
                (nombre, int(marcado))
            )

        MessageDialog(self, title="Lista guardada", text="La lista se ha guardado correctamente.").exec()

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

        print(f"Modo administrador: {es_admin}")
