"""
Representa una cita medica agendada
"""
from datetime import date, time, datetime
from src.utils.excepciones import ValidationException, EstadoInvalidoException
from src.config.constantes import ESPECIALIDADES
from typing import List, Dict, Any
class Cita:
    def __init__(
        self,
        id_cita: int,
        id_paciente: int, # FK a Paciente
        id_doctor: int, # FK a Doctor
        fecha: date,
        hora: time,
        especialidad: str,
        motivo: str,
        validar_fecha_futura: bool = True
        ) -> None:
        
        """
        Constructor de la clase Cita
        
        Args:
            id_cita (int): ID unico de la cita, auto-incremental
            id_paciente (int): ID del paciente dueno de la cita
            id_doctor (int): ID del doctor a cargo de la cita
            fecha (date): Fecha en que sera la cita
            hora (time): Hora de atencion
            especialidad (str): Especialidad necesaria del doctor para la cita
            motivo (str): Motivo de la cita
        
        Raises:
            ValidationException: Formato o estado de los datos incorrectos
        """
        
        # ========== VALIDACIONES ==========
        
        # ID cita
        if not isinstance(id_cita, int) or id_cita <= 0:
            raise ValidationException("Formato de ID de cita invalido. Debe ser un numero entero positivo")
        
        # ID paciente
        if not isinstance(id_paciente, int) or id_paciente <= 0:
            raise ValidationException("Formato de ID de paciente invalido. Debe ser un numero entero positivo")
        
        # ID doctor
        if not isinstance(id_doctor, int) or id_doctor <= 0:
            raise ValidationException("Formato de ID de doctor invalido. Debe ser un numero entero positivo")
        
        # Fecha
        if not isinstance(fecha, date):
            raise ValidationException("Formato de fecha invalido. Debe ser tipo fecha mayor o igual a la actual")
        
        # Hora
        if not isinstance(hora, time):
            raise ValidationException("Formato de hora invalido. Debe ser de tipo hora/time")
        
        if not (time(7, 0) <= hora < time(22, 0)):
            raise ValidationException("Hora invalida. Debe de ser entre 7:00AM y 10:00PM")

        # Validar que no sea pasada
        if validar_fecha_futura:
            momento_cita = datetime.combine(fecha, hora)
            if momento_cita < datetime.now():
                raise ValidationException(
                    "La fecha y hora de la cita no pueden ser en el pasado"
                )
        
        # Especialidad
        if not especialidad or not isinstance(especialidad, str):
            raise ValidationException("Formato de especialidad invalida. Debe ser texto y no puede estar vacio")
        
        especialidad = especialidad.strip().title()
        if especialidad not in ESPECIALIDADES:
            raise ValidationException("Especialidad invalida. Debe ser Medicina General, Pediatria o Cardiologia")
        
        # Motivo
        if not motivo or not isinstance(motivo, str):
            raise ValidationException("Formato de motivo invalido. Debe ser texto y no puede estar vacio")
        motivo = motivo.strip().capitalize()
        
        # ========== ASIGNACION ==========
        self._id_cita = id_cita
        self._id_paciente = id_paciente
        self._id_doctor = id_doctor
        self._fecha = fecha
        self._hora = hora
        self._especialidad = especialidad
        self._motivo = motivo
        self._estado = "Agendada"
        self._fecha_creacion = datetime.now()
        self._historial_cambios = []
    
    # ========== GETTERS ==========
    @property
    def id_cita(self) -> int:
        return self._id_cita
    
    @property
    def id_paciente(self) -> int:
        return self._id_paciente
    
    @property
    def id_doctor(self) -> int:
        return self._id_doctor
    
    @property
    def fecha(self) -> date:
        return self._fecha
    
    @property 
    def hora(self) -> time:
        return self._hora

    @property
    def motivo(self) -> str:
        return self._motivo
    
    @property
    def estado(self) -> str:
        return self._estado
    
    @property
    def historial_cambios(self) -> List[dict]:
        return self._historial_cambios.copy()
    
    # ========== METODOS =========
    def reprogramar(self, nueva_fecha: date, nueva_hora: time, usuario: int) -> None:
        """
        Reprograma la fecha o la hora de una cita agendada
        
        Args:
            nueva_fecha (date): Fecha nueva de la cita
            nueva_hora (time): Hora nueva de la cita
        
        Raises:
            ValidationException: Formato o estado de fecha/hora invalido
            EstadoInvalidoException: Estado de la cita invalido
                                    Fecha/hora nueva igual a la ya registrada
        """
        
        # Validaciones
        if not isinstance(usuario, int) or usuario <= 0:
            raise ValidationException("ID de usuario debe ser entero positivo")
        
        if self.estado != "Agendada":
            raise EstadoInvalidoException(f"No se puede reprogramar esta cita. El estado actual de la cita es '{self.estado}'")
        
        if not isinstance(nueva_fecha, date):
            raise ValidationException("Formato de fecha invalido. Debe ser tipo fecha/date")
        
        if not isinstance(nueva_hora, time):
            raise ValidationException("Formato de hora invalido. Debe ser tipo hora/time")
        
        momento_nuevo = datetime.combine(nueva_fecha, nueva_hora)
        if momento_nuevo < datetime.now():
            raise ValidationException("La nueva fecha y hora no pueden ser en el pasado")
        
        if not (time(7, 0) <= nueva_hora < time(22, 0)):
            raise ValidationException("Hora invalida. Debe de ser entre 7:00AM y 10:00PM")
        
        if nueva_fecha == self.fecha and nueva_hora == self.hora:
            raise EstadoInvalidoException("La nueva fecha/hora es igual a las ya registrada")
        
        # Crear diccionario de cambios
        registro_antiguo = {
            "fecha_antigua": self.fecha.isoformat(),
            "hora_antigua": self.hora.isoformat()
        }
        
        cambio = {
            "fecha_operacion": datetime.now().isoformat(),
            "id_empleado": usuario,
            "registro_antiguo": registro_antiguo,
            "registro_nuevo": {
                "fecha_nueva": nueva_fecha.isoformat(),
                "hora_nueva": nueva_hora.isoformat()
            }
        }
        
        # Actualizar
        self._fecha = nueva_fecha
        self._hora = nueva_hora
        
        # Guardar cambios
        self._historial_cambios.append(cambio)
    
    def cancelar(self) -> None:
        """
        Cancela una cita en estado de Agendada

        Raises:
            EstadoInvalidoException: Estado de la cita diferente de Agendada
        """
        
        # Validacion
        if self.estado != "Agendada":
            raise EstadoInvalidoException(f"No se puede cancelar esta cita. El estado actual de la cita es '{self.estado}'")
        
        # Cancelar
        self._estado = "Cancelada"
    
    def completar(self) -> None:
        """
        Completa una cita en estado de Agendada

        Raises:
            EstadoInvalidoException: Estado de la cita diferente de Agendada
        """
        
        # Validacion
        if self.estado != "Agendada":
            raise EstadoInvalidoException(f"No se puede completar esta cita. El estado actual de la cita es '{self.estado}'")
        
        # Completar
        self._estado = "Completada"
    
    def puede_ser_reprogramada(self) -> bool:
        """
        Verifica si una cita se puede reprogramar
        
        Returns:
            bool: True si tiene estado Agendada | False si tiene un estado diferente
        """
        
        if self.estado != "Agendada":
            return False
        
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte un objeto Cita en un diccionario para serializacion JSON
        
        Returns:
            Dict[str, Any]: Diccionario que representa al objeto
        """
        return {
            "id_cita": self._id_cita,
            "id_paciente": self._id_paciente,
            "id_doctor": self._id_doctor,
            "fecha": self._fecha.isoformat(),
            "hora": self._hora.isoformat(),
            "especialidad": self._especialidad,
            "motivo": self._motivo,
            "estado": self._estado,
            "fecha_creacion": self._fecha_creacion.isoformat(),
            "historial_cambios": self._historial_cambios if self._historial_cambios else []
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Cita':
        """
        Crea un objeto Cita desde un diccionario (deserializacion)
        
        Args:
            data (Dict[str, Any]): Diccionario con los datos del objeto
        
        Returns:
            Cita: Objeto Cita reconstruido
        
        Raises:
            ValueError: Si faltan datos o son invalidos
        
        """
        
        try:
            cita = cls(
                id_cita=data["id_cita"],
                id_paciente=data["id_paciente"],
                id_doctor=data["id_doctor"],
                fecha=date.fromisoformat(data["fecha"]),
                hora=time.fromisoformat(data["hora"]),
                especialidad=data["especialidad"],
                motivo=data["motivo"],
                validar_fecha_futura=False
            )
            
            cita._estado = data["estado"]
            cita._fecha_creacion = datetime.fromisoformat(data["fecha_creacion"])
            cita._historial_cambios = data["historial_cambios"]
            
            return cita
            
        except KeyError as e:
            raise ValueError(f"Falta el campo requerido: {e}")
        except Exception as e:
            raise ValueError(f"Error al deserializar Cita: {e}")