from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt


class MessageDialog(QDialog):
    def __init__(self, parent=None, title: str = "Mensaje", text: str = "", editable: bool = False,
                 on_save_callback=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(400, 200)

        self._editable = bool(editable)
        self.on_save_callback = on_save_callback
        layout = QVBoxLayout(self)
        self.text_edit = QTextEdit(self)
        self.text_edit.setPlainText(text)

        if self._editable:
            self.text_edit.setReadOnly(False)
        else:
            self.text_edit.setReadOnly(True)
            self.text_edit.setFrameStyle(0)

        layout.addWidget(self.text_edit)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        if self._editable:
            self.btn_save = QPushButton("Guardar", self)
            self.btn_save.clicked.connect(self._on_save)
            btn_layout.addWidget(self.btn_save)

        self.btn_close = QPushButton("Cerrar", self)
        self.btn_close.clicked.connect(self.reject)
        btn_layout.addWidget(self.btn_close)

        layout.addLayout(btn_layout)

    def _on_save(self):
        new_text = self.text_edit.toPlainText()
        if callable(self.on_save_callback):
            try:
                self.on_save_callback(new_text)
            except Exception as e:
                print("Error en on_save_callback:", e)
        self.accept()


class ConfirmDialog(QDialog):
    def __init__(self, parent=None, title="Confirmar acción", text="¿Estás seguro?", on_confirm=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(350, 150)
        self.on_confirm = on_confirm

        layout = QVBoxLayout(self)
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        btn_yes = QPushButton("Sí", self)
        btn_no = QPushButton("No", self)

        btn_yes.clicked.connect(self._confirmar)
        btn_no.clicked.connect(self.reject)

        btn_layout.addWidget(btn_yes)
        btn_layout.addWidget(btn_no)
        layout.addLayout(btn_layout)

    def _confirmar(self):
        if callable(self.on_confirm):
            self.on_confirm()
        self.accept()
