import sys
from PyQt6.QtWidgets import QApplication
from pagina_principal import PaginaPrincipal
from navigation import NavigationManager


class AppController:
    def __init__(self):
        self.ventana_actual = None
        self._ventanas = []

    def mostrar(self, ventana):
        if self.ventana_actual:
            self.ventana_actual.hide()
        self.ventana_actual = ventana
        self._ventanas.append(ventana)
        ventana.show()


if __name__ == "__main__":
    app = QApplication([])

    nav = NavigationManager.get_instance()
    nav.mostrar("principal", PaginaPrincipal, None)
    app.exec()

    """controlador = AppController()
    window = PaginaPrincipal(controlador)
    nav.ventanas["principal"] = window
    nav.ventana_actual = window
    controlador.mostrar(window)

    sys.exit(app.exec())"""