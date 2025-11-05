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
        # DEBUG: ver a qué ventana se intenta navegar
        print(f"NavigationManager: navegar a clave='{clave_ventana}', clase={ventana_class.__name__}")

        # Guardar en historial la clave de la ventana actual
        if self.ventana_actual:
            ventana_actual_key = self._obtener_clave_ventana(self.ventana_actual)
            if ventana_actual_key:
                self.historial.append(ventana_actual_key)
            # ocultar la ventana actual antes de crear/mostrar la nueva
            try:
                self.ventana_actual.hide()
            except Exception:
                pass

        # Crear (o reutilizar) la instancia de la ventana solicitada
        if clave_ventana not in self.ventanas:
            try:
                print(f"NavigationManager: creando instancia de {ventana_class.__name__}")
                self.ventanas[clave_ventana] = ventana_class(*args, **kwargs)
            except Exception as e:
                import traceback
                print(f"ERROR: al crear {ventana_class.__name__}: {e}")
                traceback.print_exc()
                return  # salir sin cambiar ventana_actual si falla la creación
        else:
            print(f"NavigationManager: reutilizando instancia de {ventana_class.__name__}")

        # Mostrar y activar la ventana
        self.ventana_actual = self.ventanas[clave_ventana]
        try:
            self.ventana_actual.show()
            # forzar que la ventana aparezca por encima y reciba foco
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
