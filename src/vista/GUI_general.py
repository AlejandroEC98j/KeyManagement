import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QScrollArea, QComboBox, QSlider, QCheckBox
)
from PyQt6.QtCore import Qt
from datetime import datetime
from src.logica.archivos import ArchivoManager
from src.logica.funciones import generar_contraseña

class App(QWidget):
    def __init__(self):
        super().__init__()

        # Configuración principal de la ventana
        self.setWindowTitle("Gestión de Contraseñas")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #2C3E50; color: white;")  # Fondo oscuro para un tema futurista

        # Instancia del gestor de contraseñas
        self.archivo_manager = ArchivoManager()

        # Layout principal
        layout = QHBoxLayout(self)

        # Sidebar (menú lateral izquierdo)
        self.sidebar = QVBoxLayout()
        self.create_sidebar()
        sidebar_widget = QWidget()
        sidebar_widget.setLayout(self.sidebar)

        # Contenedor principal para las secciones
        self.main_content = QScrollArea()
        self.main_content.setWidgetResizable(True)

        # Añadir un widget vacío con layout por defecto a main_content
        initial_widget = QWidget()
        initial_layout = QVBoxLayout(initial_widget)
        self.main_content.setWidget(initial_widget)

        # Añadir al layout principal
        layout.addWidget(sidebar_widget, 1)
        layout.addWidget(self.main_content, 4)

        # Estado inicial
        self.current_section = None
        self.display_section("Archivos")

    def create_sidebar(self):
        """Crea los botones de la barra lateral."""
        sections = ["Archivos", "Generar contraseña", "Ajustes", "Mi perfil"]
        for section in sections:
            button = QPushButton(section)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #2980B9;
                    color: white;
                    font-size: 16px;
                    padding: 15px;
                    border-radius: 15px;
                    text-align: left;
                    border: 2px solid transparent;
                }
                QPushButton:hover {
                    background-color: #3498DB;
                    border: 2px solid #1ABC9C;
                }
            """)
            button.clicked.connect(lambda checked, s=section: self.display_section(s))
            self.sidebar.addWidget(button)
        self.sidebar.addStretch()

    def display_section(self, section):
        """Muestra la sección seleccionada."""
        if self.current_section == section:
            return
        self.current_section = section

        # Limpiar el contenido actual
        try:
            if self.main_content.widget():
                for i in reversed(range(self.main_content.widget().layout().count())):
                    widget = self.main_content.widget().layout().itemAt(i).widget()
                    if widget:
                        widget.deleteLater()
        except Exception as e:
            print(f"Error al limpiar contenido: {e}")

        # Añadir el nuevo widget de la sección seleccionada
        try:
            if section == "Archivos":
                self.show_archivos()
            elif section == "Generar contraseña":
                self.show_advanced_password_generator()
            elif section == "Ajustes":
                self.show_settings()
            elif section == "Mi perfil":
                self.show_profile()
        except Exception as e:
            print(f"Error al mostrar sección {section}: {e}")

    def show_settings(self):
        """Muestra la sección de ajustes."""
        container = QWidget()
        layout = QVBoxLayout(container)

        title = QLabel("Ajustes")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 22px; color: #ECF0F1; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)

        settings_label = QLabel("Configura las opciones de la aplicación aquí.")
        settings_label.setStyleSheet("font-size: 16px; color: #BDC3C7;")
        layout.addWidget(settings_label)

        self.main_content.setWidget(container)

    def show_profile(self):
        """Muestra la sección de mi perfil."""
        container = QWidget()
        layout = QVBoxLayout(container)

        title = QLabel("Mi Perfil")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 22px; color: #ECF0F1; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)

        profile_label = QLabel("Información del usuario.")
        profile_label.setStyleSheet("font-size: 16px; color: #BDC3C7;")
        layout.addWidget(profile_label)

        self.main_content.setWidget(container)


    def show_archivos(self):
        """Muestra la sección de archivos."""
        container = QWidget()
        layout = QVBoxLayout(container)

        # Encabezado
        header = QHBoxLayout()
        title = QLabel("Lista de contraseñas")
        title.setStyleSheet("font-size: 24px; color: #ECF0F1; font-weight: bold;")
        header.addWidget(title)

        add_button = QPushButton("Añadir contraseña")
        add_button.setStyleSheet("""
            QPushButton {
                background-color: #1ABC9C;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 15px;
                border: 2px solid transparent;
            }
            QPushButton:hover {
                background-color: #16A085;
                border: 2px solid #2980B9;
            }
        """)
        add_button.clicked.connect(self.add_password_window)
        header.addWidget(add_button)
        layout.addLayout(header)

        # Lista de contraseñas
        for idx, password in enumerate(self.archivo_manager.get_passwords()):
            row = QHBoxLayout()
            row.addWidget(QLabel(password["network"]))
            row.addWidget(QLabel(password["email"]))
            row.addWidget(QLabel(password["category"]))
            row.addWidget(QLabel(password["date"]))

            # Botón Copiar
            copy_button = QPushButton("Copiar")
            copy_button.setStyleSheet("""
                QPushButton {
                    background-color: #F39C12;
                    color: white;
                    font-size: 14px;
                    padding: 10px;
                    border-radius: 10px;
                    border: 2px solid transparent;
                }
                QPushButton:hover {
                    background-color: #E67E22;
                }
            """)
            copy_button.clicked.connect(lambda checked, p=password["password"]: self.copy_to_clipboard(p))
            row.addWidget(copy_button)

            # Botón Editar
            edit_button = QPushButton("Editar")
            edit_button.setStyleSheet("""
                QPushButton {
                    background-color: #8E44AD;
                    color: white;
                    font-size: 14px;
                    padding: 10px;
                    border-radius: 10px;
                    border: 2px solid transparent;
                }
                QPushButton:hover {
                    background-color: #9B59B6;
                }
            """)
            edit_button.clicked.connect(lambda checked, i=idx: self.edit_password_window(i))
            row.addWidget(edit_button)

            # Botón Eliminar
            delete_button = QPushButton("Eliminar")
            delete_button.setStyleSheet("""
                QPushButton {
                    background-color: #E74C3C;
                    color: white;
                    font-size: 14px;
                    padding: 10px;
                    border-radius: 10px;
                    border: 2px solid transparent;
                }
                QPushButton:hover {
                    background-color: #C0392B;
                }
            """)
            delete_button.clicked.connect(lambda checked, i=idx: self.delete_password(i))
            row.addWidget(delete_button)

            layout.addLayout(row)

        self.main_content.setWidget(container)

    def add_password_window(self):
        """Ventana para añadir una nueva contraseña."""
        dialog = QWidget()
        dialog.setWindowTitle("Añadir Contraseña")
        dialog.setGeometry(300, 300, 400, 300)

        layout = QVBoxLayout(dialog)

        self.network_input = QLineEdit()
        self.network_input.setStyleSheet("border: 1px solid #BDC3C7; padding: 10px; border-radius: 5px;")
        layout.addWidget(QLabel("Nombre de la red social:"))
        layout.addWidget(self.network_input)

        self.email_input = QLineEdit()
        self.email_input.setStyleSheet("border: 1px solid #BDC3C7; padding: 10px; border-radius: 5px;")
        layout.addWidget(QLabel("Correo electrónico:"))
        layout.addWidget(self.email_input)

        self.category_input = QComboBox()
        self.category_input.addItems(["Trabajo", "Redes sociales", "Bancario"])
        layout.addWidget(QLabel("Categoría:"))
        layout.addWidget(self.category_input)

        self.password_input = QLineEdit()
        self.password_input.setStyleSheet("border: 1px solid #BDC3C7; padding: 10px; border-radius: 5px;")
        layout.addWidget(QLabel("Contraseña:"))
        layout.addWidget(self.password_input)

        add_button = QPushButton("Añadir")
        add_button.setStyleSheet("""
            QPushButton {
                background-color: #1ABC9C;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #16A085;
            }
        """)
        add_button.clicked.connect(lambda: self.add_password(dialog))
        layout.addWidget(add_button)

        dialog.show()

    def add_password(self, dialog):
        """Añade una contraseña y actualiza la lista."""
        self.archivo_manager.add_password(
            self.network_input.text(),
            self.email_input.text(),
            self.category_input.currentText(),
            self.password_input.text()
        )
        dialog.close()
        self.show_archivos()

    def edit_password_window(self, idx):
        """Abre una ventana para editar una contraseña existente."""
        if 0 <= idx < len(self.archivo_manager.get_passwords()):
            password_data = self.archivo_manager.get_passwords()[idx]

            dialog = QWidget()
            dialog.setWindowTitle("Editar Contraseña")
            dialog.setGeometry(300, 300, 400, 300)

            layout = QVBoxLayout(dialog)

            self.network_input = QLineEdit(password_data["network"])
            self.network_input.setStyleSheet("border: 1px solid #BDC3C7; padding: 10px; border-radius: 5px;")
            layout.addWidget(QLabel("Nombre de la red social:"))
            layout.addWidget(self.network_input)

            self.email_input = QLineEdit(password_data["email"])
            self.email_input.setStyleSheet("border: 1px solid #BDC3C7; padding: 10px; border-radius: 5px;")
            layout.addWidget(QLabel("Correo electrónico:"))
            layout.addWidget(self.email_input)

            self.category_input = QComboBox()
            self.category_input.addItems(["Trabajo", "Redes sociales", "Bancario"])
            self.category_input.setCurrentText(password_data["category"])
            layout.addWidget(QLabel("Categoría:"))
            layout.addWidget(self.category_input)

            self.password_input = QLineEdit(password_data["password"])
            self.password_input.setStyleSheet("border: 1px solid #BDC3C7; padding: 10px; border-radius: 5px;")
            layout.addWidget(QLabel("Contraseña:"))
            layout.addWidget(self.password_input)

            save_button = QPushButton("Guardar")
            save_button.setStyleSheet("""
                QPushButton {
                    background-color: #1ABC9C;
                    color: white;
                    font-size: 14px;
                    padding: 10px;
                    border-radius: 15px;
                }
                QPushButton:hover {
                    background-color: #16A085;
                }
            """)
            save_button.clicked.connect(lambda: self.save_edited_password(dialog, idx))
            layout.addWidget(save_button)

            dialog.show()

    def save_edited_password(self, dialog, idx):
        """Guarda los cambios realizados en la contraseña."""
        try:
            # Asegúrate de que el índice sea válido
            if not (0 <= idx < len(self.archivo_manager.get_passwords())):
                print("Índice inválido")
                return

            # Recupera los valores actuales desde los campos de entrada
            updated_password = {
                "network": self.network_input.text(),
                "email": self.email_input.text(),
                "category": self.category_input.currentText(),
                "password": self.password_input.text(),
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

            # Actualiza la contraseña en la lista
            self.archivo_manager.passwords[idx] = updated_password

            # Cierra la ventana de edición
            dialog.close()

            # Refresca la lista en la interfaz principal
            self.show_archivos()
            print("Contraseña actualizada correctamente:", updated_password)
        except Exception as e:
            print("Error al guardar los cambios:", e)

    def delete_password(self, idx):
        """Elimina una contraseña de la lista."""
        try:
            # Verificar que el índice sea válido
            if 0 <= idx < len(self.archivo_manager.get_passwords()):
                self.archivo_manager.delete_password(idx)
                print(f"Contraseña eliminada en el índice {idx}.")
            else:
                print("Índice inválido para eliminación.")

            # Actualizar la interfaz después de eliminar
            self.show_archivos()
        except Exception as e:
            print("Error al eliminar contraseña:", e)

    def show_advanced_password_generator(self):
        """Muestra la sección de generador de contraseñas."""
        container = QWidget()
        layout = QVBoxLayout(container)

        title = QLabel("Generador de Contraseñas")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 22px; color: #ECF0F1; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)

        # Longitud de la contraseña
        length_label = QLabel("Longitud de la contraseña:")
        length_label.setStyleSheet("font-size: 16px; color: #BDC3C7;")
        layout.addWidget(length_label)

        length_slider = QSlider(Qt.Orientation.Horizontal)
        length_slider.setMinimum(12)
        length_slider.setMaximum(20)
        length_slider.setValue(14)
        layout.addWidget(length_slider)

        length_value_label = QLabel("14 caracteres")
        length_value_label.setStyleSheet("font-size: 16px; color: #BDC3C7;")
        layout.addWidget(length_value_label)
        length_slider.valueChanged.connect(lambda: length_value_label.setText(f"{length_slider.value()} caracteres"))

        # Opciones de caracteres
        uppercase_checkbox = QCheckBox("Incluir mayúsculas (A-Z)")
        uppercase_checkbox.setChecked(True)
        uppercase_checkbox.setStyleSheet("color: #BDC3C7;")
        layout.addWidget(uppercase_checkbox)

        lowercase_checkbox = QCheckBox("Incluir minúsculas (a-z)")
        lowercase_checkbox.setChecked(True)
        lowercase_checkbox.setStyleSheet("color: #BDC3C7;")
        layout.addWidget(lowercase_checkbox)

        numbers_checkbox = QCheckBox("Incluir números (0-9)")
        numbers_checkbox.setChecked(True)
        numbers_checkbox.setStyleSheet("color: #BDC3C7;")
        layout.addWidget(numbers_checkbox)

        special_checkbox = QCheckBox("Incluir caracteres especiales (!@#$%^&*)")
        special_checkbox.setChecked(True)
        special_checkbox.setStyleSheet("color: #BDC3C7;")
        layout.addWidget(special_checkbox)

        # Crear los cuadros de texto editables con botones para cantidad mínima de números
        min_numbers_label = QLabel("Cantidad mínima de números:")
        min_numbers_label.setStyleSheet("color: #BDC3C7;")
        layout.addWidget(min_numbers_label)

        min_numbers_input = QLineEdit("1")
        min_numbers_input.setStyleSheet("border: 1px solid #BDC3C7; padding: 5px; border-radius: 5px;")
        layout.addWidget(min_numbers_input)

        # Crear los cuadros de texto editables con botones para cantidad mínima de caracteres especiales
        min_special_label = QLabel("Cantidad mínima de caracteres especiales:")
        min_special_label.setStyleSheet("color: #BDC3C7;")
        layout.addWidget(min_special_label)

        min_special_input = QLineEdit("1")
        min_special_input.setStyleSheet("border: 1px solid #BDC3C7; padding: 5px; border-radius: 5px;")
        layout.addWidget(min_special_input)

        # Campo para mostrar la contraseña generada
        password_display = QLineEdit()
        password_display.setReadOnly(True)
        password_display.setStyleSheet("padding: 10px; font-size: 16px; background-color: #34495E; color: white;")
        layout.addWidget(password_display)

        # Botón para generar la contraseña
        generate_button = QPushButton("Generar Contraseña")
        generate_button.setStyleSheet("""
            QPushButton {
                background-color: #2980B9;
                color: white;
                font-size: 16px;
                padding: 15px;
                border-radius: 10px;
                text-align: left;
                border: 2px solid transparent;
            }
            QPushButton:hover {
                background-color: #3498DB;
            }
        """)
        layout.addWidget(generate_button)

        # Botón de copiar
        copy_button = QPushButton("Copiar")
        copy_button.setStyleSheet("""
               QPushButton {
                   background-color: #F39C12;
                   color: white;
                   font-size: 14px;
                   padding: 10px;
                   border-radius: 10px;
                   border: 2px solid transparent;
               }
               QPushButton:hover {
                   background-color: #E67E22;
               }
           """)

        # Conectar el botón de copiar con el método 'copy_to_clipboard'
        copy_button.clicked.connect(lambda checked: self.copy_to_clipboard(password_display.text()))

        # Agregar el botón a la interfaz
        layout.addWidget(copy_button)

        def generate_password():
            password = generar_contraseña(
                longitud=16,
                incluir_mayusculas=True,
                incluir_minusculas=True,
                incluir_numeros=True,
                incluir_especiales=True,
            )
            password_display.setText(password)

        generate_button.clicked.connect(generate_password)

        self.main_content.setWidget(container)

    def copy_to_clipboard(self, password):
        """Copia la contraseña al portapapeles."""
        QApplication.clipboard().setText(password)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()  # Asegúrate de mostrar la ventana principal
    sys.exit(app.exec())
