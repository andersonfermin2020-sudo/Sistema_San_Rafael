"""
Representa un miembro del personal del hospital
Hereda de Persona

"""

from models.persona import Persona
from datetime import date
from typing import List, Dict, Any
from utils.excepciones import EstadoInvalidoException, ValidationException
from config.constantes import TURNOS, MOTIVOS_BAJA, ROLES_PERSONAL, ESPECIALIDADES, JORNADAS, SALARIOS_BASE, ESTADOS_PERSONAL
from utils.validaciones import Validaciones

class Personal(Persona):

    def __init__(
            self, 
            dni: str, 
            nombre: str, 
            fecha_nacimiento: date, 
            telefono: str,
            id_personal: int,
            rol: str,
            especialidad: str | None,
            departamentos: List[int],
            jornada: str,
            turno: str | None,
            salario_base: float,
            estado: str,
            fecha_contratacion: date,
            fecha_baja: date | None,
            motivo_baja: str | None
    ):

        """
        Constructor de la clase Personal
            
        Args:
            Propios:
                id_personal (int): ID de la persona, auto-incremental, unico
                rol (str): Rol de la persona, ej: Doctor, enfermera
                especialidad (str | None): Solo para doctores 
                departamentos (List[int]): Lista de IDs de departamentos asignados
                jornada (str): Jornada de trabajo
                turno (str | None): Turno de trabajo si jornada es por turnos
                salario_base (float): Salario base de la persona
                estado (str): Estado de trabajo de la persona, ej: Activo o Inactivo
                fecha_contratacion (date): Fecha de contratacion de la persona
                fecha_baja (date | None): Fecha de baja                
                motivo_baja (str | None): Motivo de la baja, ej: Renuncia, Despido, Fin de contrato
                
            Heredados de Persona (Super()):
                dni (str): DNI de la persona (8 digitos)
                nombre (str): Nombre completo de la persona de la persona
                fecha_nacimiento (date): Fecha de nacimiento 
                telefono (str): Telefono (9 digitos)
                
        Raises:
            ValidationException: Formato o estado de los datos incorrectos
        """

        super().__init__(dni, nombre, fecha_nacimiento, telefono)

        # Validaciones antes de asignar valores:
        # ID
        if not isinstance(id_personal, int) or id_personal <= 0:
            raise ValidationException("Formato invalido del ID del personal. Debe ser un numero entero positivo")
        
        # Rol
        if not isinstance(rol, str) or rol.strip().capitalize() not in ROLES_PERSONAL:
            raise ValidationException("Formato invalido del rol del personal. Debe ser: Doctor, Enfermera o Administrativo")
        
        # Especialidad
        if rol == "Doctor":
            if especialidad is None:
                raise ValidationException("Los doctores deben tener una especialidad")
            else:
                if not isinstance(especialidad, str) or especialidad.strip().title() not in ESPECIALIDADES:
                    raise ValidationException("Formato invalido de especialidad. Debe de ser: Medicina General, Pediatria o Cardiologia")
        else:
            if especialidad is not None:
                raise ValidationException("Solamente los doctores pueden tener especialidades en su registro")

        # Departamentos
        if not isinstance(departamentos, list) or len(departamentos) == 0:
            raise ValidationException("Formato de departamentos invalido. Debe ser una lista con (al menos un) departamento.")
        
        if not all(isinstance(d, int) and d > 0 for d in departamentos):
            raise ValidationException("Los IDs de departamentos deben ser enteros positivos")
        
        # Jornada
        if not isinstance(jornada, str) or jornada.strip().capitalize() not in JORNADAS:
            raise ValidationException("Formato de jornada invalido. Debe ser: Medio tiempo, Tiempo completo o Por turnos")
        
        # Turno
        if jornada == "Por turnos":
            if turno is None:
                raise ValidationException("El personal con jornada de 'Por turnos' debe de tener uno asignado")
            else:
                if not isinstance(turno, str) or turno.strip().capitalize() not in TURNOS:
                    raise ValidationException("Formato de turno invalido. Debe de ser: Manana, Tarde o Noche")
        else:
            if turno is not None:
                raise ValidationException("Solamente el personal con jornada de 'Por turnos' se le puede asignar uno")

        # Salario base
        if not isinstance(salario_base, float) or salario_base < 0:
            raise ValidationException("Formato invalido del salario base. Debe ser un numero positivo.")

        if salario_base != SALARIOS_BASE[rol]:
            raise ValidationException(f"El salario {salario_base} no concuerda con el salario base definido para un personal '{rol}'")
        
        # Estado
        if not isinstance(estado, str) or estado.strip().capitalize() not in ESTADOS_PERSONAL:
            raise ValidationException("Formato de estado invalido. Debe ser: Activo o Inactivo")
        
        # Fecha de contratacion
        if not isinstance(fecha_contratacion, date):
            raise ValidationException("Formato de fecha invalido. La fecha de contratacion debe de ser un tipo de dato (fecha)")
        
        if fecha_contratacion > date.today():
            raise ValidationException("La fecha de contratacion no puede ser futura")
        
        # Fecha y motivo de baja
        if estado == "Activo":
            if fecha_baja is not None:
                raise ValidationException("Personal activo no puede tener fecha de baja")
            if motivo_baja is not None:
                raise ValidationException("Personal activo no puede tener motivo de baja")
        else: 
            if fecha_baja is None:
                raise ValidationException("Personal inactivo debe tener fecha de baja")
            if motivo_baja is None:
                raise ValidationException("Personal inactivo debe tener motivo de baja")
            
            # Validar fecha de baja
            if not isinstance(fecha_baja, date):
                raise ValidationException("Fecha de baja debe ser tipo 'date'")
            if fecha_baja < fecha_contratacion:
                raise ValidationException("Fecha de baja no puede ser anterior a contratación")
            
            # Validar motivo de baja
            if not isinstance(motivo_baja, str) or not motivo_baja.strip():
                raise ValidationException("Motivo de baja debe ser texto no vacío")
            
            motivo_normalizado = motivo_baja.strip().capitalize()
            if motivo_normalizado not in MOTIVOS_BAJA:
                raise ValidationException(f"Motivo inválido: {motivo_baja}")

        # Asignacion
        self._id_personal = id_personal
        self._rol = rol.strip().capitalize()
        self._especialidad = especialidad.strip().title() if especialidad else None
        self._departamentos = departamentos.copy()
        self._jornada = jornada.strip().capitalize()
        self._turno = turno.strip().capitalize() if turno else None
        self._salario_base = float(salario_base)
        self._estado = estado.strip().capitalize()
        self._fecha_contratacion = fecha_contratacion
        self._fecha_baja = fecha_baja
        estado_norm = estado.strip().capitalize()
        if estado_norm == "Inactivo" and motivo_baja:
            self._motivo_baja = motivo_baja.strip().capitalize()
        else:
            self._motivo_baja = None

    # Getters
    @property
    def id_personal(self) -> int:
        return self._id_personal
    
    @property
    def rol(self) -> str:
        return self._rol
    
    @property
    def especialidad(self) -> str | None:
        return self._especialidad
    
    @property
    def departamentos(self) -> List[int]:
        return self._departamentos
    
    @property
    def estado(self) -> str:
        return self._estado

    @property
    def jornada(self) -> str:
            return self._jornada

    @property
    def turno(self) -> str | None:
        return self._turno

    @property
    def salario_base(self) -> float:
        return self._salario_base
    
    @property
    def fecha_baja(self) -> date | None:
        return self._fecha_baja

    @property
    def motivo_baja(self) -> str | None:
        return self._motivo_baja
    
    # Metodos 
    def asignar_departamento(self, id_departamento: int) -> None:
        """
        Asigna un departamento nuevo al personal
        
        Args: 
            id_departamento (int): ID del departamento a asignar
            
        Raises:
            ValidationException: Si el ID es invalido
            EstadoInvalidoException: Si el departamento ya se encuentra asignado al personal o se encuentra inactivo
        """
        # Validaciones:
        
        # Formato de ID
        if not isinstance(id_departamento, int) or id_departamento <= 0:
            raise ValidationException(f"ID de departamento invalido {id_departamento}. Debe ser un numero entero positivo")
        
        # Personal no se encuentre inactivo
        if self._estado == "Inactivo":
            raise EstadoInvalidoException("No se le puede asignar un departamento a un personal inactivo.")
        
        # Departamento no se encuentra asignado
        if id_departamento in self._departamentos:
            raise EstadoInvalidoException(f"El departamento {id_departamento} ya está asignado al personal #{self.id_personal}")
        
        # Paso todas las validaciones:
        self._departamentos.append(id_departamento)

    def remover_departamento(self, id_departamento: int) -> None:
        """
        Remueve un departamento de el registro de un personal
        
        Args:
            id_departamento (int): ID del departamento a remover
            
        Raises:
            ValidationException: Formato incorrecto del ID 
            EstadoInvalidoException: 
                Personal inactivo
                Departamento no asignado 
                Remover unico departamento
        """
        
        # Validaciones:
        
        # Formato correcto del ID
        if not isinstance(id_departamento, int) or id_departamento <= 0:
            raise ValidationException(f"ID de departamento invalido {id_departamento}. Debe ser un numero entero positivo")
        
        # Personal inactivo
        if self._estado == "Inactivo":
            raise EstadoInvalidoException("No se puede remover un departamento a un personal inactivo")
        
        # Departamento no asignado
        if id_departamento not in self._departamentos:
            raise EstadoInvalidoException(f"El departamento {id_departamento} no se encuentra actualmente asignado al personal {self._dni}")
        
        # Remover unico departameto
        if len(self._departamentos) == 1:
            raise EstadoInvalidoException(f"No se puede remover el único departamento de un personal.")
        
        # Paso las validaciones:
        self._departamentos.remove(id_departamento)

    def cambiar_turno(self, nuevo_turno: str) -> None:
        """
        Cambiar turno a un personal (con jornada: Por turnos)
        
        Args:
            nuevo_turno (str): Nuevo turno a cambiar
        
        Raises:
            ValidationException: 
                Formato invalido
                Nuevo turno no concuerda con los ya definidos
            EstadoInvalidoException: 
                Si el personal esta inactivo
                Si el personal no cuenta con una jornada por turnos
                Tratar de cambiarlo por el mismo turno
        """
        
        # Validaciones:
        
        # Formato invalido o turno no definido
        if not isinstance(nuevo_turno, str) or not nuevo_turno.strip(): 
            raise ValidationException(f"Formato invalido. Debe ser texto y no puede estar vacio")
        
        nuevo_turno_estandarizado = nuevo_turno.strip().capitalize()
        
        # Turno no definido
        if nuevo_turno_estandarizado not in TURNOS:
            raise ValidationException(f"Formato invalido: {nuevo_turno}. Deber ser: Manana, Tarde o Noche")
        
        # Personal inactivo
        if self._estado == "Inactivo":
            raise EstadoInvalidoException(f"No se puede cambiar el turno a un personal inactivo")

        # Personal sin jornada 'Por turnos'
        if self._jornada != "Por turnos":
            raise EstadoInvalidoException(f"El personal {self._dni} no cuenta con una jornada por turnos")
        
        # Cambiar a mismo turno
        if self._turno == nuevo_turno_estandarizado:
            raise EstadoInvalidoException(f"El personal {self._dni} ya cuenta con el turno {nuevo_turno_estandarizado}")
        
        # Paso todas las validaciones:
        self._turno = nuevo_turno_estandarizado

    def inactivar(self, fecha_baja: date, motivo: str) -> None:
        """
        Inactiva a un personal (sin despedir por politicas del hospital)
        
        Args:
            fecha_baja (date): Fecha de baja (No puede ser futura)
            motivo (str): Motivo de la baja, ej: Renuncia, despido, fin de contrato
        
        Raises:
            TypeError: No es un objeto date
            ValidationException: 
                Formato incorrecto del motivo
                Motivo no definido
            EstadoInvalidoException:
                El personal se encuentra con estado inactivo 
                La fecha de baja no puede ser menor a la fecha de contratacion
                La fecha de baja no puede ser futura
        """
        
        # Validaciones:
        
        # Fecha no es objeto date
        if not isinstance(fecha_baja, date):
            raise TypeError("Formato incorrecto. La fecha de baja debe ser un tipo de dato (fecha)")
        
        # Formato invalido
        if not isinstance(motivo, str) or not motivo.strip():
            raise ValidationException("Formato invalido. Debe ser texto y no puede estar vacio")
        
        motivo_estandarizado = motivo.strip().capitalize()
        
        # Motivo no definido
        if motivo_estandarizado not in MOTIVOS_BAJA:
            raise ValidationException(f"Formato invalido {motivo}. Debe de ser: Renuncia, Despido o Fin de contrato")
        
        # Personal con estado inactivo
        if self._estado == "Inactivo":
            raise EstadoInvalidoException(f"El personal {self._dni} ya se encuentra inactivo")
        
        # Fecha de baja menor a fecha de contratacion
        if fecha_baja < self._fecha_contratacion:
            raise EstadoInvalidoException("La fecha de baja no puede ser menor a la fecha de contratacion")
        
        # Fecha de baja no puede ser pasada
        if Validaciones.fecha_futura(fecha_baja):
            raise EstadoInvalidoException("La fecha de baja no puede ser futura")
        
        # Paso las validaciones
        self._estado = "Inactivo"
        self._fecha_baja = fecha_baja
        self._motivo_baja = motivo_estandarizado

    def esta_activo(self) -> bool:
        """
        Verifica si un personal esta activo
        
        Returns:
            bool: True si lo esta | False si no lo esta
        """
        return self._estado == "Activo"

    def es_doctor(self) -> bool:
        """
        Verifica si un personal es Doctor
        
        Returns:
            bool: True si lo es | False si no lo es
        """
        return self._rol == "Doctor"

    def calcular_salario_mensual(self, bono: float = 0.0) -> float:
        """
        Calcula el salario mensual del personal

        Args:
            bono (float): (Opcional) Bono adicional a aplicar

        Returns:
            float: Salario base mas el bono

        Raises:
            ValueError: Si el bono es negativo
        """

        if bono < 0:
            raise ValueError(f"El bono no puede ser negativo: {bono}")

        return self._salario_base + bono

    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el objeto Personal a un diccionario para serialización JSON.
        
        Returns:
            dict: Representación en diccionario del objeto
        """
        return {
            "dni": self._dni,
            "nombre": self._nombre,
            "fecha_nacimiento": self._fecha_nacimiento.isoformat(),
            "telefono": self._telefono,
            "id_personal": self._id_personal,
            "rol": self._rol,
            "especialidad": self._especialidad,
            "departamentos": self._departamentos.copy(),
            "jornada": self._jornada,
            "turno": self._turno,
            "salario_base": self._salario_base,
            "estado": self._estado,
            "fecha_contratacion": self._fecha_contratacion.isoformat(),
            "fecha_baja": self._fecha_baja.isoformat() if self._fecha_baja else None,
            "motivo_baja": self._motivo_baja
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Personal':
        """
        Crea un objeto Personal desde un diccionario (deserialización).
        
        Args:
            data (dict): Diccionario con los datos del personal
            
        Returns:
            Personal: Objeto Personal reconstruido
            
        Raises:
            ValueError: Si faltan datos requeridos o son inválidos
        """
        try:
            return cls(
                dni=data["dni"],
                nombre=data["nombre"],
                fecha_nacimiento=date.fromisoformat(data["fecha_nacimiento"]),
                telefono=data["telefono"],
                id_personal=data["id_personal"],
                rol=data["rol"],
                especialidad=data.get("especialidad"),
                departamentos=data["departamentos"],
                jornada=data["jornada"],
                turno=data.get("turno"),
                salario_base=data["salario_base"],
                estado=data["estado"],
                fecha_contratacion=date.fromisoformat(data["fecha_contratacion"]),
                fecha_baja=date.fromisoformat(data["fecha_baja"]) if data.get("fecha_baja") else None,
                motivo_baja=data.get("motivo_baja")
            )
        except KeyError as e:
            raise ValueError(f"Falta el campo requerido: {e}")
        except Exception as e:
            raise ValueError(f"Error al deserializar Personal: {e}")
