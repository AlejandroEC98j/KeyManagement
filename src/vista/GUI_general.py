import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QSlider, QCheckBox, QLineEdit
)
from PyQt6.QtCore import Qt
import random
import string


class App(QWidget):
    def __init__(self):
        super().__init__()

        # Configuración principal de la ventana
        self.setWindowTitle("Generador de Contraseñas")
        self.setGeometry(100, 100, 800, 600)

        # Layout principal
        layout = QVBoxLayout(self)

        # Frame para el submenú a la izquierda
        self.sidebar = QWidget(self)
        self.sidebar.setStyleSheet("background-color: #2E2E2E;")
        self.sidebar.setFixedWidth(200)
        self.sidebar.setGeometry(0, 0, 200, 600)

        # Frame para el contenido principal
        self.main_content = QWidget(self)
        self.main_content.setStyleSheet("background-color: #FFFFFF;")
        self.main_content.setGeometry(200, 0, 600, 600)

        # Crear botones del submenú
        self.create_sidebar_buttons()

        # Etiqueta de bienvenida por defecto en el contenido principal
        self.content_label = QLabel("Bienvenido a la aplicación", self.main_content)
        self.content_label.setGeometry(50, 20, 500, 40)
        self.content_label.setStyleSheet("font-size: 16px; font-family: Arial; color: black;")

        self.show()

    def create_sidebar_buttons(self):
        # Lista de secciones
        sections = ["Archivos", "Categoría", "Generar contraseña", "Ajustes", "Mi perfil"]

        y_pos = 100  # Posición vertical para los botones
        for section in sections:
            button = QPushButton(section, self.sidebar)
            button.setGeometry(10, y_pos, 180, 40)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #3E3E3E;
                    color: white;
                    font-size: 12px;
                    border: 1px solid #444444;
                    border-radius: 5px;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #4CAF50;
                }
            """)
            button.clicked.connect(lambda checked, s=section: self.display_section(s))
            y_pos += 50

    def display_section(self, section):
        # Limpia el contenido actual
        for widget in self.main_content.findChildren(QWidget):
            widget.deleteLater()

        # Mostrar el contenido correspondiente a la sección
        if section == "Generar contraseña":
            self.show_advanced_password_generator()
        else:
            label = QLabel(f"Sección: {section}", self.main_content)
            label.setStyleSheet("font-size: 16px; font-family: Arial; color: black;")
            label.move(50, 80)
            label.show()

    def show_advanced_password_generator(self):
        # Layout principal del generador de contraseñas
        layout = QVBoxLayout()

        # Título del generador de contraseñas
        title_label = QLabel("Generador de contraseñas")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; color: black; margin-bottom: 20px;")
        layout.addWidget(title_label)

        # Longitud de la contraseña
        length_label = QLabel("Longitud de la contraseña:")
        length_label.setStyleSheet("color: black;")
        layout.addWidget(length_label)

        length_slider = QSlider(Qt.Orientation.Horizontal)
        length_slider.setMinimum(12)
        length_slider.setMaximum(20)
        length_slider.setValue(14)
        layout.addWidget(length_slider)

        length_value_label = QLabel("14 caracteres")
        length_value_label.setStyleSheet("color: black;")
        layout.addWidget(length_value_label)
        length_slider.valueChanged.connect(lambda: length_value_label.setText(f"{length_slider.value()} caracteres"))

        # Opciones de caracteres
        uppercase_checkbox = QCheckBox("Incluir mayúsculas (A-Z)")
        uppercase_checkbox.setChecked(True)
        uppercase_checkbox.setStyleSheet("color: black;")
        layout.addWidget(uppercase_checkbox)

        lowercase_checkbox = QCheckBox("Incluir minúsculas (a-z)")
        lowercase_checkbox.setChecked(True)
        lowercase_checkbox.setStyleSheet("color: black;")
        layout.addWidget(lowercase_checkbox)

        numbers_checkbox = QCheckBox("Incluir números (0-9)")
        numbers_checkbox.setChecked(True)
        numbers_checkbox.setStyleSheet("color: black;")
        layout.addWidget(numbers_checkbox)

        special_checkbox = QCheckBox("Incluir caracteres especiales (!@#$%^&*)")
        special_checkbox.setChecked(True)
        special_checkbox.setStyleSheet("color: black;")
        layout.addWidget(special_checkbox)

        # Crear los cuadros de texto editables con botones para cantidad mínima de números
        min_numbers_label = QLabel("Cantidad mínima de números:")
        min_numbers_label.setStyleSheet("color: black;")
        layout.addWidget(min_numbers_label)

        # Layout para el cuadro de texto editable y botones + y -
        min_numbers_layout = QHBoxLayout()

        min_numbers_edit = QLineEdit("1")
        min_numbers_edit.setStyleSheet("""
            QLineEdit {
                border: 1px solid #444444;
                padding: 5px;
                color: black;
                background-color: white;
                width: 80px;
            }
        """)
        min_numbers_layout.addWidget(min_numbers_edit)

        # Botón para disminuir
        decrement_numbers_button = QPushButton("-")
        decrement_numbers_button.setStyleSheet("""
            QPushButton {
                background-color: #FF6347;
                color: white;
                font-size: 20px;
                padding: 5px;
                width: 30px;
                height: 30px;
                border-radius: 15px;
                border: 1px solid #FF6347;
            }
            QPushButton:hover {
                background-color: #FF4500;
            }
        """)
        decrement_numbers_button.clicked.connect(lambda: self.decrement_value(min_numbers_edit))
        min_numbers_layout.addWidget(decrement_numbers_button)

        # Botón para aumentar
        increment_numbers_button = QPushButton("+")
        increment_numbers_button.setStyleSheet("""
            QPushButton {
                background-color: #32CD32;
                color: white;
                font-size: 20px;
                padding: 5px;
                width: 30px;
                height: 30px;
                border-radius: 15px;
                border: 1px solid #32CD32;
            }
            QPushButton:hover {
                background-color: #228B22;
            }
        """)
        increment_numbers_button.clicked.connect(lambda: self.increment_value(min_numbers_edit))
        min_numbers_layout.addWidget(increment_numbers_button)

        layout.addLayout(min_numbers_layout)

        # Crear los cuadros de texto editables con botones para cantidad mínima de caracteres especiales
        min_special_label = QLabel("Cantidad mínima de caracteres especiales:")
        min_special_label.setStyleSheet("color: black;")
        layout.addWidget(min_special_label)

        # Layout para el cuadro de texto editable y botones + y -
        min_special_layout = QHBoxLayout()

        min_special_edit = QLineEdit("1")
        min_special_edit.setStyleSheet("""
            QLineEdit {
                border: 1px solid #444444;
                padding: 5px;
                color: black;
                background-color: white;
                width: 80px;
            }
        """)
        min_special_layout.addWidget(min_special_edit)

        # Botón para disminuir
        decrement_special_button = QPushButton("-")
        decrement_special_button.setStyleSheet("""
            QPushButton {
                background-color: #FF6347;
                color: white;
                font-size: 20px;
                padding: 5px;
                width: 30px;
                height: 30px;
                border-radius: 15px;
                border: 1px solid #FF6347;
            }
            QPushButton:hover {
                background-color: #FF4500;
            }
        """)
        decrement_special_button.clicked.connect(lambda: self.decrement_value(min_special_edit))
        min_special_layout.addWidget(decrement_special_button)

        # Botón para aumentar
        increment_special_button = QPushButton("+")
        increment_special_button.setStyleSheet("""
            QPushButton {
                background-color: #32CD32;
                color: white;
                font-size: 20px;
                padding: 5px;
                width: 30px;
                height: 30px;
                border-radius: 15px;
                border: 1px solid #32CD32;
            }
            QPushButton:hover {
                background-color: #228B22;
            }
        """)
        increment_special_button.clicked.connect(lambda: self.increment_value(min_special_edit))
        min_special_layout.addWidget(increment_special_button)

        layout.addLayout(min_special_layout)

        # Botón para generar la contraseña
        generate_button = QPushButton("Generar contraseña")
        generate_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        layout.addWidget(generate_button)

        # Campo para mostrar la contraseña generada
        password_display = QLineEdit()
        password_display.setReadOnly(True)
        password_display.setStyleSheet("""
            QLineEdit {
                border: 1px solid #444444;
                padding: 10px;
                color: black;
                background-color: white;
            }
        """)
        layout.addWidget(password_display)

        # Función de generación de contraseña
        def generate_password():
            length = length_slider.value()
            include_uppercase = uppercase_checkbox.isChecked()
            include_lowercase = lowercase_checkbox.isChecked()
            include_numbers = numbers_checkbox.isChecked()
            include_special = special_checkbox.isChecked()
            min_numbers = int(min_numbers_edit.text())
            min_special = int(min_special_edit.text())

            characters = ""
            if include_uppercase:
                characters += string.ascii_uppercase
            if include_lowercase:
                characters += string.ascii_lowercase
            if include_numbers:
                characters += string.digits
            if include_special:
                characters += "!@#$%^&*"

            if not characters:
                password_display.setText("Seleccione al menos una opción")
                return

            password = []
            password.extend(random.choices(string.digits, k=min_numbers))
            password.extend(random.choices("!@#$%^&*", k=min_special))
            remaining_length = length - len(password)
            password.extend(random.choices(characters, k=remaining_length))
            random.shuffle(password)

            password_display.setText("".join(password))

        generate_button.clicked.connect(generate_password)

        # Agregar botón para copiar al portapapeles
        def copy_to_clipboard():
            QApplication.clipboard().setText(password_display.text())

        copy_button = QPushButton("Copiar al portapapeles")
        copy_button.setStyleSheet("""
            QPushButton {
                background-color: #1E90FF;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #4682B4;
            }
        """)
        copy_button.clicked.connect(copy_to_clipboard)
        layout.addWidget(copy_button)

        # Agregar_el_contenido_principal
        self.main_content.setLayout(layout)

    def increment_value(self, edit):
        current_value = int(edit.text())
        edit.setText(str(current_value + 1))

    def decrement_value(self, edit):
        current_value = int(edit.text())
        if current_value > 0:
            edit.setText(str(current_value - 1))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec())
