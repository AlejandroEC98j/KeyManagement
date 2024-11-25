import unittest
from PyQt6.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QCheckBox, QSlider, QWidget
from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt
from src.vista.GUI_general import App

app = QApplication([])


class TestApp(unittest.TestCase):
    def test_sidebar_buttons(self):
        """Prueba que los botones de la barra lateral cambien de sección."""
        sidebar_buttons = self.window.sidebar.findChildren(QWidget)
        self.assertGreater(len(sidebar_buttons), 0, "No se encontraron botones en la barra lateral")

        # Simula un clic en el botón "Generar contraseña"
        generate_password_button = [btn for btn in sidebar_buttons if btn.text() == "Generar contraseña"]
        self.assertTrue(generate_password_button, "No se encontró el botón 'Generar contraseña'")
        QTest.mouseClick(generate_password_button[0], Qt.MouseButton.LeftButton)

        # Verifica que el contenido cambió a la sección correcta
        main_content_widgets = self.window.main_content.findChildren(QWidget)
        found_label = any(isinstance(w, QLabel) and "Generador de contraseñas" in w.text() for w in main_content_widgets)
        self.assertTrue(found_label, "No se cambió al generador de contraseñas")

    def test_password_generation(self):
        """Prueba que el generador de contraseñas funcione correctamente."""
        # Cambiar a la sección "Generar contraseña"
        self.window.display_section("Generar contraseña")

        # Encuentra los widgets necesarios
        main_content = self.window.main_content.layout()
        slider = main_content.itemAt(1).widget()  # QSlider
        uppercase_checkbox = main_content.itemAt(3).widget()  # QCheckBox
        password_display = main_content.itemAt(12).widget()  # QLineEdit
        generate_button = main_content.itemAt(11).widget()  # QPushButton

        # Configura los valores del generador
        QTest.mouseClick(uppercase_checkbox, Qt.MouseButton.LeftButton)  # Marca "Incluir mayúsculas"
        slider.setValue(16)  # Cambia la longitud de la contraseña a 16

        # Simula un clic en el botón "Generar contraseña"
        QTest.mouseClick(generate_button, Qt.MouseButton.LeftButton)

        # Verifica que se generó una contraseña
        generated_password = password_display.text()
        self.assertEqual(len(generated_password), 16, "La contraseña generada no tiene la longitud esperada")
        self.assertTrue(any(c.isupper() for c in generated_password), "La contraseña no contiene mayúsculas")

    def test_increment_decrement_buttons(self):
        """Prueba los botones de incremento y decremento."""
        # Cambiar a la sección "Generar contraseña"
        self.window.display_section("Generar contraseña")

        # Encuentra el QLineEdit para números mínimos y los botones de incremento/decremento
        main_content = self.window.main_content.layout()
        min_numbers_edit = main_content.itemAt(7).layout().itemAt(0).widget()
        increment_button = main_content.itemAt(7).layout().itemAt(2).widget()
        decrement_button = main_content.itemAt(7).layout().itemAt(1).widget()

        # Verifica el valor inicial
        self.assertEqual(min_numbers_edit.text(), "1", "El valor inicial no es el esperado")

        # Incrementa el valor
        QTest.mouseClick(increment_button, Qt.MouseButton.LeftButton)
        self.assertEqual(min_numbers_edit.text(), "2", "El valor no se incrementó correctamente")

        # Decrementa el valor
        QTest.mouseClick(decrement_button, Qt.MouseButton.LeftButton)
        self.assertEqual(min_numbers_edit.text(), "1", "El valor no se decrementó correctamente")

    def test_copy_to_clipboard(self):
        """Prueba la funcionalidad de copiar contraseña al portapapeles."""
        # Cambiar a la sección "Generar contraseña"
        self.window.display_section("Generar contraseña")

        # Encuentra los widgets necesarios
        main_content = self.window.main_content.layout()
        password_display = main_content.itemAt(12).widget()  # QLineEdit
        copy_button = main_content.itemAt(13).widget()  # QPushButton

        # Establece una contraseña simulada
        password_display.setText("TestPassword123!")

        # Simula un clic en el botón "Copiar al portapapeles"
        QTest.mouseClick(copy_button, Qt.MouseButton.LeftButton)

        # Verifica que la contraseña se copió al portapapeles
        clipboard_text = QApplication.clipboard().text()
        self.assertEqual(clipboard_text, "TestPassword123!", "El portapapeles no contiene la contraseña correcta")


if __name__ == "__main__":
    unittest.main()
