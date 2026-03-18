"""Controlador responsable de la gestion de pacientes"""

from src.utils.persistencia import Persistencia
from datetime import date
from src.utils.excepciones import ValidationException
from src.models.paciente import Paciente
from src.utils.validaciones import Validaciones
from src.models.consulta import Consulta
class PacienteController:
    """
    Clase "controlador" encargada de la gestion de los pacientes
    
    Orquetas la logica y coordina las interacciones entra las capas:
    Vista, Modelo y Persistencia
    """
    # ========== INICIALIZA ==========
    def __init__(self) -> None:
        """
        Inicializa el controlador de Paciente configurando la ruta del archivo
        de persistencia
        
        Atributos:
            persistencia (Persistencia): Repositorio de datos para el registro de los pacientes
            persistencia_consultas (Persistencia): Repositorio de datos para las consultas de los pacientes
        """
        self.persistencia = Persistencia("data/pacientes.json")
        self.persistencia_consultas = Persistencia("data/consultas.json")
    
    # ========== OPERACIONES CRUD ==========
    def registrar_paciente(
        self, 
        dni: str,
        nombre: str,
        fecha_nacimiento: date,
        telefono: str,
        tipo_seguro: str,
        fecha_registro: date
    ) -> dict:
        
        """
        Registra nuevo paciente en el sistema
        
        Args:
            Datos necesarios para crear la instancia
        
        Returns:
            dict: {"exito": bool, "mensaje": texto, id: int | None}
        """
        
        # Crear la instancia
        try:
            # Verificar unicidad del DNI
            if self._dni_existe(dni):
                return {"exito": False, "mensaje": "El DNI ya existe", "id": None}
            
            # Generar ID unico de Paciente
            id_paciente = self._generar_id()
            
            # Crear objeto Paciente
            paciente = Paciente(
                dni=dni, 
                nombre=nombre,
                fecha_nacimiento=fecha_nacimiento,
                telefono=telefono,
                id_paciente=id_paciente,
                tipo_seguro=tipo_seguro,
                fecha_registro=fecha_registro
            )
            
            # Guardar en Persistencia JSON
            self.persistencia.agregar(paciente.to_dict())
            
            # Devolver exito
            return {"exito": True, "mensaje": "Paciente registrado exitosamente", "id": id_paciente}
        
        # Atrapa errores al crear la instancia
        except ValidationException as e:
            return {"exito": False, "mensaje": f"Datos inválidos: {str(e)}", "id": None}
        
        # Atrapa errores inesperados
        except Exception as e:
            return {"exito": False, "mensaje": f"Error interno del sistema: {str(e)}", "id": None}
    
    def buscar_por_dni(self, dni: str) -> dict:
        """
        Busca un Paciente por su DNI.
        
        Args:
            dni (str): DNI a buscar
        
        Returns:
            dict: {"exito": bool, "mensaje": str, "datos": dict | None}
        """

        # Validar DNI
        if not Validaciones.validar_dni(dni):
            return {"exito": False, "mensaje": "DNI invalido", "datos": None}

        # Buscar Paciente
        try:   
            datos = self.persistencia.leer_todos()
            
            for pac in datos:
                if pac.get("dni") == dni:
                    obj_encontrado = Paciente.from_dict(pac)
                    return {"exito": True, "mensaje": "Paciente encontrado", "datos": obj_encontrado}
            
            return {"exito": False, "mensaje": "Paciente no encontrado", "datos": None}
            
        except Exception as e:
            return {"exito": False, "mensaje": f"Error: {str(e)}", "datos": None}

    def buscar_por_id(self, id_paciente: int) -> dict:
            """
            Busca un Paciente por su ID único.
            
            Args:
                id_paciente (int): ID a buscar
            
            Returns:
                dict: {"exito": bool, "mensaje": str, "datos": Paciente | None}
            """

            # Validar ID 
            if not isinstance(id_paciente, int) or id_paciente <= 0:
                return {"exito": False, "mensaje": "ID invalido. Debe ser un numero entero positivo", "datos": None}

            # Buscar Paciente
            try:   
                pac = self.persistencia.buscar_por_id(id_paciente)
                
                if pac:
                    obj_encontrado = Paciente.from_dict(pac)
                    return {
                        "exito": True, 
                        "mensaje": "Paciente encontrado exitosamente", 
                        "datos": obj_encontrado
                    }
                
                return {
                    "exito": False, 
                    "mensaje": f"No se encontro ningun paciente con el ID {id_paciente}", 
                    "datos": None
                }
                
            except Exception as e:
                return {
                    "exito": False, 
                    "mensaje": f"Error inesperado en el controlador: {str(e)}", 
                    "datos": None
                }

    def modificar_paciente(self, id_paciente: int, campo_modificar: dict) -> dict:
        """
        Modifica datos de un Paciente registrado
        
        Args:
            id_paciente (int): ID del paciente a modificar
            campo_modificar (dict): Nombre del campo a modificar con su nuevo valor

        Returns:
            dict: {"exito": bool, "mensaje": str, "datos": dict | None}
        """

        # Validar ID
        if not isinstance(id_paciente, int) or id_paciente <= 0:
            return {"exito": False, "mensaje": "Formato de ID invalido", "datos": None}

        # Buscar Paciente
        encontrado = self.persistencia.buscar_por_id(id_paciente)
        
        if not encontrado:
            return {"exito": False, "mensaje": f"No se encontro un paciente con el ID ({id_paciente})", "datos": None}

        # Convertir los datos en una instancia
        try:
            obj_paciente = Paciente.from_dict(encontrado)
        except KeyError as e:
            return {"exito": False, "mensaje": f"Error al buscar el paciente: {str(e)}", "datos": None}
        except Exception as e:
            return {"exito": False, "mensaje": f"Error al buscar el paciente: {str(e)}", "datos": None}

        # Extraer campo a modificar y nuevo valor
        campo = next(iter(campo_modificar))
        nuevo_valor = campo_modificar[campo]
        nuevo_campo = {}
        
        # Campos modificables
        if campo == "seguro":
            # Cambiar seguro
            try:
                obj_paciente.cambiar_tipo_seguro(nuevo_valor)
            except ValidationException as e:
                return {"exito": False, "mensaje": f"{str(e)}", "datos": None}
        
            nuevo_campo = {"tipo_seguro": obj_paciente.tipo_seguro, "porcentaje_descuento": obj_paciente.porcentaje_descuento}
        
        elif campo == "nombre":
            # Validaciones
            if not nuevo_valor:
                return {"exito": False, "mensaje": "El nombre no puede estar vacio", "datos": None}
            
            if not isinstance(nuevo_valor, str):
                return {"exito": False, "mensaje": "El nombre debe ser texto", "datos": None}
            nuevo_valor = nuevo_valor.strip().title()
            
            if not Validaciones.validar_nombre(nuevo_valor, 3, 100):
                return {"exito": False, "mensaje": "Formato de nombre invalido", "datos": None}

            # Nuevo campo
            nuevo_campo = {"nombre": nuevo_valor}
        
        elif campo == "telefono":
            # Validaciones
            if not Validaciones.validar_telefono(nuevo_valor):
                return {"exito": False, "mensaje": "Numero de telefono invalido", "datos": None}
            
            # Nuevo campo
            nuevo_campo = {"telefono": nuevo_valor}
        
        else:
            return {"exito": False, "mensaje": "Campo a modificar invalido", "datos": None}
        
        # Actualizar datos
        try:
            if self.persistencia.actualizar(id_paciente, nuevo_campo):
                data_final = self.persistencia.buscar_por_id(id_paciente)
                if not data_final:
                    return {"exito": True, "mensaje": "Datos actualizados pero no se puso acceder de vuelta para mostrarlos", "datos": None}
                
                return {"exito": True, "mensaje": "Datos actualizados exitosamente", "datos": Paciente.from_dict(data_final)}
        except Exception as e:
            return {"exito": False, "mensaje": f"Error al guardar en base de datos: {str(e)}", "datos": None}

        return {"exito": False, "mensaje": "No se pudo realizar la actualización", "datos": None}    

    def obtener_historial(self, id_paciente: int) -> dict:
        """
        Busca el historial de un paciente
        Accediendo al archivo de Persistencia de consultas y filtrando por ID
        
        Args:
            id_paciente (int): ID del paciente
        
        Returns:
            dict: {"exito": bool, "mensaje": str, "datos": list | None}
        """
        
        # Validar ID
        if not isinstance(id_paciente, int) or id_paciente <= 0:
            return {"exito": False, "mensaje": "Formato de ID invalido", "datos": None}
    
        # Obtener consultas
        try:
            consultas = self.persistencia_consultas.leer_todos()    
        except Exception as e:
            return {"exito": False, "mensaje": f"{str(e)}", "datos": None}

        if not consultas:
            return {"exito": False, "mensaje": "No se han registrados consultas en el sistema", "datos": None}
    
        # Filtrar por ID
        consultas_encontradas = []
        
        for consulta in consultas:
            if consulta.get("id_paciente") == id_paciente:
                try:
                    consulta_agregar = Consulta.from_dict(consulta)
                    consultas_encontradas.append(consulta_agregar)
                except (Exception, KeyError) as e:
                    print(f"Consulta corrupta ignorada: {e}")
                    continue
    
        if not consultas_encontradas:
            return {"exito": False, "mensaje": "No se encontro un historial para el paciente", "datos": None}

        return {"exito": True, 
                "mensaje": f"Historial encontrado, numero de consultas ({len(consultas_encontradas)})", 
                "datos": consultas_encontradas}
    
    def listar_pacientes(self) -> dict:
        """
        Lista todos los pacientes registrados.
        
        Returns:
            dict: {"exito": bool, "mensaje": str, "datos": list}
        """
        try:
            datos = self.persistencia.leer_todos()
            
            if not datos:
                return {
                    "exito": False,
                    "mensaje": "No hay pacientes registrados",
                    "datos": None
                }
            
            pacientes = [Paciente.from_dict(p) for p in datos]
            
            return {
                "exito": True,
                "mensaje": f"Se encontraron {len(pacientes)} pacientes",
                "datos": pacientes
            }
        
        except Exception as e:
            return {
                "exito": False,
                "mensaje": f"Error: {str(e)}",
                "datos": None
            }

    # ========== METODOS PRIVADOS ==========
    def _dni_existe(self, dni: str) -> bool:
        """
        Evalua si un DNI esta registrado en el sistema
        
        Args:
            dni (str): DNI a buscar
            
        Returns:
            bool: True si esta registrado | False si no lo esta
        """
        # Traer registros
        registros = self.persistencia.leer_todos()
        
        # Devuelve True si al menos uno cumple la condicion
        return any(personal.get("dni") == dni for personal in registros)
    
    def _generar_id(self) -> int:
        """
        Genera un ID de Paciente unico auto-incremental
        """
        return self.persistencia.generar_id_autoincremental()