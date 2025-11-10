from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QListWidgetItem, QApplication, QButtonGroup
from PyQt6.QtCore import Qt
from database import SQLiteDatabase
from models import Receta, Ingrediente
from navigation import NavigationManager


class PaginaLista(QMainWindow):
    def __init__(self, controlador):
        super().__init__()
        uic.loadUi("pagina_lista.ui", self)

        self.db = SQLiteDatabase()
        self.recetas = Receta.obtener_todas(self.db)
        self.controlador = controlador
        self.nav = NavigationManager.get_instance()

        # Configurar radio buttons
        self.radio_group = QButtonGroup(self)
        self.radio_group.addButton(self.botonDulce)
        self.radio_group.addButton(self.botonSalado)
        self.radio_group.addButton(self.botonTodo)
        self.botonTodo.setChecked(True)
        self.radio_group.buttonToggled.connect(self.on_radio_toggled)

        # Conectar señales
        self.botonSalir.clicked.connect(self.confirmar_salida)
        self.botonInfo.clicked.connect(lambda: self.open_info("pagina_lista"))
        self.botonRegresar.clicked.connect(self.regresar_a_busqueda)
        self.cajaBusqueda.textChanged.connect(self.buscar_recetas)

        # CONEXIÓN PARA DOBLE CLICK CON DEPURACIÓN
        self.listaRecetas.itemDoubleClicked.connect(self.abrir_receta)
        print("✅ Conexión de doble click establecida")

        self.actualizar_botones_administrador()
        self.mostrar_recetas(self.recetas)

    def buscar_recetas(self):
        texto = self.cajaBusqueda.text().strip().lower()

        if texto == "":
            coincidencias = self.recetas
        else:
            coincidencias = [
                receta for receta in self.recetas
                if texto in receta.nombre.lower()
            ]
        self.mostrar_recetas(coincidencias)

    def on_radio_toggled(self, button, checked):
        if checked:
            print(f"Radio seleccionado: {button.text()}")
            self.filtrar_recetas()

    def filtrar_recetas(self):
        if self.botonDulce.isChecked():
            filtradas = [r for r in self.recetas if r.categoria.upper() == "DULCE"]
            print(f"Mostrando {len(filtradas)} recetas dulces")
        elif self.botonSalado.isChecked():
            filtradas = [r for r in self.recetas if r.categoria.upper() == "SALADO"]
            print(f"Mostrando {len(filtradas)} recetas saladas")
        else:
            filtradas = self.recetas
            print(f"Mostrando todas las {len(filtradas)} recetas")

        self.mostrar_recetas(filtradas)

    def abrir_receta(self, item):
        """Abre la receta seleccionada en pagina_receta"""
        print(f"🟢 Doble click detectado en: {item.text()}")

        receta = item.data(Qt.ItemDataRole.UserRole)
        print(f"🔍 Receta obtenida: {receta}")
        print(f"🔍 ID de receta: {receta.id if receta else 'None'}")
        print(f"🔍 Nombre de receta: {receta.nombre if receta else 'None'}")

        if receta and hasattr(receta, 'id'):
            try:
                from pagina_receta import PaginaReceta
                print(f"🚀 Navegando a PaginaReceta con ID: {receta.id}")
                ventana_receta = PaginaReceta(self.controlador, receta.id)
                self.controlador.mostrar(ventana_receta)
                print("✅ Navegación exitosa")
            except Exception as e:
                print(f"❌ Error al navegar: {e}")
        else:
            print("❌ No se pudo obtener la receta o no tiene ID")

    def regresar_a_busqueda(self):
        if self.nav.es_administrador:
            from pagina_principal_admin import PaginaAdmin
            self.nav.mostrar("admin", PaginaAdmin, self.controlador)
        else:
            from pagina_principal import PaginaPrincipal
            self.nav.mostrar("principal", PaginaPrincipal, self.controlador)
            print("Regresando")

    def confirmar_salida(self):
        from confirm_dialog import ConfirmDialog
        dlg = ConfirmDialog(
            self,
            title="Salir de la aplicación",
            text="¿Estás seguro de que deseas salir?",
            on_confirm=lambda: QApplication.quit()
        )
        dlg.exec()

    def mostrar_recetas(self, lista):
        self.listaRecetas.clear()
        for receta in lista:
            item = QListWidgetItem(receta.nombre)
            item.setData(Qt.ItemDataRole.UserRole, receta)
            self.listaRecetas.addItem(item)
        print(f"📝 Mostrando {len(lista)} recetas en la lista")

    def open_info(self, page_key):
        from message_dialog import MessageDialog
        # MANTENER EL open_info ORIGINAL
        msg = (
            "Esta es la lista de Recetas.\n\n"
            "Desde aquí puedes aplicar un filtro para ver recetas, o verlas todas. "
            "Haz clic en una receta para verla."
        )
        dlg = MessageDialog(self, title="Ayuda - Página Principal", text=msg, editable=False)
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