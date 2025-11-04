import sys
from PyQt6.QtWidgets import QApplication
from database import SQLiteDatabase
from windows.pagina_principal import PaginaPrincipal


def main():
    app = QApplication(sys.argv)
    db = SQLiteDatabase()
    ventana = PaginaPrincipal()
    ventana.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
