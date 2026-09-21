from typing import Dict, List, Optional, Set

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class Restaurante:
    """Servicio encargado de administrar las colecciones y las reglas de negocio.

    Las listas (`productos`, `usuarios`, `_ventas`) siguen siendo la fuente de
    verdad: se usan para recorrer, listar y persistir los objetos. Junto a
    ellas se mantienen índices con diccionarios para las búsquedas por clave
    que se realizan con frecuencia (código de producto, identificación de
    usuario, ventas agrupadas por usuario), evitando recorrer la lista
    completa cada vez. Los índices se actualizan en cada operación que
    registra, modifica o elimina datos, y se reconstruyen por completo al
    iniciar el programa a partir de lo recuperado desde JSON.
    """

    def __init__(
        self,
        productos_iniciales: Optional[List[Producto]] = None,
        usuarios_iniciales: Optional[List[Usuario]] = None,
        ventas_iniciales: Optional[List[Venta]] = None,
    ) -> None:
        # Listas: colecciones principales para almacenar, recorrer y persistir objetos
        self.productos: List[Producto] = list(productos_iniciales) if productos_iniciales else []
        self.usuarios: List[Usuario] = list(usuarios_iniciales) if usuarios_iniciales else []
        self._ventas: List[Venta] = list(ventas_iniciales) if ventas_iniciales else []

        # Índices (dict): búsqueda directa por clave, sin recorrer la lista completa
        self._productos_por_codigo: Dict[str, Producto] = {}
        self._usuarios_por_identificacion: Dict[str, Usuario] = {}
        self._ventas_por_usuario: Dict[str, List[Venta]] = {}

        self._reconstruir_indices()

    def _reconstruir_indices(self) -> None:
        """Reconstruye todos los índices a partir de las listas principales.

        Se llama al iniciar el servicio (por ejemplo, tras cargar los datos
        desde JSON) para que los índices queden coherentes con las listas.
        """
        self._productos_por_codigo = {producto.codigo: producto for producto in self.productos}
        self._usuarios_por_identificacion = {usuario.identificacion: usuario for usuario in self.usuarios}

        self._ventas_por_usuario = {}
        for venta in self._ventas:
            self._ventas_por_usuario.setdefault(venta.usuario_id, []).append(venta)

    # ---------------------- Productos ----------------------

    def existe_producto(self, codigo: str) -> bool:
        # Antes: recorrer toda la lista comparando código uno a uno.
        # Ahora: pertenencia directa en el índice, en tiempo constante.
        return codigo in self._productos_por_codigo

    def registrar_producto(self, producto: Producto) -> bool:
        if self.existe_producto(producto.codigo):
            return False
        self.productos.append(producto)
        self._productos_por_codigo[producto.codigo] = producto
        return True

    def buscar_producto(self, codigo: str) -> Optional[Producto]:
        # Antes: recorrer la lista completa hasta encontrar el código.
        # Ahora: acceso directo por clave en el índice de productos.
        return self._productos_por_codigo.get(codigo)

    def actualizar_producto(
        self,
        codigo: str,
        nombre: Optional[str] = None,
        categoria: Optional[str] = None,
        precio: Optional[float] = None,
        stock: Optional[int] = None,
    ) -> bool:
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False
        if nombre:
            producto.nombre = nombre
        if categoria:
            producto.categoria = categoria
        if precio is not None:
            producto.precio = precio
        if stock is not None:
            if stock < 0:
                raise ValueError("El stock del producto no puede ser negativo.")
            producto.stock = stock
        # El objeto en la lista y en el índice es el mismo, así que ambos
        # quedan actualizados automáticamente al modificar sus atributos.
        return True

    def eliminar_producto(self, codigo: str) -> bool:
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False
        self.productos.remove(producto)
        del self._productos_por_codigo[codigo]
        return True

    def listar_productos(self) -> List[Producto]:
        return list(self.productos)

    def obtener_categorias(self) -> Set[str]:
        # Conjunto: elimina automáticamente categorías repetidas
        return {producto.categoria for producto in self.productos}

    # ---------------------- Usuarios ----------------------

    def existe_usuario(self, identificacion: str) -> bool:
        # Pertenencia directa en el índice de usuarios, en tiempo constante.
        return identificacion in self._usuarios_por_identificacion

    def registrar_usuario(self, usuario: Usuario) -> bool:
        if self.existe_usuario(usuario.identificacion):
            return False
        self.usuarios.append(usuario)
        self._usuarios_por_identificacion[usuario.identificacion] = usuario
        return True

    def buscar_usuario(self, identificacion: str) -> Optional[Usuario]:
        # Antes: recorrer la lista completa hasta encontrar la identificación.
        # Ahora: acceso directo por clave en el índice de usuarios.
        return self._usuarios_por_identificacion.get(identificacion)

    def listar_usuarios(self) -> List[Usuario]:
        return list(self.usuarios)

    # ---------------------- Ventas ----------------------

    def vender_producto(self, codigo_producto: str, identificacion_usuario: str, cantidad: int) -> bool:
        """Registra la venta de un producto a un usuario, si es válida.

        Comprueba que el usuario y el producto existan, que la cantidad sea
        mayor que cero y que exista stock suficiente. Si todo es válido,
        crea la Venta, la agrega a la colección y al índice por usuario, y
        disminuye el stock.
        """
        usuario = self.buscar_usuario(identificacion_usuario)
        producto = self.buscar_producto(codigo_producto)

        if usuario is None or producto is None:
            return False

        if cantidad <= 0 or producto.stock < cantidad:
            return False

        venta = Venta(usuario.identificacion, producto.codigo, cantidad)
        self._ventas.append(venta)
        self._ventas_por_usuario.setdefault(venta.usuario_id, []).append(venta)
        producto.vender(cantidad)
        return True

    def listar_ventas(self) -> List[Venta]:
        return list(self._ventas)

    def consultar_ventas_usuario(self, identificacion_usuario: str) -> List[Venta]:
        # Antes: recorrer toda la colección de ventas comparando el usuario
        # en cada una. Ahora: acceso directo a la lista de ventas ya
        # agrupadas por usuario en el índice, sin recorrer las demás ventas.
        return list(self._ventas_por_usuario.get(identificacion_usuario, []))
