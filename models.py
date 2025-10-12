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
        return f"Ingrediente(nombre={self.nombre!r}, cantidad={self.cantidad}, unidad={self.unidad!r}"
class Receta:
    def __init__(self, db:SQLiteDatabase, nombre:str, categoria:str, instrucciones:str=""):
        self.db=db
        self.id:Optional[int]=None
        self.nombre=nombre
        self.categoria=categoria.upper()
        self.instrucciones=instrucciones
        self.ingredientes:List[Ingrediente]=Ingrediente

    def agregar_ingrediente(self,nombre:str, cantidad:float, unidad:str):
        ing=Ingrediente(nombre, cantidad, unidad)
        self.ingredientes.append(ing)
    def guardar(self, ):

