from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton

class ConfirmDialog(QDialog):
    def __init__(self, parent=None, title="Confirmar", text="¿Estás seguro?", on_confirm=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(350, 150)
        self.on_confirm = on_confirm

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(text, self))

        button_layout = QHBoxLayout()
        btn_yes = QPushButton("Sí", self)
        btn_no = QPushButton("No", self)
        button_layout.addWidget(btn_yes)
        button_layout.addWidget(btn_no)
        layout.addLayout(button_layout)

        btn_yes.clicked.connect(self.confirm)
        btn_no.clicked.connect(self.reject)

    def confirm(self):
        if callable(self.on_confirm):
            self.on_confirm()
        self.accept()
