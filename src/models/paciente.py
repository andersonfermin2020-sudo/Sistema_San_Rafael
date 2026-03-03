"""
Representa un paciente del Hospital
Hereda de persona
"""
from datetime import date
from src.models.persona import Persona
from src.utils.excepciones import ValidationException, EstadoInvalidoException
from src.config.constantes import TIPOS_SEGURO
from typing import List, Dict, Any

class Paciente(Persona):
    
    def __init__(
        self, 
        dni: str, 
        nombre: str, 
        fecha_nacimiento: date, 
        telefono: str,
        id_paciente: int,
        tipo_seguro: str,
        fecha_registro: date
    ):
        
        super().__init__(dni, nombre, fecha_nacimiento, telefono)
        
        """
        Constructor de la clase Paciente
        
        Args:
            Propios:
                id_paciente (int): ID unico del paciente, auto-incremental
                tipo_seguro (str): Tipo de seguro del paciente (Ninguno, Publico, Privado)
                fecha_registro (date): Fecha de registro del paciente
            
            Heredados de Persona (super()):
                dni (str): DNI de la persona (8 digitos)
                nombre (str): Nombre completo de la persona de la persona
                fecha_nacimiento (date): Fecha de nacimiento 
                telefono (str): Telefono (9 digitos empezando con 9)
            
        Raises:
            ValidationException: Formato o estado de los datos incorrectos
        """
        
        # =========== VALIDACIONES ==========
        # ID
        if not isinstance(id_paciente, int) or id_paciente <= 0:
            raise ValidationException("Formato de ID de paciente invalido. Debe ser un numero entero positivo")
        
        # Tipo seguro
        if not isinstance(tipo_seguro, str) or not tipo_seguro:
            raise ValidationException("Formato de Tipo de seguro invalido. Debe de ser texto")
        
        tipo_seguro = tipo_seguro.strip().capitalize()
        
        if tipo_seguro not in TIPOS_SEGURO.keys():
            raise ValidationException("Tipo de seguro invalido. Debe ser Ninguno, Publico o Privado")
        
        # Fecha registro
        if not isinstance(fecha_registro, date) or not fecha_registro:
            raise ValidationException("Formato de fecha invalido. Debe ser tipo fecha DD/MM/AAAA")
        
        if fecha_registro > date.today():
            raise ValidationException("La fecha de registro no puede ser futura")
        
        # ========== ASIGNACION ==========
        self._id_paciente = id_paciente
        self._tipo_seguro = tipo_seguro
        self._porcentaje_descuento = TIPOS_SEGURO[tipo_seguro]
        self._fecha_registro = fecha_registro
        self._historial_consultas = []
        
    # ========== GETTERS ==========
    
    @property
    def id_paciente(self) -> int:
        return self._id_paciente

    @property
    def tipo_seguro(self) -> str:
        return self._tipo_seguro
    
    @property
    def porcentaje_descuento(self) -> float:
        return self._porcentaje_descuento
    
    @property 
    def historial_consultas(self) -> List[int]:
        return self._historial_consultas

    # ========== METODOS ==========
    def cambiar_tipo_seguro(self, nuevo_tipo: str) -> None:
        """
        Cambia el tipo de seguro de un Paciente
        
        Args:
            nuevo_tipo (str): Nuevo tipo de seguro a cambiar
        
        Raises:
            ValidationException: Tipo de seguro invalido
            EstadoInvalidoException: Asignar el mismo tipo de seguro
        """
        
        # Validaciones
        if not isinstance(nuevo_tipo, str) or not nuevo_tipo:
            raise ValidationException("Formato de nuevo Tipo de seguro invalido. Debe ser texto")
        
        nuevo_tipo = nuevo_tipo.strip().capitalize()
        
        if nuevo_tipo not in TIPOS_SEGURO.keys():
            raise ValidationException("Nuevo Tipo de seguro invalido. Debe ser Ninguno, Publico o Privado")
        
        if nuevo_tipo == self.tipo_seguro:
            raise EstadoInvalidoException(f"El seguro {self.tipo_seguro} ya esta registrado para el paciente {self.id_paciente}")
        
        # Cambio
        self._tipo_seguro = nuevo_tipo
        self._porcentaje_descuento = TIPOS_SEGURO[nuevo_tipo]
    
    def agregar_consulta_historial(self, id_consulta: int) -> None:
        """
        Agrega el ID de una consulta al historial del paciente
        
        Args:
            id_consulta (int): ID de la consulta a agregar
        
        Raises:
            ValidationException: Formato de ID invalido
            EstadoInvalidoException: Agregar una consulta ya registrada
        """
        
        # Validaciones
        if not isinstance(id_consulta, int) or id_consulta <= 0:
            raise ValidationException("Formato de ID de consulta invalido. Debe ser un numero entero positivo")
        
        if id_consulta in self.historial_consultas:
            raise EstadoInvalidoException(f"La consulta {id_consulta} ya esta registrada en el historial del paciente {self.id_paciente}")
        
        # Agregar consulta
        self._historial_consultas.append(id_consulta)
    
    def calcular_descuento(self, monto: float) -> float:
        """
        Calcula el monto final despues de aplicar un descuento (0%, 20%, 50%)
        
        Args:
            monto (float): Monto al cual aplicarle el descuento

        Raises:
            ValidationException: Formato de monto invalido
        
        Returns:
            float: Monto con descuento
        """
        
        # Validacion
        if not isinstance(monto, (float, int)) or monto <= 0:
            raise ValidationException("Formato de monto invalido. Debe ser un numero positivo")
        
        # Calculo
        if self.porcentaje_descuento == 0:
            return monto
        
        conversion = self.porcentaje_descuento / 100
        
        descuento = monto * conversion
        
        return monto - descuento
    
    def to_dict(self) -> Dict[str, Any]:
        """        
        Convierte el objeto Paciente a un diccionario para serialización JSON
        
        Returns:
            Dict[str, Any]: Representación en diccionario del objeto
        """
        
        return {
            "dni": self._dni,
            "nombre": self._nombre,
            "fecha_nacimiento": self._fecha_nacimiento.isoformat(),
            "telefono": self._telefono,
            "id_paciente": self._id_paciente,
            "tipo_seguro": self._tipo_seguro,
            "porcentaje_descuento": self._porcentaje_descuento,
            "fecha_registro": self._fecha_registro.isoformat(),
            "historial_consultas": self._historial_consultas.copy() if self._historial_consultas else []
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Paciente':
        """       
        Crea un objeto Paciente desde un diccionario (deserialización).
        
        Args:
            data (dict): Diccionario con los datos del personal
            
        Returns:
            Paciente: Objeto Paciente reconstruido
            
        Raises:
            ValueError: Si faltan datos requeridos o son inválidos
        """
        
        try:
            paciente = cls(
                dni=data["dni"],
                nombre=data["nombre"],
                fecha_nacimiento=date.fromisoformat(data["fecha_nacimiento"]),
                telefono=data["telefono"],
                id_paciente=data["id_paciente"],
                tipo_seguro=data["tipo_seguro"],
                fecha_registro=date.fromisoformat(data["fecha_registro"])
            )
            
            # Restaurar historial si existe
            if "historial_consultas" in data:
                paciente._historial_consultas = data["historial_consultas"]
            
            return paciente
        except KeyError as e:
            raise ValueError(f"Falta el campo requerido: {e}")
        except Exception as e:
            raise ValueError(f"Error al deserializar Paciente: {e}") 