from datetime import datetime
from src.logica.Base_Datos import session, Contraseña, GestorContraseñas

# src/logica/archivos.py
class ArchivoManager:
    def __init__(self):
        self.passwords = []

    def get_passwords(self):
        return self.passwords

    def add_password(self, network, email, category, password):
        from datetime import datetime
        self.passwords.append({
            "network": network,
            "email": email,
            "category": category,
            "password": password,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    def delete_password(self, idx):
        if 0 <= idx < len(self.passwords):
            del self.passwords[idx]
