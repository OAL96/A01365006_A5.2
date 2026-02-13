import sys
import json
import time


def archivo_json(archivo_path):
    try:
        with open(archivo_path, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)
            return datos
    except FileNotFoundError:
        print(f"Archivo {archivo_path} no ha sido encontrado.")
        return None
    except json.JSONDecodeError:
        print(f"Archivo {archivo_path} no es un archivo JSON.")
        return None


def convertir_a_diccionario(precios_datos):
    dic_precios = {}

    for objeto in precios_datos:
        try:
            nombre = objeto.get('title')
            precio = objeto.get('price')
            dic_precios[nombre] = precio
        except AttributeError:
            continue

    return dic_precios


def ventas_totales(productos, ventas_datos):

    costo_total = 0.0
    cantidad_total = 0
    dic_ventas = {}
    datos_producto = []
    print("\n--- Calculando Ventas ---")
    for elemento, venta in enumerate(ventas_datos, start=1):
        try:
            producto = venta.get('Product')
            cantidad = abs(venta.get('Quantity'))

            if producto in productos:
                costo = productos[producto] * cantidad
                costo_total += costo
                cantidad_total += cantidad

                if producto in dic_ventas:
                    dic_ventas[producto]['cantidad'] += cantidad
                else:
                    dic_ventas[producto] = {
                        'cantidad': cantidad,
                        'costo': costo_total,
                        'costo_individual': productos[producto]
                    }

            else:
                print(f"Línea {elemento}: Producto '{producto}' no existe.")
        except TypeError:
            print(f"Línea {elemento}: Formato inválido.")

    for producto in dic_ventas:
        datos = dic_ventas[producto]
        cantidad = datos['cantidad']
        total = datos['costo']
        costo_individual = datos['costo_individual']

        linea_producto = (f"{producto:<30} | {cantidad:>8} | "
                          f"${costo_individual:>16.2f} | ${total:>11.2f} |")
        datos_producto.append(linea_producto)

    return costo_total, cantidad_total, datos_producto


inicio = time.time()

if len(sys.argv) != 3:
    print("Uso incorrecto de ejecución: debe ser 'python computeSales.py "
          "A_5.2_Archivos_de_Apoyo/TC1/TC1.ProductList.json "
          "A_5.2_Archivos_de_Apoyo/TC1/TC1.Sales.json'")
    sys.exit(1)

archivo_productos_path = sys.argv[1]
archivo_ventas_path = sys.argv[2]

productos_datos = archivo_json(archivo_productos_path)
ventas_datos = archivo_json(archivo_ventas_path)

if productos_datos is None or ventas_datos is None:
    sys.exit(1)

productos = convertir_a_diccionario(productos_datos)

costo_total, cantidad_total, datos_producto = ventas_totales(productos,
                                                             ventas_datos)

final = time.time()
tiempo_transcurrido = final - inicio

resultados = []
resultados.append("-" * 78)
resultados.append(" " * 37 + "VENTAS")
resultados.append("-" * 78)
resultados.append(f"Total de Unidades Vendidas: {cantidad_total}")
resultados.append("-" * 78)
resultados.append(f"{'PRODUCTO':<30} | {'CANTIDAD':>8} | "
                  f"{'PRECIO INDIVIDUAL':>12} | {'PRECIO TOTAL':>10} |")
resultados.append("-" * 78)
resultados.extend(datos_producto)
resultados.append("-" * 78)
resultados.append(f"Total de Venta: ${costo_total:.2f}")
resultados.append("-" * 78)
resultados.append(f"Tiempo Transcurrido: {tiempo_transcurrido:.6f} segundos")
resultados.append("-" * 78)

salida_datos = "\n".join(resultados)

print("\n" + salida_datos)

try:
    with open("SalesResults.txt", "w", encoding="utf-8") as archivo_resultados:
        archivo_resultados.write(salida_datos)
        print("\nResultados guardados en SalesResults.txt")
except IOError as e:
    print(f"Error al escribir los resultados en el archivo: {e}")
