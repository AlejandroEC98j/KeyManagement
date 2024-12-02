import random
import string


def generar_contraseña(longitud, incluir_mayusculas=True, incluir_minusculas=True, incluir_numeros=True,
                       incluir_especiales=True, min_numeros=1, min_especiales=1):
    """
    Genera una contraseña basada en las configuraciones dadas.

    Args:
        longitud (int): Longitud total de la contraseña.
        incluir_mayusculas (bool): Si debe incluir letras mayúsculas (A-Z).
        incluir_minusculas (bool): Si debe incluir letras minúsculas (a-z).
        incluir_numeros (bool): Si debe incluir números (0-9).
        incluir_especiales (bool): Si debe incluir caracteres especiales (!@#$%^&*).
        min_numeros (int): Mínimo número de dígitos que debe incluir.
        min_especiales (int): Mínimo número de caracteres especiales que debe incluir.

    Returns:
        str: Contraseña generada.
    """
    caracteres = ""
    if incluir_mayusculas:
        caracteres += string.ascii_uppercase
    if incluir_minusculas:
        caracteres += string.ascii_lowercase
    if incluir_numeros:
        caracteres += string.digits
    if incluir_especiales:
        caracteres += "!@#$%^&*"

    if not caracteres:
        return "Seleccione al menos una opción"

    # Generar partes específicas
    contraseña = []
    contraseña.extend(random.choices(string.digits, k=min_numeros))
    contraseña.extend(random.choices("!@#$%^&*", k=min_especiales))

    # Completar la longitud restante
    longitud_restante = longitud - len(contraseña)
    contraseña.extend(random.choices(caracteres, k=longitud_restante))

    # Mezclar la contraseña
    random.shuffle(contraseña)

    return "".join(contraseña)
