"""Funciones de entrada de datos reutilizables en el sistema"""

from datetime import date, datetime
class Entradas:
    """
    Componente encargado de solicitar datos al usuario de forma segura
    Garantiza que programa no se cierre de golpe por errores de tipeo
    """
    
    @staticmethod
    def pedir_texto(mensaje: str, obligatorio: bool = True) -> str:
        """
        Pide cadeno de texto
        Impide que se dejen campos vacios si es obligatorio
        """
        
        while True:
            valor = input(f"{mensaje}: ").strip()
            if obligatorio and not valor:
                print("  [!] Este campo no puede estar vacío. Intente de nuevo.")
            else:
                return valor
    
    @staticmethod
    def pedir_entero(mensaje: str, min_val: int | None = None, max_val: int | None = None) -> int:
        """Pide un numero entero y valida que no se ingrese letras"""
        
        while True:
            valor = input(f"{mensaje}: ").strip()
            
            try:
                numero = int(valor)
                
                #Validamos rangos si fueron definidos
                if min_val is not None and numero < min_val:
                    print(f"  [!] El número debe ser mayor o igual a {min_val}.")
                    continue
                if max_val is not None and numero > max_val:
                    print(f"  [!] El número debe ser menor o igual a {max_val}.")
                    continue
                
                return numero
            except ValueError:
                print("  [!] Por favor, ingrese un número entero válido (sin letras ni decimales).")
    
    @staticmethod
    def pedir_flotante(mensaje: str, min_val: float | None = None, max_val: float | None = None) -> float:
        """Pide un número decimal con validación de rangos"""
        while True:
            valor = input(f"{mensaje}: ").strip()
            try:
                numero = float(valor.replace(',', '.'))
                
                if min_val is not None and numero < min_val:
                    print(f"  [!] El valor debe ser mayor o igual a {min_val}.")
                    continue
                if max_val is not None and numero > max_val:
                    print(f"  [!] El valor debe ser menor o igual a {max_val}.")
                    continue
                
                return numero
            except ValueError:
                print("  [!] Ingrese un monto numérico válido (ej. 1500.50).")
    
    @staticmethod
    def pedir_fecha(mensaje: str, formato: str = "%d/%m/%Y") -> date:
        """Pide una fecha y verifica que el formato sea correcto (DD/MM/AAAA)."""
        while True:
            valor = input(f"{mensaje} (Formato DD/MM/AAAA): ").strip()
            try:
                # Validamos con el formato
                fecha_obj = datetime.strptime(valor, formato).date()
                
                return fecha_obj
            except ValueError:
                print("  [!] Formato de fecha inválido o fecha inexistente. Use DD/MM/AAAA.")

    @staticmethod
    def pedir_opcion(mensaje: str, opciones_validas: list) -> str:
        """Fuerza al usuario a elegir una opción de una lista específica."""
        # Convertimos las opciones a minúsculas para comparar fácilmente
        opciones_lower = [str(op).lower() for op in opciones_validas]
        opciones_str = "/".join(opciones_validas)
        
        while True:
            valor = input(f"{mensaje} [{opciones_str}]: ").strip()
            if valor.lower() in opciones_lower:
                # Retornamos la opción original (respetando mayúsculas/minúsculas)
                indice = opciones_lower.index(valor.lower())
                return str(opciones_validas[indice])
            else:
                print(f"  [!] Opción inválida. Elija una de las siguientes: {opciones_str}")

    @staticmethod
    def confirmar_accion(mensaje: str = "¿Está seguro?") -> bool:
        """
        Solicita confirmación al usuario (S/N).
        """
        while True:
            respuesta = input(f"\n{mensaje} (S/N): ").strip().upper()
            if respuesta in ('S', 'SI', 'SÍ'):
                return True
            elif respuesta in ('N', 'NO'):
                return False
            else:
                print("  [!] Responda S (Sí) o N (No)")