class NavigationManager:
    _instance = None

    def __init__(self):
        self.ventanas = {}
        self.ventana_actual = None
        self.historial = []

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = NavigationManager()
        return cls._instance

    def mostrar(self, clave_ventana, ventana_class, *args, **kwargs):
        print(f"Navegando a: {clave_ventana}")
        if self.ventana_actual:
            ventana_actual_key = self._obtener_clave_ventana(self.ventana_actual)
            if ventana_actual_key:
                self.historial.append(ventana_actual_key)

        if self.ventana_actual:
            self.ventana_actual.hide()

        if clave_ventana not in self.ventanas:
            print(f"Creando instancia de {ventana_class.__name__}")
            self.ventanas[clave_ventana] = ventana_class(*args, **kwargs)
        else:
            print(f"Reutilizando instancia existente de {ventana_class.__name__}")

        self.ventana_actual = self.ventanas[clave_ventana]
        self.ventana_actual.show()

    def volver_atras(self):
        if len(self.historial) > 0:
            ventana_anterior_key = self.historial.pop()
            if ventana_anterior_key in self.ventanas:
                if self.ventana_actual:
                    self.ventana_actual.hide()
                self.ventana_actual = self.ventanas[ventana_anterior_key]
                self.ventana_actual.show()

    def _obtener_clave_ventana(self, ventana):
        for clave, v in self.ventanas.items():
            if v == ventana:
                return clave
        return None