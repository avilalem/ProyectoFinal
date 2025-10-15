import sqlite3 as sql
from sqlite3 import Connection, Cursor


class IDatabaseConnection():
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
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS recetas (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        nombre TEXT NOT NULL, 
        categoria TEXT CHECK(categoria IN('DULCE', 'SALADO')),
        instrucciones TEXT)""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingredientes(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        receta_id INTEGER NOT NULL, 
        nombre TEXT NOT NULL, 
        cantidad REAL, 
        unidad TEXT NOT NULL, 
        FOREIGN KEY(receta_id) REFERENCES recetas(id) ON DELETE CASCADE)
        """)
        self.connection.commit()
    def execute(self, query, params=()):
        try:
            cursor:Cursor=self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            return cursor.lastrowid
        except sql.Error as e:
            raise Exception(f"Error al ejecutar la consulta: {e}")
    def fetchall(self, query, params=()):
        try:
            cursor: Cursor = self.connection.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        except sql.Error as e:
            raise Exception(f"Error al ejecutar la consulta: {e}")

    def fetchone(self, query, params=()):
        try:
            cursor: Cursor = self.connection.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()
        except sql.Error as e:
            raise Exception(f"Error al ejecutar la consulta: {e}")

    def close(self):
        try:
            if self.connection:
                self.connection.close()
                return True
        except sql.Error as e:
            return False






