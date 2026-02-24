"""
Representa un contrato laboral de un miembro del personal

"""
from datetime import date, timedelta
from src.utils.excepciones import ValidationException, EstadoInvalidoException
from src.config.constantes import TIPOS_CONTRATOS, ESTADOS_CONTRATO, SALARIOS_BASE
from typing import Dict, Any

class Contrato:
    
    def __init__(
            self, 
            id_contrato: int, 
            id_personal: int, 
            tipo: str, 
            fecha_inicio: date, 
            fecha_fin: date | None, 
            salario_base: float,
            estado: str
    ):
        
        """
        Constructor de la clase Contrato
        
        Args:
            id_contrato (int): ID del contrato (debe ser unico)
            id_personal (int): ID del personal al cual se le asigna el contrato (FK)
            tipo (str): Tipo de contrato
            fecha_inicio (date): Fecha de inicio del contrato
            fecha_fin (date | None): Fecha fin (solo si es de tipo Temporal)
            salario_base (float): Salario base del personal
            estado (str): Estado del contrato
        
        Raises:
            ValidationException: Formato o estado de los datos incorrectos
        
        """
        
        # ========== Validaciones antes de asignacion ==========
        
        # ID de contrato
        if not isinstance(id_contrato, int) or id_contrato <= 0:
            raise ValidationException("Formato de ID de contrato invalido. Debe ser un numero entero positivo")
        
        # ID de personal
        if not isinstance(id_personal, int) or id_personal <= 0:
            raise ValidationException("Formato de ID de personal invalido. Debe ser un numero entero positivo")
        
        # Tipo
        if not isinstance(tipo, str) or tipo.strip().capitalize() not in TIPOS_CONTRATOS:
            raise ValidationException("Tipo de contrato invalido. Debe ser: Temporal, Indefinido o Por honorarios")
        
        # Fecha de inicio
        if not isinstance(fecha_inicio, date):
            raise ValidationException("Formato de fecha de inicio invalido. Debe ser un tipo de dato (fecha)")
        
        if fecha_inicio > date.today():
            raise ValidationException("La fecha de inico del contrato no puede ser futura")
        
        # Fecha de fin
        if tipo.strip().capitalize() == "Temporal":
            if not isinstance(fecha_fin, date):
                raise ValidationException("Los contratos temporales deben de tener fecha limite")
            
            if fecha_fin <= fecha_inicio:
                raise ValidationException("La fecha limite debe ser mayor a la fecha de inicio del contrato")
            
        else:
            if fecha_fin is not None:
                raise ValidationException("Solo los contratos temporales pueden tener fecha limite")
        
        # Salario base
        if not isinstance(salario_base, (float, int)) or salario_base <= 0:
            raise ValidationException("Formato de salario invalido. Debe ser un numero positivo")
        
        if salario_base not in SALARIOS_BASE.values():
            raise ValidationException("EL salario base no concuerda con los salarios definidos por el hospital")
        
        # Estado 
        if not isinstance(estado, str) or estado.strip().capitalize() not in ESTADOS_CONTRATO:
            raise ValidationException("Formato de estado de contrato invalido. Debe ser: Activo, Vencido o Finalizado")
        
        if estado.strip().capitalize() == "Vencido":
            if fecha_fin is None or date.today() < fecha_fin:
                raise ValidationException("Estado 'Vencido' solo es válido si la fecha fin ya paso")
        
        # ========== Asignacion ==========
        
        self._id_contrato = id_contrato
        self._id_personal = id_personal
        self._tipo = tipo.strip().capitalize()
        self._fecha_inicio = fecha_inicio
        self._fecha_fin = fecha_fin
        self._salario_base = float(salario_base)
        self._estado = estado.strip().capitalize()
        
    
    # ========== Getters ==========
    @property
    def id_contrato(self) -> int:
        return self._id_contrato
    
    @property
    def id_personal(self) -> int:
        return self._id_personal
    
    @property
    def tipo(self) -> str:
        return self._tipo
    
    @property
    def fecha_inicio(self) -> date:
        return self._fecha_inicio
    
    @property
    def fecha_fin(self) -> date | None:
        return self._fecha_fin
    
    @property
    def estado(self) -> str:
        return self._estado
    
    # ========== Metodos ==========
    
    def esta_por_vencer(self, dias: int = 60) -> bool:
        """
        Calcula si un contrato esta proximo a vencer en (60 dias por defecto)

        Args:
            dias (int, optional): Dias de alerta antes de su fecha limite

        Returns:
            bool: True si esta en el rango de dias | False si no lo esta
        """
        
        # No es un contrato temporal
        if self._fecha_fin is None:
            return False
        
        # Calculo de dias
        inico_alerta = self._fecha_fin - timedelta(days=dias)
        hoy = date.today()
        
        # Esta o no esta en el rango
        return inico_alerta <= hoy <= self._fecha_fin
    
    def dias_restantes(self) -> int | None:
        """
        Calcula los dias que le quedan a un contrato con fecha de vencimiento
        
        Returns:
            int: Dias restantes del contrato
            
        Raises:
            EstadoInvalidoException: 
                El contrato no es temporal 
                El contrato ya vencio
        """

        # Contrato no es temporal
        if self._fecha_fin is None:
            raise EstadoInvalidoException(f"El contrato {self._id_contrato} no es un contrato temporal (no posee fecha fin)")
        
        # El contrato se encuentra vencido
        if self._fecha_fin < date.today():
            raise EstadoInvalidoException(f"El contrato {self._id_contrato} se encuentra vencido. Fecha de vencimiento: {self._fecha_fin}")
        
        # Calculo de dias restantes
        dias_restantes = self._fecha_fin - date.today()
        return dias_restantes.days
    
    def actualizar_estado(self) -> None:
        """
        Verifica si la fecha de fin ha pasado y actualiza el estado a 'Vencido'.
        Si el contrato no es temporal o aún no ha vencido, no hace nada.
        
        """

        # Contrato no es temporal
        if self._tipo != "Temporal" or self._fecha_fin is None:
            return None
        
        # El contrato aun no vence
        if date.today() < self._fecha_fin:
            return None
        
        # Cambiar estado (cubre == y >)
        self._estado = "Vencido"
        print(f"Contrato {self._id_contrato} ha sido marcado como Vencido.")

    def finalizar(self) -> None:
        """
        Cambia el estado del contrato a finalizado por motivos administrativos (renuncia/despido)
        
        Raises:
            EstadoInvalidoException:
                El contrato se encuentra vencido (tipo temporal)
                El contrato se encuentra finalizado
        """
        # El contrato se encuentra vencido (tipo temporal)
        if self._estado == "Vencido":
            raise EstadoInvalidoException(f"El contrato {self._id_contrato} es de tipo temporal y ya se encuentra vencido.")
        
        # El contrato ya fue finalizado
        if self._estado == "Finalizado":
            raise EstadoInvalidoException(f"El contrato {self._id_contrato} ya se encuentra finalizado")
        
        # Cambiar estado a finalizado
        self._estado = "Finalizado"
        self._fecha_fin = date.today()
        print(f"Cambio de estado del contrato {self._id_contrato} a 'Finalizado'")

    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el objeto contrato en un diccionario para serializacion JSON
        
        Returns:
            dict: Representacion del objeto en un diccionario
        """
        return {
            "id_contrato": self._id_contrato,
            "id_personal": self._id_personal,
            "tipo": self._tipo,
            "fecha_inicio": self._fecha_inicio.isoformat(),
            "fecha_fin": self._fecha_fin.isoformat() if self._fecha_fin else None,
            "salario_base": self._salario_base,
            "estado": self._estado
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Contrato':
        """
        Crea un objeto Contrato desde un archivo JSON (deserializacion)
        
        Args:
            data (dict): Diccionario con los datos del contrato
            
        Returs:
            Contrato: Objeto Contrato reconstruido
            
        Raises:
            ValueError: Si faltan datos requeridos o son invalidos
        
        """
        
        try:
            return cls(
                id_contrato=data["id_contrato"],
                id_personal=data["id_personal"],
                tipo=data["tipo"],
                fecha_inicio=date.fromisoformat(data["fecha_inicio"]),
                fecha_fin=date.fromisoformat(data["fecha_fin"]) if data.get("fecha_fin") else None,
                salario_base=data["salario_base"],
                estado=data["estado"]
            )
        except KeyError as e:
            raise ValueError(f"Falta el campo requerido: {e}")
        except Exception as e:
            raise ValueError(f"Error al deserializar Contrato: {e}")
