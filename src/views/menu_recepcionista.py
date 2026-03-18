"""
Menu para el rol de Recepcionista
Gestiona Pacientes y Citas
"""
from src.controllers.paciente_controller import PacienteController
from src.controllers.cita_controller import CitaController
from src.controllers.personal_controller import PersonalController
from src.controllers.facturacion_controller import FacturacionController
from src.controllers.inventario_controller import InventarioController
from src.utils.helpers import Helpers
from src.views.componentes.inputs import Entradas
from src.views.componentes.mensajes import Mensajes
from src.views.componentes.tablas import Tablas
from src.config.constantes import TIPOS_SEGURO, ESPECIALIDADES
from datetime import date
class MenuRecepcionista:
    """Menu principal de Recepcionista"""
    
    # ========== INICIALIZA ==========
    def __init__(self) -> None:
        """Inicializa el menu con los controladores de Pacientes, Citas, Personal, Facturas e Inventario"""
        self.controlador_pacientes = PacienteController()
        self.controlador_citas = CitaController()
        self.controlador_personal = PersonalController()
        self.controlador_facturas = FacturacionController()
        self.controlador_inventario = InventarioController()
    
    # ========== MENU PRINCIPAL ==========
    def mostrar(self):
        """Muestra el menu y maneja las opciones"""
        while True:
            Helpers.limpiar_pantalla()
            print("═" * 50)
            print("    MENÚ RECEPCIONISTA")
            print("═" * 50)
            print("\nGESTIÓN DE PACIENTES:")
            print("1. Registrar nuevo paciente")
            print("2. Buscar paciente")
            print("3. Modificar datos de paciente")
            print("4. Consultar historial clínico")
            print("\nGESTIÓN DE CITAS:")
            print("5. Agendar nueva cita")
            print("6. Reprogramar cita")
            print("7. Cancelar cita")
            print("8. Consultar citas del día")
            print("\nFACTURACIÓN:")
            print("9. Registrar pago de factura")
            print("10. Consultar facturas pendientes")
            print("\nCONSULTAS:")
            print("11. Ver inventario de medicamentos")   
            print("\n0. Cerrar sesión")
            print("═" * 50)
            
            # Pedir opcion y validar
            opcion = Entradas.pedir_entero("\nSeleccione una opcion", 0, 11)
            
            # Opciones
            if opcion == 1:
                self.registrar_paciente()
            elif opcion == 2:
                self.buscar_paciente()
            elif opcion == 3:
                self.modificar_paciente()
            elif opcion == 4:
                self.consultar_historial()
            elif opcion == 5:
                self.agendar_nueva_cita()
            elif opcion == 6:
                self.reprogramar_cita()
            elif opcion == 7:
                self.cancelar_cita()
            elif opcion == 8:
                self.citas_del_dia()
            elif opcion == 9:
                self.registrar_pago_factura()
            elif opcion == 10:
                self.consultar_facturas()
            elif opcion == 11:
                self.inventario_medicamentos()
            elif opcion == 0:
                print("\nCerrando sesion de Recepcionista...")
                Helpers.pausar()
                break
    
    # ========= GESTION DE PACIENTES ==========
    def registrar_paciente(self):
        """Opcion 1: Registrar nuevo Paciente"""
        Helpers.limpiar_pantalla()
        print("=" * 50)
        print("     REGISTRAR NUEVO PACIENTE")
        print("=" * 50)
        
        try:
            # Datos personales
            print("\n--- DATOS PERSONALES ---")
            dni = Entradas.pedir_texto("DNI (8 digitos)")
            nombre = Entradas.pedir_texto("Nombre completo")
            fecha_nacimiento = Entradas.pedir_fecha("Fecha de nacimiento")
            telefono = Entradas.pedir_texto("Telefono (9 digitos empezando en 9)")
            
            # Tipo de seguro
            print("\n--- TIPO DE SEGURO ---")
            print("\nSeguros Permitidos:")
            for nombre_seguro, costo in TIPOS_SEGURO.items():
                print(f"    Seguro: {nombre_seguro} - Descuento: {costo}%")
            tipo_seguro = Entradas.pedir_opcion("Seleccione tipo de seguro", list(TIPOS_SEGURO.keys()))
            
            # Fecha de registro
            print("\n--- FECHA DE REGISTRO ---")
            fecha_registro = Entradas.pedir_fecha("Fecha de registro")
            
            # Mostrar datos ingresados
            print("\n--- DATOS INGRESADOS ---")
            Tablas.mostrar_detalle("DATOS DEL PACIENTE", {
                "DNI": dni,
                "Nombre": nombre,
                "Fecha de nacimiento": fecha_nacimiento,
                "Telefono": telefono,
                "Tipo de seguro": tipo_seguro,
                "Fecha de registro": fecha_registro
            })
            
            # Confirmar
            if not Entradas.confirmar_accion("¿Confirma el registro de este Paciente?"):
                print("\nRegistro cancelado.")
                Helpers.pausar()
                return
            
            # Registrar
            resultado = self.controlador_pacientes.registrar_paciente(
                dni=dni,
                nombre=nombre,
                fecha_nacimiento=fecha_nacimiento,
                telefono=telefono,
                tipo_seguro=tipo_seguro,
                fecha_registro=fecha_registro
            )
            
            # Mostrar resultado
            Mensajes.mostrar(resultado)
            
        except KeyboardInterrupt:
            print("\n\nRegistro cancelado por el usuario.")
            Helpers.pausar()
        except Exception as e:
            Mensajes.mostrar({"exito": False, "mensaje": f"Error inesperado: {str(e)}"})
    
    def buscar_paciente(self):
        """Opcion 2: Buscar Paciente"""
        Helpers.limpiar_pantalla()
        print("=" * 50)
        print("     BUSCAR PACIENTE")
        print("=" * 50)
        
        try:
            # Pedir DNI
            dni_buscar = Entradas.pedir_texto("\nIngrese DNI a buscar")
            
            resultado = self.controlador_pacientes.buscar_por_dni(dni_buscar)
            
            # Evaluar si se encontro al paciente
            if resultado["exito"]:
                paciente = resultado["datos"]
                
                # Mostrar en formato detalles
                Tablas.mostrar_detalle("DATOS DEL PACIENTE", {
                    "ID": paciente.id_paciente,
                    "DNI": paciente._dni,
                    "Nombre": paciente._nombre,
                    "Fecha nacimiento": paciente._fecha_nacimiento,
                    "Telefono": paciente._telefono,
                    "Tipo de seguro": paciente.tipo_seguro,
                    "Fecha de registro": paciente._fecha_registro,
                    "Porcentaje de descuento": f"{paciente._porcentaje_descuento}%",
                    "Historial de consultas": ", ".join(map(str, paciente.historial_consultas)) if paciente.historial_consultas else "Sin consultas"
                })
                
                Helpers.pausar()
                
            else:
                Mensajes.mostrar(resultado)
        except KeyboardInterrupt:
            print("\n\nBusqueda cancelada por el usuario.")
            Helpers.pausar()
        except Exception as e:
            Mensajes.mostrar({"exito": False, "mensaje": f"Error inesperado: {str(e)}"})
    
    def modificar_paciente(self):
        """Opcion 3: Modificar Paciente"""
        Helpers.limpiar_pantalla()
        print("=" * 50)
        print("     MODIFICAR PACIENTE")
        print("=" * 50)

        try:
            # Pedir ID
            id_paciente = Entradas.pedir_entero("\nIngrese ID del paciente", 1)
            
            # Buscar primero para confirmar identidad
            res = self.controlador_pacientes.buscar_por_id(id_paciente)
            
            if not res["exito"]:
                Mensajes.mostrar(res)
                return
            
            # Mostrar datos del paciente seleccionado
            paciente = res["datos"]
            print(f"Paciente seleccionado: {paciente._nombre} | DNI: {paciente._dni}")
            
            # Confirmar que no se equivoco de paciente
            if not Entradas.confirmar_accion("¿Desea continuar?"):
                print("Modificacion cancelada")
                Helpers.pausar()
                return
            
            # Mostrar campos a modificar
            print("\n¿Qué desea modificar?")
            print("1. Seguro")
            print("2. Nombre")
            print("3. Telefono")
            print("0. Cancelar")
            
            opcion = Entradas.pedir_entero("\nIngrese una opcion", 0, 3)
            
            if opcion == 0:
                print("Operacion cancelada")
                Helpers.pausar()
                return
            
            campo_modificar = {}
            
            # Opciones a modificar
            if opcion == 1:
                print("\nSeguros Permitidos:")
                for nombre, descuento in TIPOS_SEGURO.items():
                    print(f"     Seguro: {nombre} - Descuento: {descuento}%")
                nuevo_seguro = Entradas.pedir_opcion("Nuevo seguro", list(TIPOS_SEGURO.keys()))
                campo_modificar = {"seguro": nuevo_seguro}
            
            elif opcion == 2:
                nombre_nuevo = Entradas.pedir_texto("Nombre nuevo (minimo 3 caracteres)")
                campo_modificar = {"nombre": nombre_nuevo}
            
            elif opcion == 3:
                telefono_nuevo = Entradas.pedir_texto("Nuevo telefono (9 digitos empezando en 9)")
                campo_modificar = {"telefono": telefono_nuevo}
            
            # Confirmar
            if Entradas.confirmar_accion("¿Confirma la modificación?"):
                resultado = self.controlador_pacientes.modificar_paciente(id_paciente, campo_modificar)
                Mensajes.mostrar(resultado)
            else:
                print("\nModificacion cancelada")
                Helpers.pausar()
        except KeyboardInterrupt:
            print("\n\nAccion cancelada por el usuario.")
            Helpers.pausar()
        except Exception as e:
            Mensajes.mostrar({"exito": False, "mensaje": f"Error inesperado: {str(e)}"})
    
    def consultar_historial(self):
        """Opcion 4: Consultar historial clinico"""
        Helpers.limpiar_pantalla()
        print("=" * 50)
        print("     CONSULTAR HISTORIAL CLINICO")
        print("=" * 50)
        
        try:
            # Pedir ID
            id_paciente = Entradas.pedir_entero("\nIngrese ID del paciente", 1)
            
            # Buscar para confirmar identidad
            res = self.controlador_pacientes.buscar_por_id(id_paciente)
            
            if not res["exito"]:
                Mensajes.mostrar(res)
                return
            
            # Mostrar datos del paciente seleccionado
            paciente = res["datos"]
            print(f"Paciente seleccionado: {paciente._nombre} | DNI: {paciente._dni}")
            
            # Confirmar que no se equivoco de paciente
            if not Entradas.confirmar_accion("¿Desea continuar?"):
                print("Modificacion cancelada")
                Helpers.pausar()
                return
            
            # Buscar historial
            resultado_historial = self.controlador_pacientes.obtener_historial(id_paciente)
            
            if resultado_historial["exito"] and resultado_historial["datos"]:
                # Preparar datos para la tabla
                datos_tabla = []
                for consulta in resultado_historial["datos"]:
                # Procesamiento de Recetas (Lista a String)
                    texto_recetas = "Sin medicamentos"
                    if consulta.recetas and isinstance(consulta.recetas, list):
                        # Convertimos la lista de dicts en un string legible
                        items = [f"ID:{r['id_medicamento']}(x{r['cantidad']})" for r in consulta.recetas]
                        texto_recetas = ", ".join(items)
                    datos_tabla.append({
                        "id_consulta": consulta.id_consulta,
                        "id_cita": consulta.id_cita,
                        "id_paciente": consulta.id_paciente,
                        "id_doctor": consulta.id_doctor,
                        "fecha": consulta.fecha_hora,
                        "especialidad": consulta.especialidad,
                        "diagnostico": (consulta.diagnostico[:22] + "...") if len(consulta.diagnostico) > 25 else consulta.diagnostico,
                        "tratamiento": (consulta.tratamiento[:22] + "...") if consulta.tratamiento and len(consulta.tratamiento) > 25 else (consulta.tratamiento or "Sin tratamiento"),
                        "recetas": (texto_recetas[:22] + "...") if len(texto_recetas) > 25 else texto_recetas
                    })
                
                config = [
                    ("id_consulta", "ID Consulta"),
                    ("id_cita", "ID Cita"),
                    ("id_paciente", "ID Paciente"),
                    ("id_doctor", "ID Doctor"),
                    ("fecha", "Fecha"),
                    ("especialidad", "Especialidad"),
                    ("diagnostico", "Diagnostico"),
                    ("tratamiento", "Tratamiento"),
                    ("recetas", "Recetas")
                ]
                
                Tablas.mostrar(f"HISTORIAL DEL PACIENTE {paciente._nombre} - ID {paciente.id_paciente}", config, datos_tabla)
                Helpers.pausar()
            else:
                Mensajes.mostrar(resultado_historial)
            
        except KeyboardInterrupt:
            print("\n\nAccion cancelada por el usuario.")
            Helpers.pausar()
        except Exception as e:
            Mensajes.mostrar({"exito": False, "mensaje": f"Error inesperado: {str(e)}"})
    
    # ========== GESTION DE CITAS ==========
    def agendar_nueva_cita(self):
        """Opcion 5: Agendar nueva cita"""
        Helpers.limpiar_pantalla()
        print("=" * 50)
        print("     AGENDAR NUEVA CITA")
        print("=" * 50)
        
        try:
            # Solicitar DNI
            dni_paciente = Entradas.pedir_texto("\nIngrese DNI del paciente")
            
            # Buscar paciente
            resultado_paciente = self.controlador_pacientes.buscar_por_dni(dni_paciente)
        
            if not resultado_paciente["exito"]:
                Mensajes.mostrar(resultado_paciente)
                return 
            
            paciente = resultado_paciente["datos"]

            # Mostrar detalles de Paciente
            Tablas.mostrar_detalle("DATOS DEL PACIENTE", {
                "ID": paciente.id_paciente,
                "DNI": paciente._dni,
                "Nombre": paciente._nombre,
                "Fecha nacimiento": paciente._fecha_nacimiento,
                "Telefono": paciente._telefono,
                "Tipo de seguro": paciente.tipo_seguro,
                "Fecha de registro": paciente._fecha_registro,
                "Porcentaje de descuento": f"{paciente._porcentaje_descuento}%",
                "Historial de consultas": ", ".join(map(str, paciente.historial_consultas)) if paciente.historial_consultas else "Sin consultas"
                })
        
            # Confirmar que no se equivoco de paciente
            if not Entradas.confirmar_accion("\n¿Desea continuar?"):
                print("Agendar nueva cita cancelada")
                Helpers.pausar()
                return
            
            # Mostrar especialidades
            print("\nEspecialidades de Doctores:")
            for i, esp in enumerate(ESPECIALIDADES, 1):
                print(f"    {i}. {esp}") 
            especialidad = Entradas.pedir_opcion("Seleccione especialidad", list(ESPECIALIDADES))
            
            # Obtener doctores activos con esa especialidad
            doctores_encontrados = self.controlador_personal.obtener_doctores_por_especialidad(especialidad)
            
            if not doctores_encontrados["exito"]:
                Mensajes.mostrar(doctores_encontrados)
                Helpers.pausar()
                return
            
            doctores = doctores_encontrados["datos"]
            ids_permitidos = [doctor.id_personal for doctor in doctores] # Extraer IDs para validar existencia
            
            # Mostrar doctores
            print(f"\nDoctores disponibles Especialistas en {especialidad}:")
            for i, doctor in enumerate(doctores, 1):
                print(f"    {i}. Doctor: {doctor._nombre} | ID: {doctor.id_personal}")
            id_doctor = int(Entradas.pedir_opcion("Selecciona ID del Doctor", ids_permitidos))
            nombre_doctor = next((d._nombre for d in doctores if d.id_personal == id_doctor), "")
            
            # Pedir fecha y hora
            fecha = Entradas.pedir_fecha("Fecha de la cita")
            hora = Entradas.pedir_hora("Hora de la cita")
            
            # Motivo
            motivo = Entradas.pedir_texto("Motivo")
            
            # Mostrar resumen de la cita
            Tablas.mostrar_detalle("DATOS DE LA CITA", {
                "Paciente": paciente._nombre,
                "Doctor": nombre_doctor,
                "Especialidad": especialidad,
                "Fecha": fecha,
                "Hora": hora,
                "Motivo": motivo[:22] + "..." if len(motivo) > 25 else motivo
            })
            
            # Confirmacion
            if not Entradas.confirmar_accion("¿Confirma el registro de esta Cita?"):
                print("\nRegistro cancelado.")
                Helpers.pausar()
                return
            
            # Registrar
            resultado = self.controlador_citas.agendar_cita(
                id_paciente=paciente.id_paciente,
                id_doctor=id_doctor,
                fecha=fecha,
                hora=hora,
                motivo=motivo
            )
            
            # Mostrar resultado
            Mensajes.mostrar(resultado)
            
        except KeyboardInterrupt:
            print("\n\nAccion cancelada por el usuario.")
            Helpers.pausar()
        except Exception as e:
            Mensajes.mostrar({"exito": False, "mensaje": f"Error inesperado: {str(e)}"})
    
    def reprogramar_cita(self):
        """Opcion 6: Reprogramar cita"""
        Helpers.limpiar_pantalla()
        print("=" * 50)
        print("     REPROGRAMAR CITA")
        print("=" * 50)
        
        try:
            # Solicitar DNI del paciente
            dni_paciente = Entradas.pedir_texto("DNI del paciente")
            
            # Buscar paciente
            paciente_encontrado = self.controlador_pacientes.buscar_por_dni(dni_paciente)
            
            if not paciente_encontrado["exito"]:
                Mensajes.mostrar(paciente_encontrado)
                return
            
            paciente = paciente_encontrado["datos"]
            
            # Mostrar paciente
            print(f"Paciente: {paciente._nombre} | ID: {paciente.id_paciente}")
            
            # Confirmar que no se equivoco de paciente
            if not Entradas.confirmar_accion("\n¿Desea continuar?"):
                print("Reprogramacion de cita cancelada")
                Helpers.pausar()
                return
            
            # Buscar citas pendientes
            citas_encontradas = self.controlador_citas.listar_citas_pendientes_paciente(paciente.id_paciente)
            
            if not citas_encontradas["exito"]:
                Mensajes.mostrar(citas_encontradas)
                return
            
            citas = citas_encontradas["datos"]
        
            # Mostrar citas pendientes
            print(f"\nCitas pendientes del paciente {paciente._nombre}:")
            for i, cita in enumerate(citas, 1):
                print(f"    {i}. ID: {cita.id_cita} | Fecha: {cita.fecha} | Hora: {cita.hora} | Especialidad: {cita._especialidad}")
            ids_citas_str = [str(cita.id_cita) for cita in citas]
            id_cita_str = Entradas.pedir_opcion("Selecciona ID de la cita", ids_citas_str)
            id_cita = int(id_cita_str)
            obj_cita = next((c for c in citas if c.id_cita == id_cita))
            
            # Mostrar opciones a reprogramar
            print("\n¿Qué desea modificar?")
            print("1. Solo fecha")
            print("2. Solo hora")
            print("3. Fecha y hora")
            print("0. Cancelar")
        
            opcion = Entradas.pedir_entero("\nIngrese una opcion", 0, 3)
            
            if opcion == 0:
                print("Reprogramacion de cita cancelada")
                Helpers.pausar()
                return
            
            nueva_fecha = obj_cita.fecha
            nueva_hora = obj_cita.hora
            
            if opcion == 1 or opcion == 3:
                nueva_fecha = Entradas.pedir_fecha("Ingrese la Nueva Fecha")
            
            if opcion == 2 or opcion == 3:
                nueva_hora = Entradas.pedir_hora("Ingrese la Nueva Hora")
            
            # Pedir ID del recepcionista
            usuario = Entradas.pedir_entero("ID del recepcionista")
            
            # Mostrar datos anteriores y nuevos
            Tablas.mostrar_detalle("COMPARACIÓN DE CAMBIOS", {
                "Cita ID": obj_cita.id_cita,
                "Fecha Actual": obj_cita.fecha.strftime("%d/%m/%Y"),
                "Fecha Nueva": nueva_fecha.strftime("%d/%m/%Y"),
                "---": "---",
                "Hora Actual": obj_cita.hora.strftime("%H:%M"),
                "Hora Nueva": nueva_hora.strftime("%H:%M"),
                "Recepcionista": usuario
            })
            
            # Confirmacion
            if not Entradas.confirmar_accion("¿Confirma la reprogramacion de esta cita?"):
                print("\nRegistro cancelado.")
                Helpers.pausar()
                return
            
            # Reprogramar
            resultado = self.controlador_citas.reprogramar_cita(id_cita, usuario, nueva_fecha, nueva_hora)
            
            # Mostrar resultado
            Mensajes.mostrar(resultado)

        except KeyboardInterrupt:
            print("\n\nReprogramacion cancelada por el usuario.")
            Helpers.pausar()
        except Exception as e:
            Mensajes.mostrar({"exito": False, "mensaje": f"Error inesperado: {str(e)}"})
    
    def cancelar_cita(self):
        """Opcion 7: Cancelar Cita"""
        Helpers.limpiar_pantalla()
        print("=" * 50)
        print("     CANCELAR CITA")
        print("=" * 50)
        
        try:
            # Solicitar ID cita
            id_cita = Entradas.pedir_entero("\nIngresa ID de la cita", 1)
            
            # Buscar cita
            cita_encontrada = self.controlador_citas.buscar_por_id(id_cita)
            
            if not cita_encontrada["exito"]:
                Mensajes.mostrar(cita_encontrada)
                return
            
            cita = cita_encontrada["datos"]
            
            # Validar estado
            if cita.estado != "Agendada":
                print(f"\n[!] AVISO: Esta cita no se puede cancelar porque su estado es: {cita.estado}")
                Helpers.pausar()
                return
            
            # Mostrar detalles cita
            Tablas.mostrar_detalle("DETALLES DE LA CITA", {
                "ID": cita.id_cita,
                "ID Paciente": cita.id_paciente,
                "ID Doctor": cita.id_doctor,
                "Fecha": cita.fecha.strftime("%d/%m/%Y"),
                "Hora": cita.hora.strftime("%H:%M"),
                "Estado": cita.estado,
                "Motivo": cita.motivo[:22] + "..." if len(cita.motivo) > 25 else cita.motivo
            })
            
            # Confirmacion para continuar
            if not Entradas.confirmar_accion("\n¿Desea continuar?"):
                print("Cancelacion de cita anulada")
                Helpers.pausar()
                return
            
            # Cancelar cita
            resultado = self.controlador_citas.cancelar_cita(id_cita)
            
            # Mostrar resultado
            Mensajes.mostrar(resultado)
            
        except KeyboardInterrupt:
            print("\n\nAccion cancelada por el usuario.")
            Helpers.pausar()
        except Exception as e:
            Mensajes.mostrar({"exito": False, "mensaje": f"Error inesperado: {str(e)}"}) 
    
    def citas_del_dia(self):
        """Opcion 8: Consultar citas del dia"""
        Helpers.limpiar_pantalla()
        print("=" * 50)
        print("     CONSULTAR CITAS DEL DIA")
        print("=" * 50)
        
        try:
            # Mostrar Opciones
            print("\nSeleccione Fecha")
            print("1. Hoy")
            print("2. Otro dia")
            print("0. Cancelar")
            
            opcion = Entradas.pedir_entero("\nIngrese una opcion", 0, 2)
            
            if opcion == 0:
                print("Proceso cancelado")
                Helpers.pausar()
                return
            
            # Seleccionar fecha
            fecha_buscar = date.today()

            if opcion == 2:
                fecha_buscar = Entradas.pedir_fecha("Fecha a buscar")
            
            # Buscar citas
            citas_encontradas = self.controlador_citas.listar_citas_dia(fecha_buscar)
            
            if not citas_encontradas["exito"]:
                Mensajes.mostrar(citas_encontradas)
                return
            
            citas = citas_encontradas["datos"]
            
            # Preparar datos para tabla
            datos_tabla = []
            for cita in citas:
                datos_tabla.append({
                    "id_cita": cita.id_cita,
                    "id_paciente": cita.id_paciente,
                    "id_doctor": cita.id_doctor,
                    "fecha": cita.fecha,
                    "hora": cita.hora,
                    "especialidad": cita._especialidad,
                    "estado": cita.estado,
                    "motivo": cita.motivo[:22] + "..." if len(cita.motivo) > 25 else cita.motivo
                })
            
            config = [
                ("id_cita", "ID Cita"),
                ("id_paciente", "ID Paciente"),
                ("id_doctor", "ID Doctor"),
                ("fecha", "Fecha"),
                ("hora", "Hora"),
                ("especialidad", "Especialidad"),
                ("estado", "Estado"),
                ("motivo", "Motivo"),
            ]
            
            # Mostrar tabla
            Tablas.mostrar(f"CITAS DEL DIA {fecha_buscar}", config, datos_tabla)
            
        except KeyboardInterrupt:
            print("\n\nAccion cancelada por el usuario.")
            Helpers.pausar()
        except Exception as e:
            Mensajes.mostrar({"exito": False, "mensaje": f"Error inesperado: {str(e)}"})
    
    # ========== GESTION DE FACTURACION ==========
    def registrar_pago_factura(self):
        """Opción 9: Registrar pago de factura"""
        Helpers.limpiar_pantalla()
        print("═" * 50)
        print("    REGISTRAR PAGO DE FACTURA")
        print("═" * 50)
        print("\n⚠ Funcionalidad en desarrollo...")
        print("(Requiere implementar métodos en FacturacionController)")
        Helpers.pausar()
    
    def consultar_facturas(self):
        """Opción 10: Consultar facturas pendientes"""
        Helpers.limpiar_pantalla()
        print("═" * 50)
        print("    CONSULTAR FACTURAS PENDIENTES")
        print("═" * 50)
        print("\n⚠ Funcionalidad en desarrollo...")
        print("(Requiere implementar métodos en FacturacionController)")
        Helpers.pausar()
    
    # ========== VER INVENTARIO ==========
    def inventario_medicamentos(self):
        """Opción 11: Ver inventario de medicamentos"""
        Helpers.limpiar_pantalla()
        print("═" * 50)
        print("    VER INVENTARIO DE MEDICAMENTOS")
        print("═" * 50)
        print("\n⚠ Funcionalidad en desarrollo...")
        print("(Requiere implementar métodos en InventarioController)")
        Helpers.pausar()