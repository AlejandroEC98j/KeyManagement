from cryptography.fernet import Fernet


class LogArchivos:
    def __init__(self):
        # Clave de encriptación (se debe guardar de forma segura en un entorno real)
        self.key = Fernet.generate_key()  # Cambiar por una clave fija si es necesario
        self.cipher = Fernet(self.key)

        # Simulación de almacenamiento en memoria (reemplazar con base de datos en proyectos reales)
        self.passwords = []

    def encrypt_password(self, password: str) -> str:
        """Encripta una contraseña."""
        encrypted = self.cipher.encrypt(password.encode())
        return encrypted.decode()

    def decrypt_password(self, encrypted_password: str) -> str:
        """Desencripta una contraseña."""
        decrypted = self.cipher.decrypt(encrypted_password.encode())
        return decrypted.decode()

    def add_password(self, name: str, description: str, password: str):
        """Agrega una nueva contraseña al almacenamiento."""
        encrypted_password = self.encrypt_password(password)
        self.passwords.append({
            "name": name,
            "description": description,
            "password": encrypted_password
        })

    def update_password(self, old_name: str, new_name: str, new_description: str, new_password: str):
        """Actualiza una contraseña existente."""
        for entry in self.passwords:
            if entry["name"] == old_name:
                entry["name"] = new_name
                entry["description"] = new_description
                entry["password"] = self.encrypt_password(new_password)
                break

    def delete_password(self, name: str):
        """Elimina una contraseña por su nombre."""
        self.passwords = [entry for entry in self.passwords if entry["name"] != name]

    def get_all_passwords(self):
        """Obtiene todas las contraseñas desencriptadas para mostrarlas."""
        result = []
        for entry in self.passwords:
            result.append((
                entry["name"],
                entry["description"],
                self.decrypt_password(entry["password"])
            ))
        return result
