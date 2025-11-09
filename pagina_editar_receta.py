import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox
from database import SQLiteDatabase
from models import Receta, Ingrediente
from navigation import NavigationManager


class PaginaEditarReceta(QMainWindow):
    def __init__(self, controlador, receta_id):
        super().__init__()
        uic.loadUi("pagina_editar_receta.ui", self)

        self.db = SQLiteDatabase()
        self.nav = NavigationManager.get_instance()
        self.receta_id = receta_id
        self.controlador = controlador
        self.receta = Receta.obtener_por_id(self.db, receta_id)

        self.botonGuardar.clicked.connect(self.guardar_cambios)
        self.botonEliminar.clicked.connect(self.eliminar_receta)
        self.botonCancelar.clicked.connect(self.cancelar_cambios)
        self.botonRegresar.clicked.connect(self.volver)
        self.botonSalir.clicked.connect(self.confirmar_salida)
        self.botonCerrarS.clicked.connect(self.cerrar_sesion)

        if self.receta:
            self.cargar_datos()
        else:
            QMessageBox.critical(self, "Error", "Receta no encontrada")
            self.close()

    def confirmar_salida(self):
        from confirm_dialog import ConfirmDialog
        dlg = ConfirmDialog(
            self,
            title="Salir de la aplicación",
            text="¿Estás seguro de que deseas salir?",
            on_confirm=lambda: QApplication.quit()
        )
        dlg.exec()

    def cargar_datos(self):
        self.lineEdit.setText(self.receta.nombre)
        self.textEditReceta.setPlainText(self.obtener_ingredientes_texto())
        self.textEditProced.setPlainText(self.receta.instrucciones)

    def obtener_ingredientes_texto(self):
        texto = ""
        for ingrediente, cantidad in self.receta.ingredientes:
            if cantidad.is_integer():
                cantidad_str = str(int(cantidad))
            else:
                cantidad_str = f"{cantidad:.2f}".rstrip('0').rstrip('.')

            texto += f"{cantidad_str} {ingrediente.unidad} {ingrediente.nombre}\n"
        return texto.strip()

    def guardar_cambios(self):
        try:
            nombre = self.lineEdit.text().strip()
            ingredientes_texto = self.textEditReceta.toPlainText().strip()
            procedimiento = self.textEditProced.toPlainText().strip()

            if not nombre:
                QMessageBox.warning(self, "Error", "El nombre de la receta es obligatorio")
                self.lineEdit.setFocus()
                return

            if not ingredientes_texto:
                QMessageBox.warning(self, "Error", "Debes ingresar al menos un ingrediente")
                self.textEditReceta.setFocus()
                return

            if not procedimiento:
                QMessageBox.warning(self, "Error", "El procedimiento es obligatorio")
                self.textEditProced.setFocus()
                return

            from confirm_dialog import ConfirmDialog
            dlg = ConfirmDialog(
                self,
                title="Guardar cambios",
                text="¿Estás seguro de que deseas guardar los cambios?",
                on_confirm=lambda: self._procesar_guardado(nombre, ingredientes_texto, procedimiento)
            )
            dlg.exec()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar cambios: {str(e)}")

    def _procesar_guardado(self, nombre, ingredientes_texto, procedimiento):
        try:
            self.db.execute(
                "UPDATE recetas SET nombre = ?, instrucciones = ? WHERE id = ?",
                (nombre.upper(), procedimiento.upper(), self.receta_id)
            )

            self.db.execute("DELETE FROM detalle_receta WHERE receta_id = ?", (self.receta_id,))

            ingredientes_parseados = self.parsear_ingredientes(ingredientes_texto)
            for cantidad, nombre_ing, unidad in ingredientes_parseados:
                ingrediente = Ingrediente(self.db, nombre_ing, unidad)
                ing_id = ingrediente.guardar()

                self.db.execute(
                    "INSERT INTO detalle_receta (receta_id, ingrediente_id, cantidad) VALUES (?, ?, ?)",
                    (self.receta_id, ing_id, cantidad)
                )

            QMessageBox.information(self, "Éxito", "Cambios guardados correctamente")
            self.volver()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar: {str(e)}")

    def parsear_ingredientes(self, texto_ingredientes):
        lineas = texto_ingredientes.split('\n')
        ingredientes = []

        for linea in (linea.strip() for linea in lineas if linea.strip()):
            partes = linea.split()
            if len(partes) < 3:
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
                nombre_ing = nombre_ing.upper().strip()

                ingredientes.append((cantidad, nombre_ing, unidad_normalizada))

            except ValueError:
                continue

        return ingredientes

    def normalizar_unidad(self, unidad):
        unidad = unidad.lower().strip()
        unidades_map = {
            'g': 'GRAMOS', 'gr': 'GRAMOS', 'gramo': 'GRAMOS', 'gramos': 'GRAMOS',
            'kg': 'KILOGRAMOS', 'kilo': 'KILOGRAMOS', 'kilogramo': 'KILOGRAMOS', 'kilogramos': 'KILOGRAMOS',
            'lb': 'LIBRAS', 'lbs': 'LIBRAS', 'libra': 'LIBRAS', 'libras': 'LIBRAS',
            'oz': 'ONZAS', 'onza': 'ONZAS', 'onzas': 'ONZAS',
            'ml': 'MILILITROS', 'mililitro': 'MILILITROS', 'mililitros': 'MILILITROS', 'mlts': 'MILILITROS',
            'l': 'LITROS', 'lt': 'LITROS', 'lts': 'LITROS', 'litro': 'LITROS', 'litros': 'LITROS',
            'taza': 'TAZAS', 'tazas': 'TAZAS', 'taz': 'TAZAS',
            'cda': 'CUCHARADAS', 'cdas': 'CUCHARADAS', 'cucharada': 'CUCHARADAS', 'cucharadas': 'CUCHARADAS',
            'cdta': 'CUCHARADITAS', 'cdtas': 'CUCHARADITAS', 'cucharadita': 'CUCHARADITAS',
            'cucharaditas': 'CUCHARADITAS',
            'copa': 'COPAS', 'copas': 'COPAS',
            'unidad': 'UNIDADES', 'unidades': 'UNIDADES', 'uni': 'UNIDADES', 'ud': 'UNIDADES',
            'pizca': 'PIZCAS', 'pizcas': 'PIZCAS',
            'puñado': 'PUÑADOS', 'puñados': 'PUÑADOS',
            'al gusto': 'AL GUSTO', 'gusto': 'AL GUSTO',
            'diente': 'DIENTES', 'dientes': 'DIENTES',
            'hoja': 'HOJAS', 'hojas': 'HOJAS',
            'rama': 'RAMAS', 'ramas': 'RAMAS'
        }
        return unidades_map.get(unidad, unidad.upper())

    def eliminar_receta(self):
        from confirm_dialog import ConfirmDialog
        dlg = ConfirmDialog(
            self,
            title="Eliminar receta",
            text=f"¿Estás seguro de que deseas eliminar la receta '{self.receta.nombre}'?\n\nEsta acción no se puede deshacer.",
            on_confirm=self._eliminar_receta_confirmada
        )
        dlg.exec()

    def _eliminar_receta_confirmada(self):
        try:
            self.db.execute("DELETE FROM recetas WHERE id = ?", (self.receta_id,))
            QMessageBox.information(self, "Éxito", "Receta eliminada correctamente")
            self.volver()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al eliminar receta: {str(e)}")

    def cancelar_cambios(self):
        from confirm_dialog import ConfirmDialog
        dlg = ConfirmDialog(
            self,
            title="Cancelar cambios",
            text="¿Estás seguro de que deseas descartar los cambios?",
            on_confirm=self._cancelar_confirmado
        )
        dlg.exec()

    def _cancelar_confirmado(self):
        self.receta = Receta.obtener_por_id(self.db, self.receta_id)
        if self.receta:
            self.cargar_datos()
            QMessageBox.information(self, "Información", "Cambios descartados")

    def volver(self):
        from pagina_busqueda import PaginaBusqueda
        ventana_busqueda = PaginaBusqueda(self.controlador)
        self.controlador.mostrar(ventana_busqueda)

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