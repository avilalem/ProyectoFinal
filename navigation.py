class NavigationManager:
    _instance = None

    def __init__(self):
        self.ventanas = {}
        self.ventana_actual = None
        self.historial = []
        self.es_administrador = False

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = NavigationManager()
        return cls._instance

    def login_administrador(self):
        self.es_administrador = True
        print("Sesión de administrador activada")

    def logout_administrador(self):
        self.es_administrador = False
        print("Sesión de administrador cerrada")

    def mostrar(self, clave_ventana, ventana_class, *args, **kwargs):
        print(f"NavigationManager: navegar a clave='{clave_ventana}', clase={ventana_class.__name__}")

        for clave, ventana in list(self.ventanas.items()):
            print(f"Cerrando ventana: {clave}")
            ventana.close()


        self.ventanas.clear()
        self.ventana_actual = None

        print(f"Creando nueva instancia de {ventana_class.__name__}")
        try:
            self.ventanas[clave_ventana] = ventana_class(*args, **kwargs)
        except Exception as e:
            print(f"ERROR al crear la ventana '{clave_ventana}': {e}\n")
            import traceback
            traceback.print_exc()
            return

        self.ventana_actual = self.ventanas[clave_ventana]
        self.ventana_actual.show()
        print(f"Mostrando {clave_ventana}")

    def volver_atras(self):
        if len(self.historial) > 1:
            self.historial.pop()
            clave_anterior = self.historial[-1]
            print(f"Volviendo a: {clave_anterior}")
            pagina_actual = self.paginas[self.clave_actual]
            pagina_actual.hide()
            pagina_anterior = self.paginas[clave_anterior]
            pagina_anterior.show()
            self.clave_actual = clave_anterior
        else:
            print("No hay más páginas a las que regresar.")

    def _obtener_clave_ventana(self, ventana):
        for clave, v in self.ventanas.items():
            if v == ventana:
                return clave
        return None
