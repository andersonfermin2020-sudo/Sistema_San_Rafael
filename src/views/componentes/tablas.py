"""Funciones encargadas de mostrar tablas dinamicas reutilizables en el sistema"""

from typing import List, Dict, Tuple, Any

class Tablas:
    """
    Componente encargado de renderizar tablas dinámicas en formato ASCII/Unicode.
    Calcula automáticamente los espacios para que las columnas siempre estén alineadas.
    """

    @staticmethod
    def mostrar(titulo: str, configuracion_columnas: List[Tuple[str, str]], datos: List[Dict]):
        """
        Dibuja la tabla en consola.
        
        Args:
            titulo (str): El título superior de la tabla.
            configuracion_columnas (list): Lista de tuplas ("clave_diccionario", "Título Columna").
            datos (list): Lista de diccionarios con los datos a mostrar.
        """
        if not datos:
            print("\n" + "═" * 50)
            print(f"  {titulo}")
            print("  No hay registros para mostrar en este momento.")
            print("═" * 50 + "\n")
            return

        anchos = {}
        for clave, titulo_col in configuracion_columnas:
            # El ancho mínimo es el tamaño del título de la columna
            max_len = len(titulo_col)
            # Revisamos todos los datos para ver si hay un valor más largo
            for fila in datos:
                valor_str = str(fila.get(clave, ""))
                if len(valor_str) > max_len:
                    max_len = len(valor_str)
            anchos[clave] = max_len + 2

        # Calcular el ancho total de la tabla (sumando los separadores '|')
        ancho_total_tabla = sum(anchos.values()) + len(configuracion_columnas) - 1

        print("\n" + "═" * ancho_total_tabla)
        print(f" {titulo} ".center(ancho_total_tabla))
        print("─" * ancho_total_tabla)

        # Encabezados
        fila_encabezados = ""
        for clave, titulo_col in configuracion_columnas:
            fila_encabezados += titulo_col.center(anchos[clave]) + "│"
        print(fila_encabezados[:-1])

        # Línea separadora con cruces (┼)
        linea_separadora = ""
        for clave, _ in configuracion_columnas:
            linea_separadora += "─" * anchos[clave] + "┼"
        print(linea_separadora[:-1])

        # Filas de datos
        for fila in datos:
            fila_str = ""
            for clave, _ in configuracion_columnas:
                valor_str = str(fila.get(clave, ""))
                # Alineamos el texto a la izquierda con ljust()
                fila_str += f" {valor_str.ljust(anchos[clave] - 1)}│"
            print(fila_str[:-1])

        # Borde inferior y Footer
        print("═" * ancho_total_tabla)
        print(f"Total de registros: {len(datos)}\n")

    @staticmethod
    def mostrar_lista_simple(titulo: str, items: List[str]):
        """
        Muestra una lista simple de items.
        
        Args:
            titulo (str): Título de la lista
            items (List[str]): Items a mostrar
        
        Ejemplo:
            mostrar_lista_simple("DEPARTAMENTOS", ["Emergencia", "Pediatría"])
        """
        print("\n" + "═" * 50)
        print(f"{titulo}")
        print("─" * 50)
        for i, item in enumerate(items, 1):
            print(f"{i}. {item}")
        print("═" * 50)

    @staticmethod
    def mostrar_detalle(titulo: str, datos: Dict[str, Any]):
        """
        Muestra detalles de un registro en formato clave-valor.
        
        Args:
            titulo (str): Título del detalle
            datos (Dict[str, Any]): Diccionario con los datos
        
        Ejemplo:
            mostrar_detalle("DATOS DEL PACIENTE", {
                "DNI": "12345678",
                "Nombre": "Juan Pérez",
                "Edad": 35
            })
        """
        print("\n" + "═" * 50)
        print(f"{titulo}")
        print("─" * 50)
        for clave, valor in datos.items():
            print(f"{clave:<20}: {valor}")
        print("═" * 50)