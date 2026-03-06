"""
Representa una consulta medica completa

"""

from datetime import datetime
from typing import List, Dict, Any
from src.utils.excepciones import ValidationException, EstadoInvalidoException
from src.config.constantes import ESPECIALIDADES

class Consulta:
    def __init__(
        self,
        id_consulta: int,
        id_cita: int,
        id_paciente: int,
        id_doctor: int,
        especialidad: str,
        diagnostico: str,
        tratamiento: str | None,
        recetas: List[dict] | None = None
    ):
        """
        Constructor de la clase Consulta
        
        Args:
            id_consulta (int): ID de la consulta (unico, auto-incremental)
            id_cita (int): ID de la cita (FK a Cita 1 a 1)
            id_paciente (int): ID del paciente (FK a Paciente)
            id_doctor (int): ID del doctor (FK a Personal)
            fecha_hora (datetime): fecha y hora de la Consulta
            especialidad (str): Especialidad del doctor (Medicina General, Pediatria, Cardiologia)
            diagnostico (str): Diagnostico de la consulta
            tratamiento (str | None): Tratamiento (Opcional)
            recetas (List[dict], optional): Lista de medicamentos recetados.
                Cada dict debe tener la estructura:
                {
                    "id_medicamento": int,  # ID del medicamento
                    "cantidad": int         # Cantidad a recetar
                }
        Raises:
            ValidationException: Formato o estado de los datos incorrectos
        """
        
        # ========== VALIDACIONES ==========
        
        # IDs 
        ids_iterar = {"Consulta": id_consulta, "Cita": id_cita, "Paciente": id_paciente, "Doctor": id_doctor}
        for clave, id in ids_iterar.items():
            if not isinstance(id, int) or id <= 0:
                raise ValidationException(f"ID de {clave} invalido. Debe ser un numero entero positivo")
        
        # Especialidad
        if not especialidad or not isinstance(especialidad, str):
            raise ValidationException(f"Formato de especialidad invalido. Debe ser texto y no puede estar vacio")
        
        especialidad = especialidad.strip().title()
        if especialidad not in ESPECIALIDADES:
            raise ValidationException(f"Especialidad invalida. Debe ser Medicina General, Pediatria o Cardiologia")
        
        # Diagnostico
        if not isinstance(diagnostico, str):
            raise ValidationException("Diagnóstico debe ser texto")

        diagnostico = diagnostico.strip()
        if not diagnostico:
            raise ValidationException("Diagnóstico no puede estar vacío")

        if len(diagnostico) < 20:
            raise ValidationException("Diagnóstico debe tener al menos 20 caracteres")
        
        # Tratamiento
        if tratamiento is not None:
            if not isinstance(tratamiento, str):
                raise ValidationException("Formato de tratamiento invalido. Debe de ser texto")
            
            tratamiento = tratamiento.strip().capitalize()
            
            if not tratamiento:
                raise ValidationException("Formato de tratamiento invalido. No puede estar vacio")
            
            if len(tratamiento) < 10:
                raise ValidationException("Tratamiento invalido. Debe de tener como minimo 10 caracteres")
        
        # Receta
        if recetas is not None:
            if not isinstance(recetas, list):
                raise ValidationException("Recetas debe ser una lista")
            
            for i, receta in enumerate(recetas):
                if not isinstance(receta, dict):
                    raise ValidationException(f"Receta {i} debe ser un diccionario")
                
                if "id_medicamento" not in receta or "cantidad" not in receta:
                    raise ValidationException(
                        f"Receta {i} debe contener 'id_medicamento' y 'cantidad'"
                    )
                
                if not isinstance(receta["id_medicamento"], int) or receta["id_medicamento"] <= 0:
                    raise ValidationException(
                        f"id_medicamento en receta {i} debe ser entero positivo"
                    )
                
                if not isinstance(receta["cantidad"], int) or receta["cantidad"] <= 0:
                    raise ValidationException(
                        f"cantidad en receta {i} debe ser entero positivo"
                    )
        
        # ========== ASIGNACION ==========
        self._id_consulta = id_consulta
        self._id_cita = id_cita
        self._id_paciente = id_paciente
        self._id_doctor = id_doctor
        self._fecha_hora = datetime.now()
        self._especialidad = especialidad
        self._diagnostico = diagnostico
        self._tratamiento = tratamiento if tratamiento else None
        self._recetas = recetas if recetas is not None else []
        
    # ========== GETTERS ==========
    @property
    def id_consulta(self) -> int:
        return self._id_consulta
    
    @property
    def id_cita(self) -> int:
        return self._id_cita
    
    @property
    def diagnostico(self) -> str:
        return self._diagnostico
    
    @property
    def recetas(self) -> List[dict]:
        return self._recetas.copy()
    
    @property
    def id_paciente(self) -> int:
        return self._id_paciente

    @property
    def id_doctor(self) -> int:
        return self._id_doctor

    @property
    def fecha_hora(self) -> datetime:
        return self._fecha_hora

    @property
    def especialidad(self) -> str:
        return self._especialidad

    @property
    def tratamiento(self) -> str | None:
        return self._tratamiento
    
    # ========== METODOS ==========
    def agregar_receta(self, id_medicamento: int, cantidad: int) -> None:
        """
        Agrega medicamentos a una receta (ID del medicamento y cantidad)
        
        Args:
            id_medicamento (int): ID del medicamento a recetar
            cantidad (int): Cantidad del medicamento
        
        Raises:
            ValidationException: Formato o estado de datos invalidos
            EstadoInvalidoException: Agregar un medicamento ya registrado
        """
        
        # Validar datos
        if not isinstance(id_medicamento, int) or id_medicamento <= 0:
            raise ValidationException("Formato de ID de medicamento invalido. Debe ser un numero entero positivo")
        
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValidationException("Cantidad invalida para un medicamento. Debe ser un numero entero positivo")
        
        # Medicamento ya registrado
        if any(r["id_medicamento"] == id_medicamento for r in self._recetas):
            raise EstadoInvalidoException(f"El medicamento {id_medicamento} ya está en la receta")
        
        # Registro
        registro = {"id_medicamento": id_medicamento, "cantidad": cantidad}
        
        # Agregar
        self._recetas.append(registro)
    
    def eliminar_receta(self, id_medicamento: int) -> None:
            """
            Elimina un medicamento de la receta de la consulta usando su ID
            
            Args:
                id_medicamento (int): ID del medicamento a eliminar
                
            Raises:
                ValidationException: Formato de ID invalido
                EstadoInvalidoException: El medicamento no existe en la receta actual
            """
            
            # Validacion de formato
            if not isinstance(id_medicamento, int) or id_medicamento <= 0:
                raise ValidationException("Formato de ID de medicamento invalido. Debe ser un numero entero positivo")
            
            # Verificar si el medicamento existe en la lista actual
            existe = any(r["id_medicamento"] == id_medicamento for r in self._recetas)
            
            if not existe:
                raise EstadoInvalidoException(
                    f"No se puede eliminar: el medicamento {id_medicamento} no existe en esta receta"
                )
                
            # Filtrar la lista (Eliminacion)
            self._recetas = [r for r in self._recetas if r["id_medicamento"] != id_medicamento]

    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el objeto Consulta a un diccionario para serialización JSON.
        
        Returns:
            Dict[str, Any]: Representación en diccionario del objeto
        """
        return {
            "id_consulta": self._id_consulta,
            "id_cita": self._id_cita,
            "id_paciente": self._id_paciente,
            "id_doctor": self._id_doctor,
            "fecha_hora": self._fecha_hora.isoformat(),
            "especialidad": self._especialidad,
            "diagnostico": self._diagnostico,
            "tratamiento": self._tratamiento,
            "recetas": self._recetas
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Consulta':
        """
        Crea un objeto Consulta desde un diccionario (deserializacion)
        
        Args:
            data (Dict[str, Any]): Diccionario con los datos del objeto
        
        Returns:
            Consulta: Objeto Consulta reconstruido
        
        Raises:
            ValueError: Si faltan datos o son invalidos
        
        """
        
        try:
            consulta = cls(
                id_consulta=data["id_consulta"],
                id_cita=data["id_cita"],
                id_paciente=data["id_paciente"],
                id_doctor=data["id_doctor"],
                especialidad=data["especialidad"],
                diagnostico=data["diagnostico"],
                tratamiento=data["tratamiento"],
                recetas=data["recetas"]
            )
            
            consulta._fecha_hora = datetime.fromisoformat(data["fecha_hora"])

            return consulta
        
        except KeyError as e:
            raise ValueError(f"Falta el campo requerido: {e}")
        except Exception as e:
            raise ValueError(f"Error al deserializar Consulta: {e}")
