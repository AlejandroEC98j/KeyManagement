import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configuración principal de la ventana
        self.title("Aplicación GUI con Submenú")
        self.geometry("800x600")

        # Frame para el submenú a la izquierda
        self.sidebar = tk.Frame(self, bg="#2E2E2E", width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        # Frame para el contenido principal
        self.main_content = tk.Frame(self, bg="#FFFFFF")
        self.main_content.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        # Crear botones del submenú
        self.create_sidebar_buttons()

        # Etiqueta de bienvenida por defecto en el contenido principal
        self.content_label = tk.Label(self.main_content, text="Bienvenido a la aplicación", font=("Arial", 16), bg="#FFFFFF")
        self.content_label.pack(pady=20)

    def create_sidebar_buttons(self):
        # Lista de secciones
        sections = ["Archivos", "Categoría", "Generar contraseña", "Ajustes", "Mi perfil"]

        for section in sections:
            button = tk.Button(
                self.sidebar,
                text=section,
                font=("Arial", 12),
                bg="#3E3E3E",
                fg="white",
                relief=tk.FLAT,
                command=lambda s=section: self.display_section(s)
            )
            button.pack(fill=tk.X, pady=5, padx=10)

    def display_section(self, section):
        # Limpia el contenido actual
        for widget in self.main_content.winfo_children():
            widget.destroy()

        # Mostrar el contenido correspondiente a la sección
        if section == "Generar contraseña":
            self.show_password_generator()
        else:
            label = tk.Label(
                self.main_content,
                text=f"Sección: {section}",
                font=("Arial", 16),
                bg="#FFFFFF"
            )
            label.pack(pady=20)

    def show_password_generator(self):
        label = tk.Label(self.main_content, text="Generador de contraseñas", font=("Arial", 16), bg="#FFFFFF")
        label.pack(pady=10)

        password_entry = tk.Entry(self.main_content, font=("Arial", 14))
        password_entry.pack(pady=5)

        generate_button = tk.Button(
            self.main_content,
            text="Generar",
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            command=lambda: self.generate_password(password_entry)
        )
        generate_button.pack(pady=10)

    def generate_password(self, entry):
        import random
        import string

        # Generar una contraseña aleatoria de 12 caracteres
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        entry.delete(0, tk.END)
        entry.insert(0, password)


if __name__ == "__main__":
    app = App()
    app.mainloop()
