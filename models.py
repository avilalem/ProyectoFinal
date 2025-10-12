from typing import List, Optional
from database import SQLiteDatabase

class Ingrediente:
    def __init__(self, nombre:str, cantidad:float=0.0, unidad: str=""):
        self.nombre=nombre
        self.cantidad=cantidad
        self.unidad=unidad
    def a_tupla(self, receta_id:int):
        return(receta_id, self.nombre, self.cantidad,self.unidad)
    def mostrar_ingrediente(self):
        return f"Ingrediente(nombre={self.nombre!r}, cantidad={self.cantidad}, unidad={self.unidad!r}"
