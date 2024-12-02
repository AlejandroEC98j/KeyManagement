from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox, QLabel, QLineEdit
from src.logica.Base_Datos import session, GestorContraseñas

class CategoriaManager(QWidget):
    def __init__(self, archivo_manager, update_category_callback):
        super().__init__()
        self.archivo_manager = archivo_manager
        self.update_category_callback = update_category_callback
        self.categorias = self.get_categories()  # Obtener categorías de la base de datos
        self.init_ui()

    def get_categories(self):
        """Recuperar las categorías de contraseñas del gestor de contraseñas asociado al usuario."""
        return [gestor.Nombre_Gestor for gestor in session.query(GestorContraseñas).filter(GestorContraseñas.ID_Usuario == self.archivo_manager.user_id).all()]

    def init_ui(self):
        """Inicializa los botones de las categorías y el botón para añadir una nueva categoría."""
        layout = QVBoxLayout(self)

        # Botones para cada categoría
        for category in self.categorias:
            button = QPushButton(category, self)
            button.clicked.connect(lambda checked, c=category: self.filter_by_category(c))
            layout.addWidget(button)

        # Botón para añadir una nueva categoría
        add_category_button = QPushButton("Añadir categoría", self)
        add_category_button.clicked.connect(self.add_category_window)
        layout.addWidget(add_category_button)

    def filter_by_category(self, category):
        """Filtra las contraseñas mostradas según la categoría seleccionada."""
        self.archivo_manager.get_passwords_by_category(category)

    def add_category_window(self):
        """Ventana para añadir una nueva categoría."""
        dialog = QWidget(self)
        dialog.setWindowTitle("Añadir categoría")
        dialog.setGeometry(300, 300, 400, 150)

        layout = QVBoxLayout(dialog)

        self.category_input = QLineEdit()
        layout.addWidget(QLabel("Nombre de la categoría:"))
        layout.addWidget(self.category_input)

        add_button = QPushButton("Añadir", dialog)
        add_button.clicked.connect(self.add_category)
        layout.addWidget(add_button)

        dialog.show()

    def add_category(self):
        """Añadir una nueva categoría a la base de datos."""
        category_name = self.category_input.text()
        gestor = GestorContraseñas(ID_Usuario=self.archivo_manager.user_id, Nombre_Gestor=category_name)
        session.add(gestor)
        session.commit()
        self.update_category_callback(category_name)  # Actualizar el ComboBox en GUI
