from typing import Callable, Dict, Tuple

from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante import Restaurante

# Tupla: información estable que no cambia durante la ejecución del programa
OPCIONES_MENU: Tuple[str, ...] = (
    "1. Registrar producto",
    "2. Buscar producto",
    "3. Actualizar producto",
    "4. Eliminar producto",
    "5. Listar productos",
    "6. Registrar usuario",
    "7. Listar usuarios",
    "8. Mostrar categorías",
    "9. Vender producto",
    "10. Consultar ventas de un usuario",
    "11. Salir",
)


def mostrar_menu() -> None:
    print("=" * 40)
    print("        SISTEMA DE RESTAURANTE")
    print("=" * 40)
    for opcion in OPCIONES_MENU:
        print(opcion)
    print("-" * 40)


def leer_float(mensaje: str) -> float:
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Valor inválido. Ingrese un número, por ejemplo 4.50.")


def leer_entero(mensaje: str) -> int:
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Valor inválido. Ingrese un número entero, por ejemplo 5.")


def registrar_producto(restaurante: Restaurante, archivo_servicio: ArchivoServicio) -> None:
    codigo = input("Código del producto: ").strip()
    if restaurante.existe_producto(codigo):
        print(f"Ya existe un producto con el código '{codigo}'.")
        return
    nombre = input("Nombre: ").strip()
    categoria = input("Categoría: ").strip()
    precio = leer_float("Precio: ")
    stock = leer_entero("Stock inicial: ")

    try:
        producto = Producto(codigo, nombre, categoria, precio, stock)
    except ValueError as error:
        print(f"No se pudo registrar el producto: {error}")
        return

    if restaurante.registrar_producto(producto):
        archivo_servicio.guardar_productos(restaurante.listar_productos())
        print("Producto registrado y guardado correctamente.")
    else:
        print("No se pudo registrar el producto.")


def buscar_producto(restaurante: Restaurante) -> None:
    codigo = input("Código a buscar: ").strip()
    producto = restaurante.buscar_producto(codigo)
    print(producto if producto else "Producto no encontrado.")


def actualizar_producto(restaurante: Restaurante, archivo_servicio: ArchivoServicio) -> None:
    codigo = input("Código del producto a actualizar: ").strip()
    if restaurante.buscar_producto(codigo) is None:
        print("Producto no encontrado.")
        return
    print("Deje en blanco el campo que no desea modificar.")
    nombre = input("Nuevo nombre: ").strip() or None
    categoria = input("Nueva categoría: ").strip() or None
    precio_str = input("Nuevo precio: ").strip()
    precio = float(precio_str) if precio_str else None
    stock_str = input("Nuevo stock: ").strip()
    stock = int(stock_str) if stock_str else None

    try:
        actualizado = restaurante.actualizar_producto(codigo, nombre, categoria, precio, stock)
    except ValueError as error:
        print(f"No se pudo actualizar el producto: {error}")
        return

    if actualizado:
        archivo_servicio.guardar_productos(restaurante.listar_productos())
        print("Producto actualizado y guardado correctamente.")
    else:
        print("No se pudo actualizar el producto.")


def eliminar_producto(restaurante: Restaurante, archivo_servicio: ArchivoServicio) -> None:
    codigo = input("Código del producto a eliminar: ").strip()
    if restaurante.eliminar_producto(codigo):
        archivo_servicio.guardar_productos(restaurante.listar_productos())
        print("Producto eliminado y guardado correctamente.")
    else:
        print("Producto no encontrado.")


def listar_productos(restaurante: Restaurante) -> None:
    productos = restaurante.listar_productos()
    if not productos:
        print("No hay productos registrados.")
        return
    for producto in productos:
        print(producto)


def registrar_usuario(restaurante: Restaurante, archivo_servicio: ArchivoServicio) -> None:
    identificacion = input("Identificación: ").strip()
    if restaurante.existe_usuario(identificacion):
        print(f"Ya existe un usuario con la identificación '{identificacion}'.")
        return
    nombre = input("Nombre: ").strip()
    correo = input("Correo: ").strip()

    try:
        usuario = Usuario(identificacion, nombre, correo)
    except ValueError as error:
        print(f"No se pudo registrar el usuario: {error}")
        return

    if restaurante.registrar_usuario(usuario):
        archivo_servicio.guardar_usuarios(restaurante.listar_usuarios())
        print("Usuario registrado y guardado correctamente.")
    else:
        print("No se pudo registrar el usuario.")


def listar_usuarios(restaurante: Restaurante) -> None:
    usuarios = restaurante.listar_usuarios()
    if not usuarios:
        print("No hay usuarios registrados.")
        return
    for usuario in usuarios:
        print(usuario)


def mostrar_categorias(restaurante: Restaurante) -> None:
    categorias = restaurante.obtener_categorias()
    if not categorias:
        print("No hay categorías registradas todavía.")
        return
    for categoria in sorted(categorias):
        print(f"- {categoria}")


def vender_producto(restaurante: Restaurante, archivo_servicio: ArchivoServicio) -> None:
    identificacion = input("Identificación del usuario: ").strip()
    codigo = input("Código del producto: ").strip()
    cantidad = leer_entero("Cantidad a vender: ")

    try:
        venta_exitosa = restaurante.vender_producto(codigo, identificacion, cantidad)
    except ValueError as error:
        print(f"No se pudo realizar la venta: {error}")
        return

    if venta_exitosa:
        archivo_servicio.guardar_ventas(restaurante.listar_ventas())
        archivo_servicio.guardar_productos(restaurante.listar_productos())
        print("Venta registrada correctamente.")
    else:
        print("No se pudo realizar la venta (usuario o producto inexistente, cantidad inválida o stock insuficiente).")


def consultar_ventas_usuario(restaurante: Restaurante) -> None:
    identificacion = input("Identificación del usuario: ").strip()
    ventas = restaurante.consultar_ventas_usuario(identificacion)

    if not ventas:
        print("Este usuario no tiene ventas registradas.")
        return

    for venta in ventas:
        producto = restaurante.buscar_producto(venta.producto_codigo)
        nombre_producto = producto.nombre if producto else "producto no encontrado"
        print(f"- {venta.producto_codigo} ({nombre_producto}): {venta.cantidad} unidad(es)")


def salir(
    restaurante: Restaurante,
    archivo_servicio: ArchivoServicio,
) -> None:
    print("Gracias por usar el sistema. ¡Hasta pronto!")


def main() -> None:
    archivo_servicio = ArchivoServicio()
    productos_cargados = archivo_servicio.cargar_productos()
    usuarios_cargados = archivo_servicio.cargar_usuarios()
    ventas_cargadas = archivo_servicio.cargar_ventas()

    restaurante = Restaurante(
        productos_iniciales=productos_cargados,
        usuarios_iniciales=usuarios_cargados,
        ventas_iniciales=ventas_cargadas,
    )

    print(
        f"Se cargaron {len(productos_cargados)} producto(s), "
        f"{len(usuarios_cargados)} usuario(s) y {len(ventas_cargadas)} venta(s)."
    )

    # Diccionario: relación clave (opción del menú) -> valor (función que la resuelve)
    acciones: Dict[str, Callable[[], None]] = {
        "1": lambda: registrar_producto(restaurante, archivo_servicio),
        "2": lambda: buscar_producto(restaurante),
        "3": lambda: actualizar_producto(restaurante, archivo_servicio),
        "4": lambda: eliminar_producto(restaurante, archivo_servicio),
        "5": lambda: listar_productos(restaurante),
        "6": lambda: registrar_usuario(restaurante, archivo_servicio),
        "7": lambda: listar_usuarios(restaurante),
        "8": lambda: mostrar_categorias(restaurante),
        "9": lambda: vender_producto(restaurante, archivo_servicio),
        "10": lambda: consultar_ventas_usuario(restaurante),
    }

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "11":
            salir(restaurante, archivo_servicio)
            break

        accion = acciones.get(opcion)
        if accion is None:
            print("Opción inválida. Intente nuevamente.")
        else:
            accion()

        input("\nPresione Enter para continuar...")


if __name__ == "__main__":
    main()
