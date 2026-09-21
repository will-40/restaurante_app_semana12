from typing import Any, Dict


class Venta:
    """Representa la relación entre un usuario y un producto vendido."""

    def __init__(self, usuario_id: str, producto_codigo: str, cantidad: int) -> None:
        if not usuario_id or not usuario_id.strip():
            raise ValueError("La venta debe tener un usuario asociado.")
        if not producto_codigo or not producto_codigo.strip():
            raise ValueError("La venta debe tener un producto asociado.")
        if cantidad <= 0:
            raise ValueError("La cantidad vendida debe ser mayor que cero.")

        self.usuario_id: str = usuario_id.strip()
        self.producto_codigo: str = producto_codigo.strip()
        self.cantidad: int = int(cantidad)

    def to_dict(self) -> Dict[str, Any]:
        """Convierte la venta a un diccionario compatible con JSON."""
        return {
            "usuario_id": self.usuario_id,
            "producto_codigo": self.producto_codigo,
            "cantidad": self.cantidad,
        }

    @staticmethod
    def from_dict(datos: Dict[str, Any]) -> "Venta":
        """Reconstruye una Venta a partir de un diccionario cargado desde JSON.

        Lanza KeyError si falta alguna clave esperada, y ValueError si algún
        dato recuperado no es válido (delegado al constructor de Venta).
        """
        return Venta(
            usuario_id=datos["usuario_id"],
            producto_codigo=datos["producto_codigo"],
            cantidad=datos["cantidad"],
        )

    def __str__(self) -> str:
        return (
            f"Usuario {self.usuario_id} compró {self.cantidad} "
            f"unidad(es) del producto {self.producto_codigo}"
        )
