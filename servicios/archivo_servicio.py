import json
from pathlib import Path
from typing import Any, Callable, Dict, List, TypeVar

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta

CARPETA_DATOS: Path = Path("datos")
RUTA_PRODUCTOS: Path = CARPETA_DATOS / "productos.json"
RUTA_USUARIOS: Path = CARPETA_DATOS / "usuarios.json"
RUTA_VENTAS: Path = CARPETA_DATOS / "ventas.json"

T = TypeVar("T")


class ArchivoServicio:
    """Servicio encargado de la persistencia de productos, usuarios y ventas en JSON."""

    def __init__(
        self,
        ruta_productos: Path = RUTA_PRODUCTOS,
        ruta_usuarios: Path = RUTA_USUARIOS,
        ruta_ventas: Path = RUTA_VENTAS,
    ) -> None:
        self.ruta_productos: Path = ruta_productos
        self.ruta_usuarios: Path = ruta_usuarios
        self.ruta_ventas: Path = ruta_ventas

    # ---------------------- Utilidades genéricas ----------------------

    def _cargar_lista(
        self,
        ruta: Path,
        from_dict: Callable[[Dict[str, Any]], T],
        nombre_entidad: str,
    ) -> List[T]:
        """Lee una lista de diccionarios desde un archivo JSON y reconstruye objetos.

        Controla la ausencia del archivo, un contenido JSON inválido y la
        falta de permisos de lectura, retornando una lista vacía en esos
        casos para no detener la aplicación. Los registros individuales
        inválidos o incompletos se omiten con un aviso.
        """
        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                registros = json.load(archivo)
        except FileNotFoundError:
            print(f"No se encontró un archivo previo de {nombre_entidad}. Se inicia con una colección vacía.")
            return []
        except json.JSONDecodeError:
            print(f"El archivo de {nombre_entidad} tiene un formato inválido. Se inicia con una colección vacía.")
            return []
        except PermissionError:
            print(f"No hay permisos suficientes para leer el archivo de {nombre_entidad}.")
            return []

        objetos: List[T] = []
        for registro in registros:
            try:
                objetos.append(from_dict(registro))
            except KeyError as error:
                print(f"Registro de {nombre_entidad} incompleto omitido (falta la clave {error}).")
            except ValueError as error:
                print(f"Registro de {nombre_entidad} inválido omitido: {error}")

        return objetos

    def _guardar_lista(
        self,
        ruta: Path,
        objetos: List[Any],
        nombre_entidad: str,
    ) -> bool:
        """Guarda una lista de objetos en un archivo JSON.

        Retorna True si el guardado fue exitoso, False si un problema de
        permisos impidió escribir el archivo.
        """
        try:
            ruta.parent.mkdir(parents=True, exist_ok=True)
            datos = [objeto.to_dict() for objeto in objetos]
            with open(ruta, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, ensure_ascii=False, indent=4)
            return True
        except PermissionError:
            print(f"No hay permisos suficientes para guardar el archivo de {nombre_entidad}.")
            return False

    # ---------------------- Productos ----------------------

    def cargar_productos(self) -> List[Producto]:
        return self._cargar_lista(self.ruta_productos, Producto.from_dict, "productos")

    def guardar_productos(self, productos: List[Producto]) -> bool:
        return self._guardar_lista(self.ruta_productos, productos, "productos")

    # ---------------------- Usuarios ----------------------

    def cargar_usuarios(self) -> List[Usuario]:
        return self._cargar_lista(self.ruta_usuarios, Usuario.from_dict, "usuarios")

    def guardar_usuarios(self, usuarios: List[Usuario]) -> bool:
        return self._guardar_lista(self.ruta_usuarios, usuarios, "usuarios")

    # ---------------------- Ventas ----------------------

    def cargar_ventas(self) -> List[Venta]:
        return self._cargar_lista(self.ruta_ventas, Venta.from_dict, "ventas")

    def guardar_ventas(self, ventas: List[Venta]) -> bool:
        return self._guardar_lista(self.ruta_ventas, ventas, "ventas")
