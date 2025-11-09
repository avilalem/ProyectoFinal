import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox
from database import SQLiteDatabase
from models import Receta, Ingrediente
from navigation import NavigationManager


class PaginaAgregarReceta(QMainWindow):

    def __init__(self, controlador):
        super().__init__()
        uic.loadUi("pagina_agregar_receta.ui", self)

        self.db = SQLiteDatabase()
        self.controlador = controlador
        self.nav = NavigationManager.get_instance()

        self.botonSalir.clicked.connect(self.confirmar_salida)
        self.botonGuardar.clicked.connect(self.confirmar_guardar)
        self.botonEliminar.clicked.connect(self.confirmar_eliminar)
        self.botonRegresar.clicked.connect(self.regresar)

        self.configurar_categorias()

    def configurar_categorias(self):
        if hasattr(self.categorias, 'setMinimum') and hasattr(self.categorias, 'setMaximum'):
            self.categorias.setMinimum(0)
            self.categorias.setMaximum(1)
            self.categorias.setValue(0)

    def confirmar_salida(self):
        from confirm_dialog import ConfirmDialog
        dlg = ConfirmDialog(
            self,
            title="Salir de la aplicación",
            text="¿Estás seguro de que deseas salir?",
            on_confirm=lambda: QApplication.quit()
        )
        dlg.exec()

    def confirmar_guardar(self):
        from confirm_dialog import ConfirmDialog
        dlg = ConfirmDialog(
            self,
            title="Guardar receta",
            text="¿Deseas guardar esta receta en la base de datos?",
            on_confirm=self.guardar_receta
        )
        dlg.exec()

    def confirmar_eliminar(self):
        from confirm_dialog import ConfirmDialog
        dlg = ConfirmDialog(
            self,
            title="Limpiar campos",
            text="¿Deseas eliminar todos los datos ingresados?\n\nEsta acción borrará todo lo que has escrito.",
            on_confirm=self.limpiar_campos
        )
        dlg.exec()

    def normalizar_unidad(self, unidad):
        unidad = unidad.lower().strip()

        unidades_map = {
            # Peso
            'g': 'gramos', 'gr': 'gramos', 'gramo': 'gramos', 'gramos': 'gramos',
            'kg': 'kilogramos', 'kilo': 'kilogramos', 'kilogramo': 'kilogramos', 'kilogramos': 'kilogramos',
            'lb': 'libras', 'lbs': 'libras', 'libra': 'libras', 'libras': 'libras',
            'oz': 'onzas', 'onza': 'onzas', 'onzas': 'onzas',

            # Volumen
            'ml': 'mililitros', 'mililitro': 'mililitros', 'mililitros': 'mililitros', 'mlts': 'mililitros',
            'l': 'litros', 'lt': 'litros', 'lts': 'litros', 'litro': 'litros', 'litros': 'litros',
            'taza': 'tazas', 'tazas': 'tazas', 'taz': 'tazas',
            'cda': 'cucharadas', 'cdas': 'cucharadas', 'cucharada': 'cucharadas', 'cucharadas': 'cucharadas',
            'cdta': 'cucharaditas', 'cdtas': 'cucharaditas', 'cucharadita': 'cucharaditas',
            'cucharaditas': 'cucharaditas',
            'copa': 'copas', 'copas': 'copas',

            # Unidades
            'unidad': 'unidades', 'unidades': 'unidades', 'uni': 'unidades', 'ud': 'unidades',
            'pizca': 'pizcas', 'pizcas': 'pizcas',
            'puñado': 'puñados', 'puñados': 'puñados',

            # Especias/condimentos
            'al gusto': 'al gusto', 'gusto': 'al gusto',

            # Otros
            'diente': 'dientes', 'dientes': 'dientes',
            'hoja': 'hojas', 'hojas': 'hojas',
            'rama': 'ramas', 'ramas': 'ramas'
        }

        return unidades_map.get(unidad, unidad)

    def parsear_ingredientes(self, texto_ingredientes):
        lineas = texto_ingredientes.split('\n')
        ingredientes = []

        for i, linea in enumerate(linea.strip() for linea in lineas if linea.strip()):
            partes = linea.split()
            if len(partes) < 3:
                print(f"Línea ignorada (formato incorrecto): {linea}")
                continue

            try:
                if partes[0].lower() == 'al' and partes[1].lower() == 'gusto':
                    cantidad = 0
                    unidad_original = 'al gusto'
                    nombre_ing = ' '.join(partes[2:])
                else:
                    cantidad = float(partes[0])
                    unidad_original = partes[1]
                    nombre_ing = ' '.join(partes[2:])

                unidad_normalizada = self.normalizar_unidad(unidad_original)
                ingredientes.append((cantidad, nombre_ing, unidad_normalizada))
                print(
                    f"Ingrediente parseado: {cantidad} {unidad_normalizada} de {nombre_ing} (original: {unidad_original})")

            except ValueError:
                print(f"Línea ignorada (cantidad no numérica): {linea}")
                continue
            except Exception as e:
                print(f"Error parseando línea '{linea}': {e}")
                continue

        return ingredientes

    def guardar_receta(self):
        try:
            nombre = self.nombreReceta.text().strip()

            categoria_val = self.categorias.value()
            categoria = "DULCE" if categoria_val == 0 else "SALADO"

            ingredientes_texto = self.listaIngredientes.toPlainText().strip()
            procedimiento = self.procedimiento.toPlainText().strip()

            if not nombre:
                QMessageBox.warning(self, "Error", "El nombre de la receta es obligatorio")
                self.nombreReceta.setFocus()
                return

            if not ingredientes_texto:
                QMessageBox.warning(self, "Error", "Debes ingresar al menos un ingrediente")
                self.listaIngredientes.setFocus()
                return

            receta = Receta(self.db, nombre, categoria, procedimiento)

            ingredientes_parseados = self.parsear_ingredientes(ingredientes_texto)
            if not ingredientes_parseados:
                QMessageBox.warning(self, "Error",
                                    "No se pudieron procesar los ingredientes.\n\n"
                                    "Formato esperado por línea:\n"
                                    "'cantidad unidad nombre'\n\n"
                                    "Ejemplos:\n"
                                    "200 g harina\n"
                                    "2 cucharadas azúcar\n"
                                    "1 taza leche\n"
                                    "500 ml agua\n"
                                    "al gusto sal"
                                    )
                return

            for cantidad, nombre_ing, unidad in ingredientes_parseados:
                ingrediente = Ingrediente(self.db, nombre_ing, unidad)
                receta.agregar_ingrediente(ingrediente, cantidad)

            receta_id = receta.guardar()
            if receta_id:
                QMessageBox.information(
                    self,
                    "Éxito",
                    f"Receta '{nombre}' guardada correctamente\n\n"
                    f"Detalles:\n"
                    f"• Categoría: {categoria}\n"
                    f"• Ingredientes: {len(ingredientes_parseados)}\n"
                    f"• ID: {receta_id}"
                )
                self.limpiar_campos()
            else:
                QMessageBox.critical(self, "Error", "No se pudo guardar la receta")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar receta: {str(e)}")

    def limpiar_campos(self):
        self.nombreReceta.clear()
        self.categorias.setValue(0)
        self.listaIngredientes.clear()
        self.procedimiento.clear()
        self.nombreReceta.setFocus()

    def regresar(self):
        from pagina_principal_admin import PaginaAdmin
        ventana_admin = PaginaAdmin(self.controlador)
        self.controlador.mostrar(ventana_admin)