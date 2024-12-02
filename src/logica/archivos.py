from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton, QScrollArea
)
from PyQt6.QtCore import Qt


class Archivos:
    def __init__(self, password_list):
        self.password_list = password_list

    def create_files_header(self, parent_window):
        """Crea el encabezado de la sección de archivos."""
        header_layout = QHBoxLayout()

        # Título de la lista de contraseñas
        title = QLabel("Lista de contraseñas")
        title.setStyleSheet("font-size: 18px; color: black;")
        header_layout.addWidget(title)

        # Botón "Añadir contraseña"
        add_button = QPushButton("Añadir contraseña")
        add_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                padding: 5px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        add_button.clicked.connect(parent_window.add_password_window)
        header_layout.addWidget(add_button)

        header_frame = QFrame()
        header_frame.setLayout(header_layout)
        return header_frame

    def update_password_list(self, parent_layout):
        """Actualiza la lista de contraseñas mostradas."""
        # Limpiar el contenido actual
        for i in reversed(range(parent_layout.count())):
            widget = parent_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Crear un QVBoxLayout para agregar la lista
        list_layout = QVBoxLayout()

        # Encabezado de la lista
        headers = ["Red Social", "Correo electrónico", "Categoría", "Fecha de creación", "Acciones"]
        header_layout = QHBoxLayout()
        for header in headers:
            header_label = QLabel(header)
            header_label.setStyleSheet("font-weight: bold; font-size: 14px; padding: 5px; border-bottom: 2px solid black;")
            header_layout.addWidget(header_label)
        list_layout.addLayout(header_layout)

        # Añadir las contraseñas actuales en el layout
        for row, password in enumerate(self.password_list):
            item_layout = QHBoxLayout()

            # Red social
            network_label = QLabel(password["network"])
            network_label.setStyleSheet("font-size: 14px; padding: 5px;")
            item_layout.addWidget(network_label, alignment=Qt.AlignmentFlag.AlignLeft)

            # Correo electrónico
            email_label = QLabel(password["email"])
            email_label.setStyleSheet("font-size: 14px; padding: 5px;")
            item_layout.addWidget(email_label, alignment=Qt.AlignmentFlag.AlignLeft)

            # Categoría
            category_label = QLabel(password["category"])
            category_label.setStyleSheet("font-size: 14px; padding: 5px;")
            item_layout.addWidget(category_label, alignment=Qt.AlignmentFlag.AlignLeft)

            # Fecha de creación
            date_label = QLabel(password["date"])
            date_label.setStyleSheet("font-size: 14px; padding: 5px;")
            item_layout.addWidget(date_label, alignment=Qt.AlignmentFlag.AlignLeft)

            # Acciones (botones)
            action_layout = QVBoxLayout()
            copy_button = QPushButton("Copiar")
            copy_button.clicked.connect(lambda checked, p=password["password"]: parent_layout.parent().copy_to_clipboard(p))
            action_layout.addWidget(copy_button)

            edit_button = QPushButton("Editar")
            edit_button.clicked.connect(lambda checked, i=row: parent_layout.parent().edit_password_window(i))
            action_layout.addWidget(edit_button)

            delete_button = QPushButton("Eliminar")
            delete_button.clicked.connect(lambda checked, i=row: parent_layout.parent().delete_password(i))
            action_layout.addWidget(delete_button)

            # Alinear los botones de acción al centro
            item_layout.addLayout(action_layout)
            list_layout.addLayout(item_layout)

            # Línea horizontal para separar los elementos
            line = QFrame()
            line.setFrameShape(QFrame.Shape.HLine)
            line.setFrameShadow(QFrame.Shadow.Sunken)
            list_layout.addWidget(line)

        # Crear un QWidget para contener la lista completa de contraseñas
        content_widget = QWidget()
        content_widget.setLayout(list_layout)

        # Añadir el widget al layout principal
        scroll_area = QScrollArea()
        scroll_area.setWidget(content_widget)
        scroll_area.setWidgetResizable(True)
        parent_layout.addWidget(scroll_area)
