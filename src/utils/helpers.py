"""
Funciones auxiliares generales

"""

import os
from datetime import datetime, date
from typing import List, Dict

class Helpers:
    
    @staticmethod
    def limpiar_pantalla():
        """Limpia la pantalla de la consola"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def pausar():
        """Pausa la ejecucion esperando un Enter"""
        input("\nPresion Enter para continuar...")
    
    @staticmethod
    def formatear_fecha(fecha: date, formato="%d/%m/%Y") -> str:
        """
        Convierte objeto date a string
        
        Args:
            fecha: Objeto date
            formato: Formato deseado
            
        Returns:
            str: Fecha formateada 
        
        """
        
        return fecha.strftime(formato)
    
    @staticmethod 
    def parsear_fecha(fecha_str: str, formato="%d/%m/%Y") -> date:
        """
        Convierte string a objeto date
        
        Args:
            fecha_str: String con fecha
            formato: Formato del string
            
        Returns:
            date: Objeto date   
            
        """
        return datetime.strptime(fecha_str, formato).date()
    
    @staticmethod
    def calcular_edad(fecha_nacimiento: date) -> int:
        """
        Calcular edad a partir de fecha de nacimiento
        
        Args:
            fecha_nacimiento: Fecha de nacimiento
        
        Returns:
            int: Edad en anios
        
        """
        hoy = date.today()
        edad = hoy.year - fecha_nacimiento.year
        
        if (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
            edad -= 1
            
        return edad
    
    @staticmethod
    def formatear_precio(precio: float) -> str:
        """
        Formatear un precio con 2 decimales y separador de miles.
        
        Args:
            precio: Numero a formatear
        
        Returns:
            str: Precio formateado
        
        """
        
        return f"S/. {precio:,.2f}"
    
    @staticmethod
    def formatear_tabla(datos:List[Dict], columnas: List[str],
                        titulos: List[str] | None = None) -> str:
        
        """
        Formatear una lista de diccionarios como tabla ASCII
        
        Args:
            datos: Lista de diccionarios
            columnas: Nombres de las claves a mostrar
            titulos: Titulos de las columnas (si None, usa las claves)
            
        Returns:
            str: Tabla formateada
        
        """
        if not datos:
            return "No hay datos para mostrar"
        
        if titulos is None:
            titulos = columnas
            
        anchos = []
        for i, col in enumerate(columnas):
            ancho_titulo = len(titulos[i])
            ancho_maximo_dato = max([len(str(registro.get(col, ""))) for registro in datos])
            
            anchos.append(max(ancho_titulo, ancho_maximo_dato))
            
        # Construir tabla
        linea_sep = '--' * sum(anchos) + "--" * (len(columnas) * 3-1)
        tabla = []
        tabla.append("=" * len(linea_sep))
    
        # Encabezados
        encabezado = " | ".join([titulos[i].ljust(anchos[i]) for i in range(len(titulos))])
        tabla.append(encabezado)
        tabla.append(linea_sep)
        
        # Datos
        for registro in datos:
            fila = " | ".join([str(registro.get(col, "")).ljust(anchos[i]) for i, col in enumerate(columnas)])
            tabla.append(fila)
        
        tabla.append("═" * len(linea_sep))
        
        return "\n".join(tabla)
    
    @staticmethod
    def confirmar_accion(mensaje: str = "¿Está seguro?") -> bool:
        """
        Solicita confirmacion de usuario
        
        Args:
            mensaje: Mensaje a mostrar
        
        Returns:
            bool: True si el usuario confirma
        
        """
        respuesta = input(f"{mensaje} (S/N): ").strip().upper()
        return respuesta == "S"
    
    @staticmethod
    def dias_entre_fechas(fecha1: date, fecha2: date) -> int:
        """
        Calcula el numero de dias entre dos fechas
        
        Args:
            fecha1, fecha2: Fechas 
            
        Returns:
            int: Numero de dias entre las fechas ingresadas (positivo o negativo)
        
        """
        
        return (fecha2 - fecha1).days