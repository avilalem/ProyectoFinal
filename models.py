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
    @staticmethod
    def obtener_todas(db:SQLiteDatabase):
        rows=db.fetchall("SELECT id, nombre, categoria FROM recetas ORDER BY nombre")




