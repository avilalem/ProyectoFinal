import sqlite3 as sql
from sqlite3 import Connection, Cursor


class IDatabaseConnection:
    def connect(self):
        raise NotImplementedError
    def execute(self, query:str, params:tuple=()):
        raise NotImplementedError
    def fetchall(self, query:str, params:tuple=()):
        raise NotImplementedError
    def close(self):
        raise NotImplementedError


class SQLiteDatabase(IDatabaseConnection):
    def __init__(self,db_name:str="recetario.db"):
        self.db_name=db_name
        self.connection:Connection=None
        self.connect()
        self._create_tables()
    def connect(self):
        self.connection=sql.connect(self.db_name)
    def _create_tables(self):
        cursor=self.connection.cursor()
        if not self.connection:
            raise Exception("No hay conexión activa con la base de datos.")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS recetas (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        nombre TEXT NOT NULL, 
        categoria TEXT CHECK(categoria IN('DULCE', 'SALADO')),
        instrucciones TEXT)""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingredientes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,  
        nombre TEXT NOT NULL,  
        unidad TEXT NOT NULL 
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS detalle_receta (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        receta_id INTEGER NOT NULL,
        ingrediente_id INTEGER NOT NULL,
        cantidad FLOAT NOT NULL CHECK (cantidad > 0),
        UNIQUE(receta_id, ingrediente_id),
        FOREIGN KEY(receta_id) REFERENCES recetas(id) ON DELETE CASCADE,
        FOREIGN KEY(ingrediente_id) REFERENCES ingredientes(id) ON DELETE CASCADE
         )""")
        self.connection.commit()
    def execute(self, query, params=()):
        try:
            cursor:Cursor=self.connection.cursor()
            if not self.connection:
                raise Exception("No hay conexión activa con la base de datos.")

            cursor.execute(query, params)
            self.connection.commit()
            return cursor.lastrowid
        except sql.Error as e:
            raise Exception(f"Error al ejecutar la consulta: {e}")
    def fetchall(self, query, params=()):
        try:
            cursor: Cursor = self.connection.cursor()
            if not self.connection:
                raise Exception("No hay conexión activa con la base de datos.")

            cursor.execute(query, params)
            return cursor.fetchall()
        except sql.Error as e:
            raise Exception(f"Error al ejecutar la consulta: {e}")


    def fetchone(self, query, params=()):
        try:
            cursor: Cursor = self.connection.cursor()
            if not self.connection:
                raise Exception("No hay conexión activa con la base de datos.")

            cursor.execute(query, params)
            return cursor.fetchone()
        except sql.Error as e:
            raise Exception(f"Error al ejecutar la consulta: {e}")


    def close(self):
        try:
            if self.connection:
                self.connection.close()
                return True
        except sql.Error:
            return False