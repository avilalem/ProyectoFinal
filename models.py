from typing import List, Optional
from database import SQLiteDatabase


class Ingrediente:
    def __init__(self, db: SQLiteDatabase, nombre: str, unidad: str):
        self.db = db
        self.id: Optional[int] = None
        self.nombre = nombre.strip().title()
        self.unidad = unidad.strip()

    def guardar(self):
        existente = self.db.fetchone("SELECT id FROM ingredientes WHERE nombre = ?", (self.nombre,))
        if existente:
            self.id = existente[0]
            return self.id

        self.id = self.db.execute(
            "INSERT INTO ingredientes (nombre, unidad) VALUES (?, ?)",
            (self.nombre, self.unidad)
        )
        return self.id

    def mostrar_ingrediente(self):
        return f"Ingrediente(id={self.id}, nombre='{self.nombre}', unidad='{self.unidad}')"


class Receta:
    def __init__(self, db: SQLiteDatabase, nombre: str, categoria: str, instrucciones: str = ""):
        self.db = db
        self.id: Optional[int] = None
        self.nombre = nombre.strip().title()
        self.categoria = categoria.strip().upper()
        self.instrucciones = instrucciones.strip()
        self.ingredientes: List[tuple[Ingrediente, float]] = []  # (Ingrediente, cantidad)

    def agregar_ingrediente(self, ingrediente: Ingrediente, cantidad: float):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que 0.")

        for ing, _ in self.ingredientes:
            if ing.nombre.lower() == ingrediente.nombre.lower():
                raise ValueError(f"El ingrediente '{ingrediente.nombre}' ya fue agregado a la receta.")

        self.ingredientes.append((ingrediente, cantidad))

    def guardar(self):
        try:
            self.id = self.db.execute("""
                INSERT INTO recetas (nombre, categoria, instrucciones)
                VALUES (?, ?, ?)
            """, (self.nombre, self.categoria, self.instrucciones))

            for ingrediente, cantidad in self.ingredientes:
                ing_id = ingrediente.guardar()
                self.db.execute("""
                    INSERT INTO detalle_receta (receta_id, ingrediente_id, cantidad)
                    VALUES (?, ?, ?)
                """, (self.id, ing_id, cantidad))
            return self.id

        except Exception as e:
            print(f"Error al guardar la receta: {e}")
            return None

    def obtener_ingredientes_ajustados(self, multiplicador: float = 1.0) -> List[tuple]:
        if multiplicador <= 0:
            raise ValueError("El multiplicador debe ser mayor que 0")

        ingredientes_ajustados = []
        for ingrediente, cantidad in self.ingredientes:
            ingredientes_ajustados.append((ingrediente, cantidad * multiplicador))
        return ingredientes_ajustados

    def mostrar_ingredientes_ajustados(self, multiplicador: float = 1.0) -> str:
        if not self.ingredientes:
            return "No hay ingredientes"

        texto = "Ingredientes:\n"
        for ingrediente, cantidad in self.obtener_ingredientes_ajustados(multiplicador):
            if cantidad.is_integer():
                cantidad_str = str(int(cantidad))
            else:
                cantidad_str = f"{cantidad:.2f}".rstrip('0').rstrip('.')

            texto += f"- {cantidad_str} {ingrediente.unidad} de {ingrediente.nombre}\n"

        return texto

    @staticmethod
    def obtener_todas(db: SQLiteDatabase):
        recetas_tuplas = db.fetchall("SELECT id, nombre, categoria FROM recetas ORDER BY nombre")
        recetas_objetos = []

        for receta_id, nombre, categoria in recetas_tuplas:
            receta = Receta.obtener_por_id(db, receta_id)
            if receta:
                recetas_objetos.append(receta)

        return recetas_objetos

    @staticmethod
    def obtener_por_id(db: SQLiteDatabase, receta_id: int):
        receta_data = db.fetchone(
            "SELECT id, nombre, categoria, instrucciones FROM recetas WHERE id = ?",
            (receta_id,)
        )
        if not receta_data:
            return None

        receta = Receta(db, receta_data[1], receta_data[2], receta_data[3])
        receta.id = receta_data[0]

        ingredientes_data = db.fetchall("""
            SELECT i.id, i.nombre, i.unidad, d.cantidad
            FROM detalle_receta d
            JOIN ingredientes i ON d.ingrediente_id = i.id
            WHERE d.receta_id = ?
        """, (receta_id,))

        for ing_id, nombre, unidad, cantidad in ingredientes_data:
            ingrediente = Ingrediente(db, nombre, unidad)
            ingrediente.id = ing_id
            receta.agregar_ingrediente(ingrediente, cantidad)

        return receta


class ListaCompras:
    def __init__(self, db: SQLiteDatabase):
        self.db = db
        self.items = []

    def agregar_receta(self, receta: Receta, multiplicador: float = 1.0):
        ingredientes_ajustados = receta.obtener_ingredientes_ajustados(multiplicador)

        for ingrediente, cantidad in ingredientes_ajustados:
            self._agregar_ingrediente(ingrediente, cantidad)

    def _agregar_ingrediente(self, ingrediente: Ingrediente, cantidad: float):
        for i, (ing, cant, unidad) in enumerate(self.items):
            if ing.nombre.lower() == ingrediente.nombre.lower() and ing.unidad.lower() == ingrediente.unidad.lower():
                self.items[i] = (ing, cant + cantidad, ing.unidad)
                return

        self.items.append((ingrediente, cantidad, ingrediente.unidad))

    def obtener_items(self):
        return [(ing.nombre, cantidad, unidad) for ing, cantidad, unidad in self.items]

    def limpiar(self):
        self.items.clear()

    def generar_texto_lista(self):
        if not self.items:
            return "Lista de compras vacía"

        texto = "LISTA DE COMPRAS:\n"
        texto += "=" * 30 + "\n"

        for nombre, cantidad, unidad in self.obtener_items():
            if cantidad.is_integer():
                cantidad_str = str(int(cantidad))
            else:
                cantidad_str = f"{cantidad:.2f}".rstrip('0').rstrip('.')

            texto += f"- {cantidad_str} {unidad} de {nombre}\n"

        return texto

    def generar_pdf(self, nombre_archivo="lista_compras.pdf"):
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter

            c = canvas.Canvas(nombre_archivo, pagesize=letter)
            c.setFont("Helvetica", 12)

            # Título
            c.drawString(100, 750, "Lista de Compras - Recetario Digital")
            c.line(100, 745, 500, 745)

            # Items
            y_pos = 700
            for nombre, cantidad, unidad in self.obtener_items():
                if y_pos < 100:  # Nueva página si se acaba el espacio
                    c.showPage()
                    c.setFont("Helvetica", 12)
                    y_pos = 750
                if cantidad.is_integer():
                    cantidad_str = str(int(cantidad))
                else:
                    cantidad_str = f"{cantidad:.2f}".rstrip('0').rstrip('.')

                item_text = f"{cantidad_str} {unidad} de {nombre}"
                c.drawString(100, y_pos, f"• {item_text}")
                y_pos -= 20

            c.save()
            return True
        except ImportError:
            print("Error: reportlab no está instalado. Instala con: pip install reportlab")
            return False
        except Exception as e:
            print(f"Error al generar PDF: {e}")
            return False

    def esta_vacia(self):
        return len(self.items) == 0