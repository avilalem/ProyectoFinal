import sys
from PyQt6.QtWidgets import QApplication
from pagina_principal import PaginaPrincipal

class AppController:
    def __init__(self):
        self.ventana_actual = None

    def mostrar(self, ventana):
        if self.ventana_actual:
            self.ventana_actual.close()
        self.ventana_actual = ventana
        ventana.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PaginaPrincipal()
    window.show()
    sys.exit(app.exec())
