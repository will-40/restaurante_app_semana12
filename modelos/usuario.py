from typing import Any, Dict


class Usuario:
    """Representa a una persona registrada en el sistema."""

    def __init__(self, identificacion: str, nombre: str, correo: str) -> None:
        if not identificacion or not identificacion.strip():
            raise ValueError("La identificación del usuario no puede estar vacía.")
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del usuario no puede estar vacío.")
        if not correo or not correo.strip():
            raise ValueError("El correo del usuario no puede estar vacío.")
        if "@" not in correo or "." not in correo.split("@")[-1]:
            raise ValueError("El correo del usuario no tiene un formato válido.")

        self.identificacion: str = identificacion.strip()
        self.nombre: str = nombre.strip()
        self.correo: str = correo.strip()

    def to_dict(self) -> Dict[str, Any]:
        """Convierte el usuario a un diccionario compatible con JSON."""
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "correo": self.correo,
        }

    @staticmethod
    def from_dict(datos: Dict[str, Any]) -> "Usuario":
        """Reconstruye un Usuario a partir de un diccionario cargado desde JSON.

        Lanza KeyError si falta alguna clave esperada, y ValueError si algún
        dato recuperado no es válido (delegado al constructor de Usuario).
        """
        return Usuario(
            identificacion=datos["identificacion"],
            nombre=datos["nombre"],
            correo=datos["correo"],
        )

    def __str__(self) -> str:
        return f"[{self.identificacion}] {self.nombre} - {self.correo}"
