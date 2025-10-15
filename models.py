from typing import List, Optional
from database import SQLiteDatabase

class Ingrediente:
    def __init__(self, nombre:str, cantidad:float=0.0, unidad: str=""):
        self.nombre=nombre
        self.cantidad=cantidad
        self.unidad=unidad
    def to_tuple(self, receta_id:int):
        return(receta_id, self.nombre, self.cantidad,self.unidad)
    def mostrar_ingrediente(self):
        return f"Ingrediente(nombre={self.nombre!r}, cantidad={self.cantidad}, unidad={self.unidad!r})"
class Receta:
    def __init__(self, db:SQLiteDatabase, nombre:str, categoria:str, instrucciones:str=""):
        self.db=db
        self.id:Optional[int]=None
        self.nombre=nombre
        self.categoria=categoria.upper()
        self.instrucciones=instrucciones
        self.ingredientes:List[Ingrediente]=[]

    def agregar_ingrediente(self,nombre:str, cantidad:float, unidad:str):
        ing=Ingrediente(nombre, cantidad, unidad)
        self.ingredientes.append(ing)
    def guardar(self) -> int:
        try:
            if self.categoria not in ("DULCE", "SALADO"):
                raise ValueError("La categoría debe ser 'DULCE' o 'SALADO'")

            receta_id=self.db.execute("""
            INSERT INTO recetas( nombre, categoria, instrucciones) VALUES(?,?,?)
            """, (self.nombre, self.categoria, self.instrucciones))
            if receta_id is None:
                raise Exception("No se pudo insertar la receta en la base de datos")
            for ing in self.ingredientes:
                self.db.execute("""
                INSERT INTO ingredientes (receta_id, nombre, cantidad, unidad) VALUES(?,?,?,?)""",
                                ing.to_tuple(receta_id))
            self.id=receta_id
            return receta_id
        except Exception as e:
            raise Exception(f"No fue posible guardar la receta, error: {e}")
    @staticmethod
    def obtener_todas(db:SQLiteDatabase):
        rows=db.fetchall("SELECT id, nombre, categoria FROM recetas ORDER BY nombre")
        return rows

    @staticmethod
    def obtener_por_id(db: SQLiteDatabase, receta_id: int):
        receta_data = db.fetchone("SELECT id, nombre, categoria, instrucciones FROM recetas WHERE id = ?", (receta_id,))
        if not receta_data:
            return None

        receta = Receta(db, receta_data[1], receta_data[2], receta_data[3])
        receta.id = receta_data[0]

        ingredientes_data = db.fetchall("SELECT nombre, cantidad, unidad FROM ingredientes WHERE receta_id = ?",
                                        (receta_id,))
        for nombre, cantidad, unidad in ingredientes_data:
            receta.agregar_ingrediente(nombre, cantidad, unidad)

        return receta

    def actualizar(self):
        if not self.id:
            raise Exception("No se puede actualizar una receta que no existe en la base de datos")

        self.db.execute("""
            UPDATE recetas
            SET nombre = ?, categoria = ?, instrucciones = ?
            WHERE id = ?
        """, (self.nombre, self.categoria, self.instrucciones, self.id))

    def eliminar(self):
        if not self.id:
            raise Exception("No se puede eliminar una receta sin ID asignado")
        self.db.execute("DELETE FROM recetas WHERE id = ?", (self.id,))





