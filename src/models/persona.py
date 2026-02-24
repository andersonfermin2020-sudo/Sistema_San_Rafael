"""
Clase abstracta que representa una persona generica
Sirve para la herencia de las clases Personal y Pacientes

"""
from abc import ABC, abstractmethod
from datetime import date
from src.utils.validaciones import Validaciones
from src.utils.helpers import Helpers

class Persona(ABC):
    
    @abstractmethod
    def __init__(self, dni: str, nombre: str, fecha_nacimiento: date, telefono: str):
        """
        Constructor de persona
        
        Args:
            dni (str): DNI de la persona (8 digitos)
            nombre (str): Nombre completo de la persona de la persona
            fecha_nacimiento (date): Fecha de nacimiento 
            telefono (str): Telefono (9 digitos)
            
        Raises:
            ValueError: Si el DNI o la Fecha son invalidas 
        """

        if not Validaciones.validar_dni(dni):
            raise ValueError(f"DNI inválido: {dni}")
        self._dni = dni

        self.nombre = nombre
        
        if not isinstance(fecha_nacimiento, date):
            raise ValueError(f"Fecha invalida: {fecha_nacimiento}. Debe ser un objeto de tipo date")

        if Validaciones.fecha_futura(fecha_nacimiento):
            raise ValueError(f"Fecha invalida: {fecha_nacimiento}. La fecha de nacimiento no puede ser una fecha futura.")
        self._fecha_nacimiento = fecha_nacimiento

        self.telefono = telefono
        
    # Getters (Solo mostrar informacion como variable)
    @property
    def dni(self) -> str:
        return self._dni
        
    @property
    def nombre(self) -> str:
        return self._nombre
        
    @property
    def edad(self) -> int:
        return Helpers.calcular_edad(self._fecha_nacimiento)
        
    @property
    def telefono(self) -> str:
        return self._telefono
        
    # Setters (Modificar atributos como variables)
    @nombre.setter
    def nombre(self, nombre_nuevo: str) -> None:
        if not Validaciones.validar_nombre(nombre_nuevo):
            raise ValueError(f"Nombre invalido: {nombre_nuevo}. Debe tener un rango entre 3 y 100 caracteres.")
        self._nombre = nombre_nuevo
            
    @telefono.setter
    def telefono(self, telefono_nuevo: str) -> None:
        if not Validaciones.validar_telefono(telefono_nuevo):
            raise ValueError(f"Telefono invalido: {telefono_nuevo}. Debe de tener 9 digitos y empezar con 9")
        self._telefono = telefono_nuevo
            
    # Metodos
    def validar_dni(self) -> bool:
            return Validaciones.validar_dni(self._dni)

    def __str__(self) -> str:
        return (f"{self.nombre} (DNI: {self.dni}) - "
                f"Edad: {self.edad} años - Tel: {self.telefono}")
        
    def __repr__(self) -> str:
        """Representación técnica del objeto"""
        return (f"{self.__class__.__name__}(dni='{self._dni}', "
                f"nombre='{self._nombre}', "
                f"fecha_nacimiento={self._fecha_nacimiento}, "
                f"telefono='{self._telefono}')")