import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox,QComboBox
from database import SQLiteDatabase
from models import Receta, Ingrediente
from navigation import NavigationManager
from message_dialog import MessageDialog


class PaginaAgregarReceta(QMainWindow):

    def __init__(self, controlador):
        super().__init__()
        uic.loadUi("pagina_agregar_receta.ui", self)

        self.db = SQLiteDatabase()
        self.controlador = controlador
        self.nav = NavigationManager.get_instance()
        self.comboCategoria = self.findChild(QComboBox, "comboCategoria")
        self.botonSalir.clicked.connect(self.confirmar_salida)
        self.botonGuardar.clicked.connect(self.confirmar_guardar)
        self.botonEliminar.clicked.connect(self.confirmar_eliminar)
        self.botonRegresar.clicked.connect(self.regresar)
        self.botonCerrarS.clicked.connect(self.cerrar_sesion)
        self.botonInfo.clicked.connect(lambda: self.open_info("pagina_agregar_receta"))
        categoria = ["DULCE", "SALADO"]

        self.comboCategoria.addItems(categoria)
        self.nombreReceta.setFocus()

    def open_info(self, page_key):
        from message_dialog import MessageDialog
        msg = (
            "Aqui puedes agregar recetas.\n\n"
            "Tienes que seguir el formato especifico: "
            "Cantidad UnidadMetrica NombreIngrediente"
            "Por ejemplo: 100 gramos azucar"
            "Puedes presionar 'Guardar' para guardar la nueva receta o 'Eliminar' para borrar los cambios."
        )
        dlg = MessageDialog(self, title="Ayuda - Página Nueva Receta", text=msg, editable=False)
        dlg.exec()

    def cerrar_sesion(self):
        if self.nav.es_administrador:
            self.nav.logout_administrador()
            dlg = MessageDialog(self,
                                title="Sesión Cerrada",
                                text="Sesión de administrador cerrada correctamente",
                                editable=False)
            dlg.exec()

            from pagina_principal import PaginaPrincipal
            self.nav.mostrar("principal", PaginaPrincipal, self.controlador)

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
        if self.validar_campos():
            from confirm_dialog import ConfirmDialog
            dlg = ConfirmDialog(
                self,
                title="Guardar receta",
                text="¿Deseas guardar esta receta en la base de datos?",
                on_confirm=self.guardar_receta
            )
            dlg.exec()

    def validar_campos(self):
        nombre = self.nombreReceta.text().strip()
        ingredientes_texto = self.listaIngredientes.toPlainText().strip()
        procedimiento = self.procedimiento.toPlainText().strip()

        if not nombre:
            QMessageBox.warning(self, "Error", "El nombre de la receta es obligatorio")
            self.nombreReceta.setFocus()
            return False

        if len(nombre) < 2:
            QMessageBox.warning(self, "Error", "El nombre de la receta debe tener al menos 2 caracteres")
            self.nombreReceta.setFocus()
            return False

        if not ingredientes_texto:
            QMessageBox.warning(self, "Error", "Debes ingresar al menos un ingrediente")
            self.listaIngredientes.setFocus()
            return False

        lineas_validas = [linea.strip() for linea in ingredientes_texto.split('\n') if linea.strip()]
        if len(lineas_validas) == 0:
            QMessageBox.warning(self, "Error", "Debes ingresar al menos un ingrediente válido")
            self.listaIngredientes.setFocus()
            return False

        tiene_ingredientes_validos = False
        for linea in lineas_validas:
            partes = linea.split()
            if len(partes) >= 3:
                tiene_ingredientes_validos = True
                break

        if not tiene_ingredientes_validos:
            QMessageBox.warning(self, "Error",
                                "Formato de ingredientes incorrecto.\n\n"
                                "Cada línea debe tener:\n"
                                "cantidad unidad nombre\n\n"
                                "Ejemplo: '200 g harina'"
                                )
            self.listaIngredientes.setFocus()
            return False

        if not procedimiento:
            QMessageBox.warning(self, "Error", "El procedimiento es obligatorio")
            self.procedimiento.setFocus()
            return False

        if len(procedimiento) < 10:
            QMessageBox.warning(self, "Error", "El procedimiento debe tener al menos 10 caracteres")
            self.procedimiento.setFocus()
            return False

        return True

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
            'g': 'GRAMOS', 'gr': 'GRAMOS', 'gramo': 'GRAMOS', 'gramos': 'GRAMOS',
            'kg': 'KILOGRAMOS', 'kilo': 'KILOGRAMOS', 'kilogramo': 'KILOGRAMOS', 'kilogramos': 'KILOGRAMOS',
            'lb': 'LIBRAS', 'lbs': 'LIBRAS', 'libra': 'LIBRAS', 'libras': 'LIBRAS',
            'oz': 'ONZAS', 'onza': 'ONZAS', 'onzas': 'ONZAS',

            # Volumen
            'ml': 'MILILITROS', 'mililitro': 'MILILITROS', 'mililitros': 'MILILITROS', 'mlts': 'MILILITROS',
            'l': 'LITROS', 'lt': 'LITROS', 'lts': 'LITROS', 'litro': 'LITROS', 'litros': 'LITROS',
            'taza': 'TAZAS', 'tazas': 'TAZAS', 'taz': 'TAZAS',
            'cda': 'CUCHARADAS', 'cdas': 'CUCHARADAS', 'cucharada': 'CUCHARADAS', 'cucharadas': 'CUCHARADAS',
            'cdta': 'CUCHARADITAS', 'cdtas': 'CUCHARADITAS', 'cucharadita': 'CUCHARADITAS',
            'cucharaditas': 'CUCHARADITAS',
            'copa': 'COPAS', 'copas': 'COPAS',

            # Unidades
            'unidad': 'UNIDADES', 'unidades': 'UNIDADES', 'uni': 'UNIDADES', 'ud': 'UNIDADES',
            'pizca': 'PIZCAS', 'pizcas': 'PIZCAS',
            'puñado': 'PUÑADOS', 'puñados': 'PUÑADOS',

            # Especias/condimentos
            'al gusto': 'AL GUSTO', 'gusto': 'AL GUSTO',

            # Otros
            'diente': 'DIENTES', 'dientes': 'DIENTES',
            'hoja': 'HOJAS', 'hojas': 'HOJAS',
            'rama': 'RAMAS', 'ramas': 'RAMAS'
        }

        return unidades_map.get(unidad, unidad.upper())

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

                if not nombre_ing.strip():
                    print(f"Línea ignorada (nombre de ingrediente vacío): {linea}")
                    continue

                unidad_normalizada = self.normalizar_unidad(unidad_original)
                nombre_ing = nombre_ing.upper().strip()

                ingredientes.append((cantidad, nombre_ing, unidad_normalizada))
                print(f"Ingrediente parseado: {cantidad} {unidad_normalizada} de {nombre_ing}")

            except ValueError:
                print(f"Línea ignorada (cantidad no numérica): {linea}")
                continue
            except Exception as e:
                print(f"Error parseando línea '{linea}': {e}")
                continue

        return ingredientes

    def guardar_receta(self):
        try:
            nombre = self.nombreReceta.text().strip().upper()

            categoria = self.comboCategoria.currentText().strip().upper()

            ingredientes_texto = self.listaIngredientes.toPlainText().strip()
            procedimiento = self.procedimiento.toPlainText().strip().upper()

            if not nombre:
                QMessageBox.warning(self, "Error", "El nombre de la receta es obligatorio")
                self.nombreReceta.setFocus()
                return

            if len(nombre) < 2:
                QMessageBox.warning(self, "Error", "El nombre de la receta debe tener al menos 2 caracteres")
                self.nombreReceta.setFocus()
                return

            if categoria not in ["DULCE", "SALADO"]:
                QMessageBox.warning(self, "Error", "Debes seleccionar una categoría válida (DULCE o SALADO)")
                self.comboCategoria.setFocus()
                return

            if not ingredientes_texto:
                QMessageBox.warning(self, "Error", "Debes ingresar al menos un ingrediente")
                self.listaIngredientes.setFocus()
                return

            if not procedimiento:
                QMessageBox.warning(self, "Error", "El procedimiento es obligatorio")
                self.procedimiento.setFocus()
                return

            if len(procedimiento) < 10:
                QMessageBox.warning(self, "Error", "El procedimiento debe tener al menos 10 caracteres")
                self.procedimiento.setFocus()
                return

            receta = Receta(self.db, nombre, categoria, procedimiento)

            ingredientes_parseados = self.parsear_ingredientes(ingredientes_texto)
            if not ingredientes_parseados:
                QMessageBox.warning(self, "Error",
                                    "No se pudieron procesar los ingredientes.\n\n"
                                    "Asegúrate de que cada línea tenga el formato:\n"
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
        self.comboCategoria.setCurrentIndex(0)
        self.listaIngredientes.clear()
        self.procedimiento.clear()
        self.nombreReceta.setFocus()

    def regresar(self):
        from pagina_principal_admin import PaginaAdmin
        self.nav.mostrar("admin_panel", PaginaAdmin, self.controlador)