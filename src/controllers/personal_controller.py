"""
Controlador responsable de la gestion del personal medico y administrativo

"""
from datetime import date
from typing import List
from src.utils.persistencia import Persistencia
from src.utils.excepciones import ValidationException, EstadoInvalidoException
from src.utils.validaciones import Validaciones
from src.models.personal import Personal
from src.models.contrato import Contrato
from src.utils.helpers import Helpers
from src.config.constantes import ESPECIALIDADES, TURNOS, JORNADAS

class PersonalController:
    """
    Clase "controlador" encargada de la gestion del personal
    
    Orquetas la logica y coordina las interacciones entra las capas:
    Vista, Modelo y Persistencia
    """
    
    def __init__(self):
        """
        Inicializa el controlador personal configurando las rutas de los archivos
        de persistencias necesarios para la gestion del personal
        
        Atributos:
            persistencia (Persistencia): Repositorio de datos para los registros de personal.
            persistencia_contratos (Persistencia): Repositorio de datos para el historial de contratos.
        """
        
        self.persistencia = Persistencia("data/personal.json")
        self.persistencia_contratos = Persistencia("data/contratos.json")

    # ===== OPERACIONES CRUD =====
    def registrar_personal(
            self, 
            dni: str, 
            nombre: str, 
            fecha_nacimiento: date, 
            telefono: str,
            rol: str,
            especialidad: str | None,
            departamentos: List[int],
            jornada: str,
            turno: str | None,
            salario_base: float,
            fecha_contratacion: date,
            tipo: str,
            fecha_fin: date | None
    ) -> dict:
        
        """
        Registra un nuevo miembro del personal junto con su contrato
        
        Args:
            Datos necesarios para crear las instancias
        
        Returns:
            dict: {"exito": bool, "mensaje": str, "id": int | None}
        """
        
        # Creacion de las instancias de forma segura
        try:
            # Verificar unicidad del DNI
            if self._dni_existe(dni):
                return {"exito": False, "mensaje": "El DNI ya existe"}
        
            # Generar ID unico
            id_personal = self._generar_id()
            
            # Crear objeto Personal
            personal = Personal(
                dni=dni,
                nombre=nombre,
                fecha_nacimiento=fecha_nacimiento,
                telefono=telefono,
                id_personal=id_personal,
                rol=rol,
                especialidad=especialidad,
                departamentos=departamentos,
                jornada=jornada,
                turno=turno,
                salario_base=salario_base,
                estado="Activo",
                fecha_contratacion=fecha_contratacion,
                fecha_baja=None,
                motivo_baja=None               
            )
            
            # Crear contrato automaticamente
            contrato_personal = self._crear_contrato_inicial(id_personal, tipo, fecha_contratacion, fecha_fin, salario_base)
            
            # Guardar en persistencia JSON
            self.persistencia.agregar(personal.to_dict())
            self.persistencia_contratos.agregar(contrato_personal.to_dict())
            
            return {
                "exito": True,
                "mensaje": f"Personal registrado exitosamente",
                "id": id_personal
            }

        # Atrapa cualquier error al crear la instancia
        except ValidationException as e:
            return {"exito": False, "mensaje": f"Datos inválidos: {str(e)}", "id": None}
        
        # Atrapa errores inesperados   
        except Exception as e:
            return {"exito": False, "mensaje": f"Error interno del sistema: {str(e)}", "id": None}

    def buscar_por_dni(self, dni: str) -> dict:
        """
        Busca un empleado por su DNI.
        
        Args:
            dni (str): DNI a buscar
        
        Returns:
            dict: {"exito": bool, "mensaje": str, "datos": dict | None}
        """
        # Validar DNI
        if not Validaciones.validar_dni(dni):
            return {"exito": False, "mensaje": "Formato de DNI inválido.", "datos": None}
        
        # Busqueda
        try:
            empleados_data = self.persistencia.leer_todos() 
            
            for data in empleados_data:
                if data.get("dni") == dni:
                    personal_obj = Personal.from_dict(data)
                    
                    return {
                        "exito": True, 
                        "mensaje": "Personal encontrado.", 
                        "datos": personal_obj
                    }
                    
            return {"exito": False, "mensaje": "Personal no encontrado.", "datos": None}
            
        except Exception as e:
            return {"exito": False, "mensaje": f"Error: {str(e)}", "datos": None}

    def modificar_personal(self, id_personal: int, campo_modificar: dict) -> dict:
        """
        Modifica datos de un personal registrado
        
        Args:
            id_personal (int): ID del personal a modificar
            campo_modificar (dict): Nombre del campo a modificar con su nuevo valor

        Returns:
            dict: {"exito": bool, "mensaje": str, "datos": dict | None}
        """
        
        # Validar ID
        if not isinstance(id_personal, int) or id_personal <= 0:
            return {"exito": False, "mensaje": "Formato de ID invalido", "datos": None}
        
        # Obtener datos del personal
        data = self.persistencia.buscar_por_id(id_personal)
        
        if not data:
            return {"exito": False, "mensaje": f"No se encontro un personal con ID {id_personal}", "datos": None}
        
        # Convertir los datos en una instancia
        try:
            personal = Personal.from_dict(data)
        except KeyError as e:
            return {"exito": False, "mensaje": f"Error al buscar el personal: {str(e)}", "datos": None}
        except Exception as e:
            return {"exito": False, "mensaje": f"Error al buscar el personal: {str(e)}", "datos": None}
        
        # Validar nuevo valor segun el campo a modificar
        clave = next(iter(campo_modificar))
        valor = campo_modificar[clave]
        nuevo_campo = {}
        
        if clave == "Agregar departamento":
            try:
                personal.asignar_departamento(valor)
                lista_nueva = personal.departamentos.copy()
                nuevo_campo = {"departamentos": lista_nueva}
                
            except ValidationException as e:
                return {"exito": False, "mensaje": f"Error: {str(e)}", "datos": None}
            except EstadoInvalidoException as e:
                return {"exito": False, "mensaje": f"Error: {str(e)}", "datos": None}

        elif clave == "Eliminar departamento":
            try:
                personal.remover_departamento(valor)
                lista_nueva = personal.departamentos.copy()
                nuevo_campo = {"departamentos": lista_nueva}
            except ValidationException as e:
                return {"exito": False, "mensaje": f"Error: {str(e)}", "datos": None}
            except EstadoInvalidoException as e:
                return {"exito": False, "mensaje": f"Error: {str(e)}", "datos": None}

        elif clave == "Especialidad":
            valor = valor.strip().capitalize()
            if personal.especialidad != "Doctor":
                return {"exito": False, "mensaje": "Solo los Doctores pueden tener especialidades registradas", "datos": None}
            
            if valor not in ESPECIALIDADES:
                return {"exito": False, "mensaje": "Especialidad invalida", "datos": None}
            
            if valor == personal.especialidad:
                return {"exito": False, "mensaje": f"Esta especialidad ya esta registrada para el personal con ID {personal.id_personal}", "datos": None}
    
            nuevo_campo = {"especialidad": valor}
    
        elif clave == "Turno":
            valor = valor.strip().capitalize()
            if personal.jornada != "Por turnos":
                return {"exito": False, "mensaje": "Para modificar un turno el personal debe de tener una jornada de 'Por turnos'", "datos": None}
            
            if valor not in TURNOS:
                return {"exito": False, "mensaje": "Formato de Turno invalido", "datos": None}

            if valor == personal.turno:
                return {"exito": False, "mensaje": "Este turno ya esta registrado para este personal", "datos": None}
            
            nuevo_campo = {"turno": valor}
        
        elif clave == "Jornada":
            valor = valor.strip().capitalize()
            if not isinstance(valor, str):
                return {"exito": False, "mensaje": "Formato de jornada invalido", "datos": None}
            
            if valor not in JORNADAS:
                return {"exito": False, "mensaje": "Jornada invalida", "datos": None}
            
            if valor == personal.jornada:
                return {"exito": False, "mensaje": "Esta jornada ya esta registrada para este personal", "datos": None}
            
            # Si jornada es cambiada a por turnos se valida el turno tambien
            if valor == "Por turnos":
                segundo_valor = campo_modificar["Turno"]
                segundo_valor = segundo_valor.strip().capitalize()

                if segundo_valor not in TURNOS:
                    return {"exito": False, "mensaje": "Formato de Turno invalido", "datos": None}
                
                nuevo_campo = {"jornada": valor, "turno": segundo_valor}
            else:    
                nuevo_campo = {"jornada": valor, "turno": None}
        
        elif clave == "Salario base":
            if not isinstance(valor, (int, float)):
                return {"exito": False, "mensaje": "Formato de salario base invalido", "datos": None}
            
            valor = float(valor)
            
            if valor <= personal.salario_base:
                return {"exito": False, "mensaje": "Politicas del hospital: Para modificar el sueldo de un empleado no puede ser menor o igual a su sueldo base", "datos": None}
    
            if valor > 20000.00:
                return {"exito": False, "mensaje": "Sueldo demasiado elevado para el cargo del personal", "datos": None}
    
            nuevo_campo = {"salario_base": valor}
    
        else:
            return {"exito": False, "mensaje": "Campo a modificar invalido", "datos": None}
        
        # Actualizar datos
        try:
            if self.persistencia.actualizar(id_personal, nuevo_campo):
                # Volvemos a leer para devolver el objeto
                data_final = self.persistencia.buscar_por_id(id_personal)
                if not data_final:
                    return {"exito": True, "mensaje": "Datos actualizados pero no se pudo traerlos de vuelta para mostrarlos", "datos": None}
                
                return {
                    "exito": True, 
                    "mensaje": "Datos actualizados exitosamente", 
                    "datos": Personal.from_dict(data_final)
                }
        except Exception as e:
            return {"exito": False, "mensaje": f"Error al guardar en base de datos: {str(e)}", "datos": None}

        return {"exito": False, "mensaje": "No se pudo realizar la actualización", "datos": None}

    def inactivar_personal(self, id_personal: int, fecha_baja: date, motivo: str) -> dict:
        """
        Inactiva un personal (sin despedir por politcas del hospital)
        
        Args:
            id_personal (int): ID del personal a inactivar
            fecha_baja (date): Fecha de baja
            motivo (str): Motivo de la baja
        
        Raises:
            Exepciones importadas de la Clase Personal
        
        Returns:
            dict: {"exito": bool, "mensaje": str, "id": int | None}
        """
        
        # Validar ID
        if not isinstance(id_personal, int) or id_personal <= 0:
            return {"exito": False, "mensaje": "Formato de ID invalido", "id": None}
        
        # Validar formato de fecha
        if not isinstance(fecha_baja, date):
            return {"exito": False, "mensaje": "Formato de Fecha invalido", "id": None}
        
        if not fecha_baja:
            return {"exito": False, "mensaje": "Formato de fecha invalido", "id": None}
        
        # Buscar registro por ID
        registro_personal = self.persistencia.buscar_por_id(id_personal)
        
        if not registro_personal:
            return {"exito": False, "mensaje": f"No se encontro un personal con el ID: {id_personal}", "id": None}
        
        # Convertir el registro en instancia personal
        try:
            personal_obj = Personal.from_dict(registro_personal)
        except KeyError as e:
            return {"exito": False, "mensaje": f"Error al buscar el personal: {str(e)}", "id": None}
        except Exception as e:
            return {"exito": False, "mensaje": f"Error al buscar el personal: {str(e)}", "id": None}
        
        # Dar de baja al personal
        try:
            personal_obj.inactivar(fecha_baja, motivo)
            
            estado_nuevo = personal_obj.estado
            fecha_baja_nueva = personal_obj.fecha_baja.isoformat() if personal_obj.fecha_baja else personal_obj.fecha_baja
            motivo_nuevo = personal_obj.motivo_baja
            
            campos_actualizar = {"estado": estado_nuevo, "fecha_baja": fecha_baja_nueva, "motivo_baja": motivo_nuevo}
            actualizar_datos = self.persistencia.actualizar(id_personal, campos_actualizar)
            
            if not actualizar_datos:
                return {"exito": False, "mensaje": f"No se pudo inactivar el personal {id_personal}", "id": None}
            
            return {"exito": True, "mensaje": f"Se inactivo el personal con ID '{id_personal}' de forma exitosa", "id": id_personal}
        except ValidationException as e:
            return {"exito": False, "mensaje": f"Error: {str(e)}", "id": None}
        except EstadoInvalidoException as e:
            return {"exito": False, "mensaje": f"Error: {str(e)}", "id": None}
        except Exception as e:
            return {"exito": False, "mensaje": f"{str(e)}", "id": None}

    def listar_activos(self) -> dict:
        """
        Retorna lista de instancias Personal que se encuentren activos
        
        Returns:
            dict: {"exito": bool, "mensaje": str, "datos": []}
        """
        
        # Buscar registros que se encuentren activos
        registros_texto_plano = self.persistencia.buscar({"estado": "Activo"})
        
        # Si no hay registros activos
        if not registros_texto_plano:
            return {"exito": True, "mensaje": "Actualmente no hay Personal activo", "datos": []}
        
        # Se convierte cada registro json en una instancia Personal
        registros_instancias = []
        for registro in registros_texto_plano:
            try:
                objeto = Personal.from_dict(registro)
                registros_instancias.append(objeto)
            except (ValueError, KeyError) as e:
                continue

        if not registros_instancias:
            return {"exito": False, "mensaje": "Los registros activos encontrados están corruptos", "datos": []}
        
        return {"exito": True, "mensaje": f"Se encontraron {len(registros_instancias)} empleados activos", "datos": registros_instancias}

    def listar_por_departamento(self, id_departamento: int) -> dict:
        """
        Retorna una lista de instancias Personal que pertenezcan al departamento ingresado
        
        Returns:
            {"exito": bool, "mensaje": str, "datos": []}
        """
        
        # Validar ID
        if not isinstance(id_departamento, int) or id_departamento <= 0:
            return {"exito": False, "mensaje": "Formato de ID invalido", "datos": []}

        # Buscar registros
        try:
            registros = self.persistencia.leer_todos()
            personal_encontrado = []

            for data in registros:
                departamentos_del_empleado = data.get("departamentos", [])
                
                if id_departamento in departamentos_del_empleado and data.get("estado") == "Activo":
                    try:
                        personal_obj = Personal.from_dict(data)
                        personal_encontrado.append(personal_obj)
                    except Exception as e:
                        continue 

            if not personal_encontrado:
                return {
                    "exito": False, 
                    "mensaje": f"No se encontró personal en el departamento {id_departamento}.", 
                    "datos": []
                }
            return {
                "exito": True, 
                "mensaje": f"Se encontraron {len(personal_encontrado)} empleados.", 
                "datos": personal_encontrado
            }

        except Exception as e:
            return {"exito": False, "mensaje": f"Error al acceder a los datos: {str(e)}", "datos": []}


    # ===== METODOS PRIVADOS =====

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
        Genera un ID de personal unico auto-incremental
        """
        return self.persistencia.generar_id_autoincremental()
    
    def _generar_id_contrato(self) -> int:
        """
        Genera un ID de contrato unico auto-incremental 
        """
        return self.persistencia_contratos.generar_id_autoincremental()
    
    def _crear_contrato_inicial(self, id_personal, tipo, fecha_contratacion, fecha_fin, salario_base) -> Contrato:
        """
        Crea un contrato inicial al momento de registrar un personal
        """
        id_contrato = self._generar_id_contrato()
        
        contrato = Contrato(
            id_contrato=id_contrato,
            id_personal=id_personal,
            tipo=tipo,
            fecha_inicio=fecha_contratacion,
            fecha_fin=fecha_fin,
            salario_base=salario_base,
            estado="Activo"
        )
        
        return contrato