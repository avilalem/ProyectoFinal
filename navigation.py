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

        if self.ventana_actual:
            ventana_actual_key = self._obtener_clave_ventana(self.ventana_actual)
            if ventana_actual_key:
                self.historial.append(ventana_actual_key)
            try:
                self.ventana_actual.hide()
            except Exception:
                pass

        if clave_ventana not in self.ventanas:
            try:
                print(f"NavigationManager: creando instancia de {ventana_class.__name__}")
                self.ventanas[clave_ventana] = ventana_class(*args, **kwargs)
            except Exception as e:
                import traceback
                print(f"ERROR: al crear {ventana_class.__name__}: {e}")
                traceback.print_exc()
                return
        else:
            print(f"NavigationManager: reutilizando instancia de {ventana_class.__name__}")

        self.ventana_actual = self.ventanas[clave_ventana]
        try:
            self.ventana_actual.show()
            try:
                self.ventana_actual.raise_()
                self.ventana_actual.activateWindow()
            except Exception:
                pass
        except Exception as e:
            print(f"ERROR: al mostrar la ventana {clave_ventana}: {e}")
            import traceback; traceback.print_exc()

    def volver_atras(self):
        if len(self.historial) > 0:
            ventana_anterior_key = self.historial.pop()
            if ventana_anterior_key in self.ventanas:
                if self.ventana_actual:
                    try:
                        self.ventana_actual.hide()
                    except Exception:
                        pass
                self.ventana_actual = self.ventanas[ventana_anterior_key]
                try:
                    self.ventana_actual.show()
                    try:
                        self.ventana_actual.raise_()
                        self.ventana_actual.activateWindow()
                    except Exception:
                        pass
                except Exception as e:
                    print(f"ERROR: al mostrar ventana anterior: {e}")
                    import traceback; traceback.print_exc()

    def _obtener_clave_ventana(self, ventana):
        for clave, v in self.ventanas.items():
            if v == ventana:
                return clave
        return None
