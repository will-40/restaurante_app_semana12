from typing import Any, Dict


class Producto:
    """Representa un producto disponible en el restaurante, con su stock."""

    def __init__(
        self,
        codigo: str,
        nombre: str,
        categoria: str,
        precio: float,
        stock: int = 0,
    ) -> None:
        if not codigo or not codigo.strip():
            raise ValueError("El código del producto no puede estar vacío.")
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")
        if not categoria or not categoria.strip():
            raise ValueError("La categoría del producto no puede estar vacía.")
        if precio < 0:
            raise ValueError("El precio del producto no puede ser negativo.")
        if stock < 0:
            raise ValueError("El stock del producto no puede ser negativo.")

        self.codigo: str = codigo.strip()
        self.nombre: str = nombre.strip()
        self.categoria: str = categoria.strip()
        self.precio: float = float(precio)
        self.stock: int = int(stock)

    def vender(self, cantidad: int) -> None:
        """Disminuye el stock disponible tras una venta válida.

        Se asume que la cantidad ya fue validada (mayor que cero y no mayor
        al stock disponible) por quien llama a este método.
        """
        if cantidad <= 0:
            raise ValueError("La cantidad a vender debe ser mayor que cero.")
        if cantidad > self.stock:
            raise ValueError("No hay stock suficiente para realizar la venta.")
        self.stock -= cantidad

    def to_dict(self) -> Dict[str, Any]:
        """Convierte el producto a un diccionario compatible con JSON."""
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
            "stock": self.stock,
        }

    @staticmethod
    def from_dict(datos: Dict[str, Any]) -> "Producto":
        """Reconstruye un Producto a partir de un diccionario cargado desde JSON.

        Lanza KeyError si falta alguna clave esperada, y ValueError si algún
        dato recuperado no es válido (delegado al constructor de Producto).
        El campo "stock" es opcional para compatibilidad con registros de
        semanas anteriores; si no está presente, se asume 0.
        """
        return Producto(
            codigo=datos["codigo"],
            nombre=datos["nombre"],
            categoria=datos["categoria"],
            precio=datos["precio"],
            stock=datos.get("stock", 0),
        )

    def __str__(self) -> str:
        return (
            f"[{self.codigo}] {self.nombre} - {self.categoria} - "
            f"${self.precio:.2f} - Stock: {self.stock}"
        )
