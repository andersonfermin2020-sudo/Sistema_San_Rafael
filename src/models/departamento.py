"""
Representa un departamento del hospital

"""
from typing import List, Dict, Any
from utils.excepciones import ValidationException, EstadoInvalidoException
from utils.validaciones import Validaciones

class Departamento:
    def __init__(self, id_departamento: int, nombre: str, descripcion: str | None, id_jefe: int, personal_asignado: List[int]):
        """
        Construtor de Departamento
        
        Args:
            id_departamento (int): ID unico del departamento
            nombre (str): Nombre del departamento
            descripcion (str | None): (Opcional) Descripcion del departamento
            id_jefe (int): ID del personal asignado como jefe de departamento
            personal_asignado (List[int]): Lista con los IDs del personal asignado al departamento
            
        Raises:
            ValidationException: Formato o estado de datos incorrectos
        """
        
        # ========== Validaciones ==========
        
        # ID del departamento
        if not isinstance(id_departamento, int) or id_departamento <= 0:
            raise ValidationException(f"Error de formato del ID del departamento {id_departamento}. Debe ser un numero entero positivo")
        
        # Nombre
        if not Validaciones.validar_longitud_minima(nombre.strip(), 5):
            raise ValidationException(f"Error de formato del nombre del departamento. Debe ser mayor a 4 caracteres")
        
        # Descripcion
        if descripcion is not None:
            if not Validaciones.validar_longitud_minima(descripcion.strip(), 10):
                raise ValidationException(f"Error de formato de la descripcion. Debe ser mayor a 10 caracteres.")
            
        # ID de jefe
        if not isinstance(id_jefe, int) or id_jefe <= 0:
            raise ValidationException(f"Error de formato del ID del jefe de departamento {id_jefe}. Debe ser un numero entero positivo")
        
        # Personal asignado
        if not isinstance(personal_asignado, list) or len(personal_asignado) == 0:
            raise ValidationException(f"Error de formato de personal asignado. Debe ser una lista con (al menos) un personal asignado.")
        
        if not all(isinstance(personal, int) and personal > 0 for personal in personal_asignado):
            raise ValidationException("Los IDs del personal deben ser enteros positivos")
        
        # Validacion logica: El jefe inicial DEBE estar en la lista de personal
        if id_jefe not in personal_asignado:
            raise ValidationException(f"Inconsistencia: El jefe designado (ID {id_jefe}) debe estar incluido en la lista de personal asignado.")
        
        # ========== Asignacion ==========
        
        self._id_departamento = id_departamento
        self._nombre = nombre.strip().capitalize()
        self._descripcion = descripcion.strip().capitalize() if descripcion else None
        self._id_jefe = id_jefe
        self._personal_asignado = personal_asignado.copy()


    # ========== Getters ==========
    
    @property
    def id_departamento(self) -> int:
        return self._id_departamento
    
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @property
    def descripcion(self) -> str | None:
        return self._descripcion
    
    @property
    def id_jefe(self) -> int:
        return self._id_jefe
    
    @property
    def personal_asignado(self) -> List[int]:
        return self._personal_asignado.copy()
    
    # ========== Metodos ==========
    
    def asignar_jefe(self, id_personal: int) -> None:
        """
        Asigna un personal como jefe al departamento
        
        Args:
            id_personal (int): ID del personal a asignar
        
        Raises:
            ValidationException: Formato de ID incorrecto
            EstadoInvalidoException: 
                El personal no esta registrado en el departamento
                El personal ya se encuentra asignado
        """
        
        # ========== Validaciones ==========
        
        # ID del personal
        if not isinstance(id_personal, int) or id_personal <= 0:
            raise ValidationException(f"El ID del personal debe ser un numero entero positivo")
        
        # Personal no registrado
        if not id_personal in self._personal_asignado:
            raise EstadoInvalidoException(f"No se puede asignar como jefe al personal {id_personal}. Debe de estar registrado en el departamento primero")
        
        # El personal ya se encuentra asignado
        if self._id_jefe == id_personal:
            raise EstadoInvalidoException(f"El personal con ID {id_personal} ya se encuentra asignado como jefe de departamento")
        
        # ========== Asignacion ==========
        self._id_jefe = id_personal
    
    def agregar_personal(self, id_personal: int) -> None:
        """
        Agrega personal al departamento
        
        Args:
            id_personal (int): ID del personal
        
        Raises:
            ValidationException: Formato invalido del ID
            EstadoInvalidoException: Personal ya registrado
        """
        
        # ========== Validaciones ==========
        
        # ID del personal
        if not isinstance(id_personal, int) or id_personal <= 0:
            raise ValidationException("El ID del personal debe ser un numero entero positivo")
        
        # Personal ya esta registrado
        personal_registrado = id_personal in self._personal_asignado
        
        if personal_registrado:
            raise EstadoInvalidoException(f"Error: El personal con ID {id_personal} ya se encuentra registrado en el departamento {self._nombre}")
        
        # ========== Agregar ==========
        self._personal_asignado.append(id_personal)

    def remover_personal(self, id_personal: int) -> None:
        """
        Remueve personal de un departamento
        
        Args:
            id_personal (int): ID del personal
            
        Raises:
            ValidationException: Formato de ID invalido
            EstadoInvalidoException: 
                El personal no se encuentra registrado 
                El departamento queda sin personal   
                Tratar de eliminar al jefe del departamento                
        """
        
        # ========== Validaciones ==========
        
        # ID del personal
        if not isinstance(id_personal, int) or id_personal <= 0:
            raise ValidationException("El ID del personal debe ser un numero entero positivo")
        
        # Personal no encontrado
        personal_encontrado = id_personal in self._personal_asignado
        
        if not personal_encontrado:
            raise EstadoInvalidoException(f"Error: El personal con ID {id_personal} no se encuentra asignado al departamento {self._nombre}")
        
        # Departamento sin personal
        if personal_encontrado and len(self._personal_asignado) == 1:
            raise EstadoInvalidoException(f"No se puede remover el personal con ID. El departamento no puede quedar sin personal")
        
        # Eliminar jefe de departamento
        if id_personal == self._id_jefe:
            raise EstadoInvalidoException(f"Error: No se puede eliminar al jefe del departamento - ID {id_personal}. Para quitarle su cargo debe cambiarlo por otro personal")
        
        # ========== Remover ==========
        self._personal_asignado.remove(id_personal)

    def obtener_cantidad_personal(self) -> int:
        """Retorna la cantidad del personal asignado al departamento"""
        
        return len(self._personal_asignado)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte un objeto Departamento a un diccionario para serializacion JSON
        
        Returns:
            dict: Objeto representado en forma de diccionario
        """
        
        return {
            "id_departamento": self._id_departamento,
            "nombre": self._nombre,
            "descripcion": self._descripcion,
            "id_jefe": self._id_jefe,
            "personal_asignado": self._personal_asignado.copy()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Departamento':
        """
        Reconstruye un objeto Departamento a traves de un archivo JSON
        
        Args:
            data (Dict[int, Any]): Datos del objeto en forma de diccionario
        
        Returns:
            Departamento: Objeto Departamento reconstruido
        
        Raises:
            ValueError: Si faltan datos o si son invalidos
        """
        
        try:
            return cls(
                id_departamento=data["id_departamento"],
                nombre=data["nombre"],
                descripcion=data.get("descripcion"),
                id_jefe=data["id_jefe"],
                personal_asignado=data["personal_asignado"]
            )
        except KeyError as e:
            raise ValueError(f"Falta el campo requerido: {e}")
        except Exception as e:
            raise ValueError(f"Error al deserializar Departamento: {e}")