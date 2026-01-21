"""
Funciones de validación reutilizables para el sistema.

"""

from datetime import datetime, date

class Validaciones:
    """
    Clase con métodos estáticos para validar datos del sistema.
    
    Todos los métodos retornan True si la validación es exitosa,
    False en caso contrario.
    
    Ejemplo:
        if Validaciones.validar_dni("12345678"):
            print("DNI válido")
    """
    
    # ===== VALIDACIONES DE IDENTIFICACIÓN =====
    
    @staticmethod
    def validar_dni(dni: str) -> bool:
        """
        Valida formato de DNI
        
        El DNI debe de tener exactamente 8 digitos, introducido como string
        
        Args:
            dni (str): String a evaluar
            
        Returns:
            bool: True si el DNI es valido (8 digitos) | False si no lo es 
        
        """

        # Validar que sea un string
        if not isinstance(dni, str):
            return False
        
        # Validar que tenga exactamente 8 digitos
        if len(dni) != 8:
            return False 
        
        # validar que solon sean numeros
        if not dni.isdigit():
            return False
        
        # Paso todos los casos posibles
        return True
    
    @staticmethod
    def validar_telefono(numero_telefono: str) -> bool:
        """
        Valida formato de telefono
        
        El numero de telefono debe de tener 9 digitos empezando por 9, introducido como string
        
        Args:
            numero_telefono (str): String a evaluar
        
        Returns:
            bool: True si cumple con el formato | False si no cumple

        """
        
        # Validar que sea un string
        if not isinstance(numero_telefono, str):
            return False
        
        # Validar que tenga exactamente 9 digitos
        if len(numero_telefono) != 9:
            return False
        
        # Validar que solo tenga numeros
        if not numero_telefono.isdigit():
            return False
        
        # Validar que empieze con 9
        if not numero_telefono.startswith("9"):
            return False
        
        # Paso todos los casos posibles
        return True
    
    @staticmethod
    def validar_nombre(nombre: str, min_length=3, max_length=100) -> bool:
        """
        Valida longitud de nombre
        
        La longitud del nombre debe de ser mayor a 3 y menor que 100 caracteres
        
        Args:
            nombre (str): String a evaluar 
            Por defecto: 
                min_length (int): Longitud minima
                max_length (int): Longitud maxima
        
        Returns:
            bool: True si comple la validacion | False si no cumple        
        
        """    

        # Validar que el nombre sea un string
        if not isinstance(nombre, str):
            return False
        
        # Validar que tenga la longitud necesaria
        nombre_limpio = nombre.strip()
        if len(nombre_limpio) < min_length or len(nombre_limpio) > max_length:
            return False
        
        # Paso con exito los posibles errores
        return True
    
    @staticmethod
    def validar_longitud_minima(texto: str, minimo: int) -> bool:
        """
        Valida longitud de un texto
        
        El texto ingresado no puede ser menor que la cantidad minima permitida
        
        Args:
            texto (str): Texto a evaluar
            minimo (int): Cantidad minima de longitud
        
        Returns:
            bool: True si el texto es mayor a la cantidad | False si no lo es
        
        """
        
        # Validar que sea un string
        if not isinstance(texto, str):
            return False
        
        # Validar longitud y retornar valor
        return len(texto) >= minimo

    # ===== VALIDACIONES DE FECHA =====
    
    @staticmethod
    def validar_fecha(fecha: str, formato="%d/%m/%Y") -> bool:
        """
        Valida el formato de una fecha ingresada
        
        La fecha ingresada debe de ser un string que siga el siguiente formato: 
        dia/mes/ano (%d/%m/%Y)
        eje: 20/01/2026
        
        Args:
            fecha (str): Fecha ingresada como string
            formato (str): Formato que debe de seguir la fecha ingresada
        
        Returns:
            bool: True si cumple con el formato | False si no cumple

        """
    
        # Validar que sea un string
        if not isinstance(fecha, str):
            return False
        
        # Validar que cumpla con el formato solicitado
        try:
            datetime.strptime(fecha, formato)
            return True
        except ValueError:
            return False    
    
    @staticmethod
    def fecha_no_pasada(fecha: date) -> bool:
        """
        Valida fecha
        
        La fecha ingresada (tipo date) no puede ser menor a la fecha actual
        
        Args:
            fecha (date): Fecha (objeto de datetime) a evaluar
        
        Returs:
            bool: True si la fecha no es menor a hoy | False si lo es
        
        """

        # Validar que sea tipo date
        if not isinstance(fecha, date):
            return False
        
        # Validar si cumple y retornar valor
        return fecha >= date.today()
    
    @staticmethod
    def fecha_futura(fecha: date) -> bool:
        """
        Valida fecha
        
        La fecha ingresada (tipo date) debe de ser "mayor" a la actual
        
        Args:
            fecha (date): Fecha a evaluar
        
        Returns:
            bool: True si la fecha es futura | False si no lo es    
        
        """
        
        # Validar que sea tipo date
        if not isinstance(fecha, date):
            return False
        
        # Validar si cumple y retornar valor
        return fecha > date.today()
    
    # ===== VALIDACIONES DE NUMEROS  =====
    
    @staticmethod
    def validar_precio(precio: float) -> bool:
        """
        Valida precio positivo
        
        El valor ingresado no puede ser menor a cero
        
        Args:
            precio (float): Precio a evaluar
        
        Returns:
            bool: True si es mayor a 0 | False si no lo es
        
        """
        
        # Validar que sea float o int
        if not isinstance(precio, (float, int)):
            return False
        
        # Evaluar y retornar valor
        return precio > 0
    
    @staticmethod
    def validar_rango(valor: int, minimo: int, maximo: int) -> bool:
        """
        Valida un rango de numeros
        
        El numero ingresado debe estar en el rango que los extremos (minimo/maximo) indican
        
        Args:
            valor (int): Numero a evaluar
            minimo (int): Numero minimo
            maximo (int): Numero maximo
        
        Returs:
            bool: True si esta en el rango | False si no lo esta
        
        """
        
        # Validar que sean un numeros
        if not all(isinstance(x, int) for x in [valor, minimo, maximo]):
            return False
        
        # Validar rango y retornar valor
        return minimo <= valor <= maximo
    
    # ===== VALIDACIONES DEL MENU =====
    
    @staticmethod
    def validar_opcion_menu(opcion: str, opciones_validas: list) -> bool:
        """
        Valida opcion correcta
        
        La opcion elegida debe de ser valida segun la informacion mostrada
        
        Args:
            opcion (str): Opcion a evaluar
            opciones_validas: Opciones correctas
        
        Returns:
            bool: True si la opcion se encuentra entre las validas | False si no
        
        """
        
        # Validar que sea un string 
        if not isinstance(opcion, str):
            return False
        
        # Validar que sea correcta y retornar valor
        return opcion in opciones_validas