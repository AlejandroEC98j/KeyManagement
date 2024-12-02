import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMessageBox


# Función para mostrar el mensaje al seleccionar una categoría
def mostrar_mensaje(categoria):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Information)
    msg.setWindowTitle("Categoría Seleccionada")
    msg.setText(f"Has seleccionado la categoría: {categoria}")
    msg.exec()


# Crear la clase para la ventana principal
class VentanaCategorias(QWidget):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana
        self.setWindowTitle("Ventana de Categorías")
        self.setGeometry(100, 100, 300, 200)

        # Layout vertical
        layout = QVBoxLayout()

        # Lista de categorías
        categorias = ["Deportes", "Tecnología", "Cultura", "Entretenimiento"]

        # Crear un botón por cada categoría
        for categoria in categorias:
            boton = QPushButton(categoria, self)
            boton.clicked.connect(lambda checked, c=categoria: mostrar_mensaje(c))
            layout.addWidget(boton)

        # Establecer el layout de la ventana
        self.setLayout(layout)


# Crear la aplicación y la ventana
app = QApplication(sys.argv)
ventana = VentanaCategorias()
ventana.show()

# Ejecutar la aplicación
sys.exit(app.exec())