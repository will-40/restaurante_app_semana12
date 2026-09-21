# restaurante_app — Semana 12

**Estudiante:** Walter Ortiz
**Asignatura:** Programación Orientada a Objetos
**Actividad:** Tarea Semana 12 — Utilización de colecciones para la mejora de rendimiento

## Descripción del sistema

`restaurante_app` es un sistema de consola para administrar productos, usuarios y ventas de
un restaurante, con control de stock y persistencia en JSON. En esta entrega **no se agregan
funcionalidades nuevas**: se mejora el rendimiento de las búsquedas y consultas más frecuentes
del sistema mediante índices en memoria, manteniendo las listas principales para almacenar,
recorrer y persistir los objetos.

## Estructura del proyecto
restaurante_app/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante.py
├── main.py
└── README.md

## Mejoras de rendimiento aplicadas

Las mejoras se concentraron completamente en `servicios/restaurante.py`, sin tocar `main.py`
ni los modelos, ya que la responsabilidad de optimizar búsquedas y consultas corresponde al
servicio.

### Índices con `dict` para búsquedas por clave

- **`_productos_por_codigo`**: diccionario `código → Producto`. Antes, `buscar_producto()` y
  `existe_producto()` recorrían la lista completa de productos comparando el código uno por
  uno. Ahora acceden directamente por clave (`self._productos_por_codigo.get(codigo)`), sin
  recorrer la lista.
- **`_usuarios_por_identificacion`**: diccionario `identificación → Usuario`, con la misma
  idea aplicada a `buscar_usuario()` y `existe_usuario()`.

Las listas `self.productos` y `self.usuarios` se conservan tal cual, porque siguen siendo
necesarias para listar todos los registros y para la persistencia en JSON.

### Consulta de ventas por usuario agrupada

- **`_ventas_por_usuario`**: diccionario `identificación de usuario → lista de sus Venta`.
  Antes, `consultar_ventas_usuario()` recorría toda la colección de ventas del sistema
  filtrando las que coincidían con el usuario. Ahora se accede directamente a la lista de
  ventas ya agrupadas para ese usuario, sin revisar las ventas de los demás usuarios.

La lista `self._ventas` (todas las ventas, en orden) se mantiene para persistir el archivo
`ventas.json` completo.

### `set` para categorías únicas

Se conserva el uso de `set` en `obtener_categorias()`, que ya se utilizaba desde semanas
anteriores para obtener las categorías de producto sin duplicados; no se agregó ningún `set`
adicional porque no había otra validación de unicidad o pertenencia que lo necesitara.

### Sincronización de los índices

Cada operación que modifica una colección principal actualiza también su índice en el mismo
momento:

- Registrar un producto o usuario agrega la entrada correspondiente al índice.
- Actualizar un producto modifica el mismo objeto que ya está referenciado en el índice (no
  hace falta reescribirlo aparte).
- Eliminar un producto lo quita tanto de la lista como del índice.
- Registrar una venta la agrega a la lista general y a la lista del usuario dentro de
  `_ventas_por_usuario`.

### Reconstrucción al iniciar

Al crear `Restaurante` (justo después de cargar productos, usuarios y ventas desde JSON), el
constructor llama a `_reconstruir_indices()`, que arma los tres índices desde cero a partir de
las listas recién cargadas. Así, los índices siempre quedan coherentes con los datos
recuperados, sin depender de que se hayan ido actualizando durante una ejecución anterior.

## Cómo ejecutar el programa

1. Ubicarse en la carpeta `restaurante_app/`.
2. Ejecutar:
  python main.py
 3. Usar el menú numérico para registrar y administrar productos y usuarios, vender productos,
   consultar las ventas de un usuario y mostrar las categorías registradas (las mismas
   opciones de la Semana 11).

## Pruebas realizadas

1. Se registró un usuario y dos productos, y se comprobó que `buscar_producto()` y
   `buscar_usuario()` (ahora basados en índices) siguen encontrando correctamente los
   registros por su clave.
2. Se realizó una venta y se consultaron las ventas del usuario: la consulta devolvió
   correctamente la venta registrada, usando el índice `_ventas_por_usuario`.
3. Se eliminó uno de los productos y se confirmó que una búsqueda posterior por ese código ya
   no lo encuentra (el índice quedó sincronizado con la eliminación).
4. Se cerró el programa y se volvió a ejecutar: se confirmó que productos, usuarios y ventas
   se recuperaron desde JSON, que los índices se reconstruyeron correctamente
   (`_reconstruir_indices()`), y que las búsquedas y la consulta de ventas por usuario
   siguieron funcionando con normalidad después del reinicio.
