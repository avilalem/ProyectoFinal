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

    @staticmethod
    def obtener_todas(db: SQLiteDatabase):
        return db.fetchall("SELECT id, nombre, categoria FROM recetas ORDER BY nombre")

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
