"""
Responsable de la gestion de citas medicas

"""
from src.utils.persistencia import Persistencia
from datetime import date, time, datetime
from src.models.cita import Cita
from src.utils.excepciones import ValidationException
from src.config.constantes import ESTADOS_CITA

class CitaController:
    """
    Clase "controlador" encargada de la gestion de las citas medicas
    
    Orqueta la logica y coordina las interacciones entra las capas:
    Vista, Modelo y Persistencia
    """
    
    # ========== INICIALIZA ==========
    def __init__(self) -> None:
        """
        Inicializa el controlador de Citas configurando la ruta del archivo
        de persistencia
        
        Atributos:
            persistencia (Persistencia): Repositorio de datos para el registro de las citas
            persistencia_personal (Persistencia): Repositorio de datos para evaluar la disponibilidad del personal
            persistencia_paciente (Persistencia): Repositorio de datos para evaluar existencia de pacientes
        """
        self.persistencia = Persistencia("data/citas.json")
        self.persistencia_personal = Persistencia("data/personal.json")
        self.persistencia_paciente = Persistencia("data/pacientes.json")

    # ========== OPERACIONES CRUD ==========
    def agendar_cita(
        self,
        id_paciente: int,
        id_doctor: int,
        fecha: date,
        hora: time,
        motivo: str,
    ) -> dict:
        
        """
        Agenda una cita para un paciente
        
        Args:
            Datos necesarios para la creacion de la instancia Cita
        
        Returns:
            dict: {"exito": bool, "mensaje": str, "datos": dict | None}
        """

        # Validar IDs 
        if not isinstance(id_paciente, int) or id_paciente <= 0:
            return {"exito": False, "mensaje": "Formato de ID de paciente invalido. Debe ser un numero entero positivo", "datos": None}
        
        if not isinstance(id_doctor, int) or id_doctor <= 0:
            return {"exito": False, "mensaje": "Formato de ID de Doctor invalido. Debe ser un numero entero positivo", "datos": None}
        
        # Validar fecha y hora
        if not isinstance(fecha, date):
            return {"exito": False, "mensaje": "Formato de fecha invalido. Debe ser tipo fecha mayor o igual a la actual", "datos": None}
        
        if not isinstance(hora, time):
            return {"exito": False, "mensaje": "Formato de hora invalido. Debe ser de tipo hora/time", "datos": None}
        
        if not (time(7, 0) <= hora < time(22, 0)):
            return {"exito": False, "mensaje": "Hora invalida. Debe de ser entre 7:00AM y 10:00PM", "datos": None}

        momento_cita = datetime.combine(fecha, hora)
        if momento_cita < datetime.now():
            return {"exito": False, "mensaje": "La fecha y hora de la cita no pueden ser en el pasado", "datos": None}

        # Verificar existencia del paciente
        try:
            paciente_encontrado = self.persistencia_paciente.buscar_por_id(id_paciente)
            
            if paciente_encontrado is None:
                return {"exito": False, "mensaje": f"No se encuentra registrado un paciente con el ID {id_paciente}", "datos": None}
        except Exception as e:
            return {"exito": False, "mensaje": f"{str(e)}", "id": None}
        
        # Verificar existencia del doctor
        try:
            doctor_encontrado = self.persistencia_personal.buscar_por_id(id_doctor)
            
            if doctor_encontrado is None:
                return {"exito": False, "mensaje": f"No se encuentra registrado un doctor con el ID {id_doctor}", "datos": None}
            
            # Verificar que este activo
            if doctor_encontrado["estado"] != "Activo":
                return {"exito": False, "mensaje": f"El doctor seleccionado no se encuentra activo en el hospital", "datos": None}
        except Exception as e:
            return {"exito": False, "mensaje": f"{str(e)}", "id": None}
        
        # Verificar disponibilidad del doctor
        if not self._doctor_disponible(id_doctor, fecha, hora):
            return {"exito": False, "mensaje": f"El doctor ya tiene una cita agendada en ese horario", "datos": None}

        # Crear instancia Cita
        try: 
            id_cita = self._generar_id()
            
            cita = Cita(
                id_cita=id_cita,
                id_paciente=id_paciente,
                id_doctor=id_doctor,
                fecha=fecha,
                hora=hora,
                especialidad=doctor_encontrado["especialidad"],
                motivo=motivo,
                validar_fecha_futura = True
            )
            
            # Agregar a persistencia
            self.persistencia.agregar(cita.to_dict())
            
            # Exito
            datos = {
                "paciente": paciente_encontrado["nombre"],
                "doctor": doctor_encontrado["nombre"],
                "especialidad": doctor_encontrado["especialidad"],
                "fecha": fecha,
                "hora": hora,
                "motivo": motivo
            }
            
            return {"exito": True, "mensaje": f"Cita agendada exitosamente. ID: {id_cita}", "datos": datos}
            
        # Atrapa errores al crear la instancia
        except ValidationException as e:
            return {"exito": False, "mensaje": f"Datos inválidos: {str(e)}", "datos": None}
        
        # Atrapa errores inesperados
        except Exception as e:
            return {"exito": False, "mensaje": f"Error interno del sistema: {str(e)}", "datos": None}

    def reprogramar_cita(self, id_cita: int, usuario: int, nueva_fecha: date | None = None, nueva_hora: time | None = None) -> dict:
        """
        Reprograma una cita (ya registrada)
        
        Args:
            id_cita (int): ID de la cita a reprogramar
            nueva_fecha (date): Fecha nueva de la cita
            hora (time): Hora nueva de la cita
            usuario (int): ID del recepcionista que realizo el cambio
        
        Returns:
            dict: {"exito": bool, "mensaje": str, "datos": dict | None}
        """

        # Validar IDs
        if not isinstance(id_cita, int) or id_cita <= 0:
            return {"exito": False, "mensaje": "Formato de ID de cita invalido. Debe ser un numero entero positivo", "datos": None}

        if not isinstance(usuario, int) or usuario <= 0:
            return {"exito": False, "mensaje": "Formato de ID de personal invalido. Debe ser un numero entero positivo", "datos": None}
        
        # Buscar cita
        try:
            cita_encontrada = self.persistencia.buscar_por_id(id_cita)
            
            if cita_encontrada is None:
                return {"exito": False, "mensaje": f"No se encontro una cita registrada con el ID {id_cita}", "datos": None}
            
            # Recrear instancia
            obj_cita = Cita.from_dict(cita_encontrada)
            
        except (KeyError, Exception) as e:
            return {"exito": False, "mensaje": f"{str(e)}", "datos": None}
        
        # Validar estado
        if obj_cita.estado != "Agendada":
            return {"exito": False, "mensaje": f"Cambio invalido. El estado actual de cita es {obj_cita.estado}", "datos": None}
        
        # Validar que el personal responsable exista
        try:
            personal_encontrado = self.persistencia_personal.buscar_por_id(usuario)
            
            if personal_encontrado is None:
                return {"exito": False, "mensaje": f"No se encontro un personal registrado con ID {usuario}", "datos": None}
        except Exception as e:
            return {"exito": False, "mensaje": f"{str(e)}", "datos": None}

        # Asignar valor segun opcion
        if nueva_fecha is None:
            nueva_fecha = obj_cita.fecha
        
        if nueva_hora is None:
            nueva_hora = obj_cita.hora

        # Validar fecha y hora
        if not isinstance(nueva_fecha, date):
            return {"exito": False, "mensaje": "Formato de fecha invalido. Debe ser tipo fecha mayor o igual a la actual", "datos": None}
        
        if not isinstance(nueva_hora, time):
            return {"exito": False, "mensaje": "Formato de hora invalido. Debe ser de tipo hora/time", "datos": None}
        
        if not (time(7, 0) <= nueva_hora < time(22, 0)):
            return {"exito": False, "mensaje": "Hora invalida. Debe de ser entre 7:00AM y 10:00PM", "datos": None}

        momento_cita = datetime.combine(nueva_fecha, nueva_hora)
        if momento_cita < datetime.now():
            return {"exito": False, "mensaje": "La fecha y hora de la cita no pueden ser en el pasado", "datos": None}

        # Validar disponibilidad del doctor en el nuevo horario
        if not self._doctor_disponible(obj_cita.id_doctor, nueva_fecha, nueva_hora):
            return {"exito": False, "mensaje": "El doctor ya tiene agendada una cita en este horario", "datos": None}

        # Reprogramar cita
        try:
            obj_cita.reprogramar(nueva_fecha, nueva_hora, usuario)
        except ValidationException as e:
            return {"exito": False, "mensaje": f"{str(e)}", "datos": None}

        # Actualizar persistencia
        try:
            datos_actualizados = obj_cita.to_dict()
            self.persistencia.actualizar(obj_cita.id_cita, datos_actualizados)
            
        except Exception as e:
            return {"exito": False, "mensaje": f"{str(e)}", "datos": None}
        
        # Exito
        datos = {
            "fecha": obj_cita.fecha,
            "hora": obj_cita.hora
        }

        return {"exito": True, "mensaje": f"Cita reprogramada exitosamente", "datos": datos}

    def cancelar_cita(self, id_cita: int) -> dict:
        """
        Cancela una cita (Registrada previamente como Agendada)
        
        Args:
            id_cita (int): ID de la cita a cancelar
        
        Returns:
            dict: {"exito": bool, "mensaje": str, "id": int | None}
        """

        # Validar ID
        if not isinstance(id_cita, int) or id_cita <= 0:
            return {"exito": False, "mensaje": "Formato de ID de Cita invalido. Debe ser un numero entero positivo", "id": None}
        
        # Buscar Cita
        try:
            cita_encontrada = self.persistencia.buscar_por_id(id_cita)
            
            if cita_encontrada is None:
                return {"exito": False, "mensaje": f"No se encontro una cita registrada con el ID {id_cita}", "id": None}
            
            # Recrear la instancia
            obj_cita = Cita.from_dict(cita_encontrada)
            
        except (KeyError, Exception) as e:
            return {"exito": False, "mensaje": f"{str(e)}", "id": None}

        # Validar estado
        if obj_cita.estado != "Agendada":
            return {"exito": False, "mensaje": f"Cambio invalido. Estado de la cita: {obj_cita.estado}", "id": None}
        
        # Cancelar cita
        obj_cita.cancelar()
        
        # Actualizar persistencia
        cita_actualizada = obj_cita.to_dict()
        try:
            self.persistencia.actualizar(obj_cita.id_cita, cita_actualizada)
        except Exception as e:
            return {"exito": False, "mensaje": f"{str(e)}", "id": None}

        # Exito
        return {"exito": True, "mensaje": "Cita cancelada exitosamente", "id": obj_cita.id_cita}

    def buscar_por_id(self, id_cita: int) -> dict:
        """
        Busca una cita específica por su ID
        
        Args:
            id_cita (int): ID de la cita a buscar
            
        Returns:
            dict: {"exito": bool, "mensaje": str, "datos": Cita | None}
        """
        
        # Validar ID
        if not isinstance(id_cita, int) or id_cita <= 0:
            return {
                "exito": False, 
                "mensaje": "Formato de ID de cita inválido. Debe ser un número entero positivo.", 
                "datos": None
            }

        # Buscar cita
        try:
            cita_encontrada = self.persistencia.buscar_por_id(id_cita)
            
            if cita_encontrada is None:
                return {
                    "exito": False, 
                    "mensaje": f"No se encontró ninguna cita registrada con el ID {id_cita}", 
                    "datos": None
                }
            
            obj_cita = Cita.from_dict(cita_encontrada)
            
            return {
                "exito": True, 
                "mensaje": "Cita localizada con éxito", 
                "datos": obj_cita
            }

        except (KeyError, Exception) as e:
            return {
                "exito": False, 
                "mensaje": f"Error al recuperar la cita: {str(e)}", 
                "datos": None
            }

    def listar_citas_dia(self, fecha: date) -> dict:
        """
        Lista todas las citas de un dia especifico
        
        Args:
            fecha (date): Dia a buscar
        
        Returns:
            dict: {"exito": bool, "mensaje": str, "datos": list}
        """

        # Validar fecha
        if not isinstance(fecha, date):
            return {"exito": False, "mensaje": "Formato de fecha invalido. Debe ser de tipo date", "datos": []}

        # Buscar citas
        try:
            citas_encontradas = self.persistencia.buscar({"fecha": fecha})
            
            if not citas_encontradas:
                return {"exito": False, "mensaje": f"No se encontraron citas para la fecha {fecha}", "datos": []}
            
        except Exception as e:
            return {"exito": False, "mensaje": f"{str(e)}", "datos": []}

        # Convertir a instancias
        datos = []
        for cita in citas_encontradas:
            try:
                cita_agregar = Cita.from_dict(cita)
                datos.append(cita_agregar)
            except (KeyError, Exception) as e:
                print(f"Cita corrupta ignorada: {e}")
                continue
        
        # Datos corruptos
        if not datos:
            return {"exito": False, "mensaje": f"No se pudo acceder a las citas del dia {fecha}", "datos": []}                 

        # Exito
        return {"exito": True, "mensaje": f"Citas del dia {fecha} encontradas con exito", "datos": datos}

    def listar_citas_doctor(self, id_doctor: int, estado: str | None = None) -> dict:
        """
        Lista las citas de un doctor ordenadas por fecha (opcionalmente por estado)
        
        Args:
            id_doctor (int): ID del doctor
            estado (str | None): Estado (opcional) a buscar
        
        Returns:
            dict: {"exito": bool, "mensaje": str, "datos": list}
        """
        
        # Validar ID
        if not isinstance(id_doctor, int) or id_doctor <= 0:
            return {"exito": False, "mensaje": "Formato de ID invalido. Debe ser un numero entero positivo", "datos": []}
        
        # Validar estado
        if estado is not None:
            if not estado:
                return {"exito": False, "mensaje": "Estado invalido. No puede estar vacio", "datos": []}
            
            if not isinstance(estado, str):
                return {"exito": False, "mensaje": "Estado invalido. Debe ser texto", "datos": []}
            
            estado = estado.strip().capitalize()
            
            if estado not in ESTADOS_CITA:
                return {"exito": False, "mensaje": "Estado invalido. Debe ser Agendada, Cancelada o Completada", "datos": []}        
        
        # Buscar doctor
        try:
            doctor_encontrado = self.persistencia_personal.buscar_por_id(id_doctor)
            
            if doctor_encontrado is None:
                return {"exito": False, "mensaje": f"No se encontro ningun doctor registrado con el ID {id_doctor}", "datos": []}
        except Exception as e:
            return {"exito": False, "mensaje": f"{str(e)}", "datos": []}
        
        # Buscar citas
        citas_encontradas = []
        try:
            if estado is None:
                citas_encontradas = self.persistencia.buscar({"id_doctor": doctor_encontrado["id_personal"]})
            else:
                citas_encontradas = self.persistencia.buscar({"id_doctor": doctor_encontrado["id_personal"], "estado": estado})
        except Exception as e:
            return {"exito": False, "mensaje": f"{str(e)}", "datos": []}
        
        if not citas_encontradas:
            return {"exito": False, "mensaje": f"No se encontraron citas para el doctor {doctor_encontrado['nombre']}", "datos": []}
        
        # Convertir a instancias
        datos = []
        for cita in citas_encontradas:
            try:
                obj_cita = Cita.from_dict(cita)
                datos.append(obj_cita)
            except (KeyError, Exception) as e:
                print(f"Cita corrupta ignorada: {e}")
                continue
        
        # Datos corruptos
        if not datos:
            return {"exito": False, "mensaje": f"No se pudo acceder a las citas del doctor {doctor_encontrado['nombre']}", "datos": []}

        try:
            datos.sort(key=lambda cita: (cita.fecha, cita.hora))
        except AttributeError:
            print("Advertencia: No se pudo ordenar por fecha. Verifica el nombre del atributo.")

        # Exito
        return {"exito": True, "mensaje": "Consultas encontradas de manera exitosa", "datos": datos}

    def listar_agenda_actual_doctor(self, id_doctor: int, estado) -> dict:
        """
        Lista las citas de un doctor para el día de hoy filtradas por estado
        
        Args:
            id_doctor (int): ID del doctor
            estado (str): Estado a filtrar 
        
        Returns:
            dict: {"exito": bool, "mensaje": str, "datos": list}
        """
        # Validar ID
        if not isinstance(id_doctor, int) or id_doctor <= 0:
            return {"exito": False, "mensaje": "ID de doctor inválido", "datos": []}
        
        # Validar estado
        estado = estado.strip().capitalize()
        if estado not in ESTADOS_CITA:
            return {"exito": False, "mensaje": f"Estado '{estado}' no reconocido", "datos": []}

        # Definir fecha actual
        fecha_hoy = date.today()

        try:
            # Buscar en Persistencia
            doctor_encontrado = self.persistencia_personal.buscar_por_id(id_doctor)
            if not doctor_encontrado:
                return {"exito": False, "mensaje": f"No se encontró al doctor con ID {id_doctor}", "datos": []}
            
            # Busqueda con triple filtro
            citas_data = self.persistencia.buscar({
                "id_doctor": id_doctor,
                "estado": estado,
                "fecha": fecha_hoy.isoformat()
            })

            if not citas_data:
                return {
                    "exito": False, 
                    "mensaje": f"No hay citas {estado.lower()}s para el Dr. {doctor_encontrado['nombre']} el día de hoy.", 
                    "datos": []
                }

            # Conversion
            instancias_citas = []
            for data in citas_data:
                try:
                    obj_cita = Cita.from_dict(data)
                    instancias_citas.append(obj_cita)
                except Exception:
                    continue # Ignorar registros corruptos

            # Ordenar por hora
            instancias_citas.sort(key=lambda x: x.hora)

            return {
                "exito": True,
                "mensaje": f"Agenda de hoy para el Dr. {doctor_encontrado['nombre']} recuperada.",
                "datos": instancias_citas
            }

        # Captura de errores de estructura o lectura
        except Exception as e:
            return {"exito": False, "mensaje": f"Error al consultar la agenda: {str(e)}", "datos": []}

    def listar_proximas_citas_doctor(self, id_doctor: int, estado: str) -> dict:
        """
        Lista las citas de un doctor de mañana en adelante, filtradas por estado
        
        Args:
            id_doctor (int): ID del doctor
            estado (str): Estado a filtrar (Agendada, Cancelada)
        
        Returns:
            dict: {"exito": bool, "mensaje": str, "datos": list}
        """
        # Validar ID
        if not isinstance(id_doctor, int) or id_doctor <= 0:
            return {"exito": False, "mensaje": "ID de doctor inválido", "datos": []}
        
        # Validar estado
        estado = estado.strip().capitalize()
        if estado not in ESTADOS_CITA:
            return {"exito": False, "mensaje": f"Estado '{estado}' no reconocido", "datos": []}

        # Obtener fecha
        hoy = date.today()

        try:
            # Buscar en Persistencia
            doctor_encontrado = self.persistencia_personal.buscar_por_id(id_doctor)
            if not doctor_encontrado:
                return {"exito": False, "mensaje": f"No se encontró al doctor con ID {id_doctor}", "datos": []}
            
            # Condicion a buscar citas
            citas_data = self.persistencia.buscar({
                "id_doctor": id_doctor,
                "estado": estado
            })

            # Conversion
            instancias_proximas = []
            for data in citas_data:
                try:
                    obj_cita = Cita.from_dict(data)
                    # FILTRO: Solo si la fecha es estrictamente mayor a hoy
                    if obj_cita.fecha > hoy:
                        instancias_proximas.append(obj_cita)
                except Exception:
                    continue 

            if not instancias_proximas:
                return {
                    "exito": False, 
                    "mensaje": f"No hay citas {estado.lower()}s futuras para el Dr. {doctor_encontrado['nombre']}.", 
                    "datos": []
                }

            # Ordenamiento por fecha y luego por hora
            instancias_proximas.sort(key=lambda x: (x.fecha, x.hora))

            return {
                "exito": True,
                "mensaje": f"Citas futuras del Dr. {doctor_encontrado['nombre']} recuperadas.",
                "datos": instancias_proximas
            }

        except Exception as e:
            return {"exito": False, "mensaje": f"Error al consultar citas futuras: {str(e)}", "datos": []}
    
    def listar_citas_pendientes_paciente(self, id_paciente: int) -> dict:  
        """
        Busca todas las citas con estado 'Agendada' de un paciente específico
        
        Args:
            id_paciente (int): ID del paciente a consultar
            
        Returns:
            dict: {"exito": bool, "mensaje": str, "datos": list[Cita]}
        """
        
        # Validar ID
        if not isinstance(id_paciente, int) or id_paciente <= 0:
            return {"exito": False, "mensaje": "ID de paciente inválido", "datos": []}

        try:
            # Buscar en persistencia por ID de paciente y estado
            citas_data = self.persistencia.buscar({
                "id_paciente": id_paciente,
                "estado": "Agendada"
            })

            if not citas_data:
                return {
                    "exito": False, 
                    "mensaje": "El paciente no tiene citas pendientes de atención", 
                    "datos": []
                }

            # Convertir diccionarios a instancias de Cita
            lista_instancias = []
            for item in citas_data:
                try:
                    lista_instancias.append(Cita.from_dict(item))
                except Exception as e:
                    print(f"Error al procesar cita ID {item.get('id_cita')}: {e}")
                    continue

            # 4. Ordenar por fecha y hora
            lista_instancias.sort(key=lambda x: (x.fecha, x.hora))

            return {
                "exito": True,
                "mensaje": f"Se encontraron {len(lista_instancias)} citas pendientes",
                "datos": lista_instancias
            }

        except Exception as e:
            return {"exito": False, "mensaje": f"Error al buscar citas: {str(e)}", "datos": []}
    
    # ========== METODOS PRIVADOS ==========
    def _doctor_disponible(self, id_doctor: int, fecha: date, hora: time) -> bool:
        """
        Verifica si el doctor está disponible en fecha/hora específica.
        
        Returns:
            bool: True si está disponible, False si tiene cita o hubo error
        """
        try:
            citas_doctor = self.persistencia.buscar({
                "id_doctor": id_doctor,
                "fecha": fecha.isoformat(),
                "hora": hora.isoformat(),
                "estado": "Agendada"
            })
            
            return len(citas_doctor) == 0
        
        except Exception as e:
            # En caso de error asumir no disponible
            print(f"Error al verificar disponibilidad: {e}")
            return False

    def _generar_id(self) -> int:
        """
        Genera un ID de Cita unico auto-incremental
        """
        return self.persistencia.generar_id_autoincremental()