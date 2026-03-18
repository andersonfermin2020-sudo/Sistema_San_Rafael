"""
Menu principal de un Doctor
Gestiona Citas, Consultas y Pacientes
"""
from src.controllers.consulta_controller import ConsultaController
from src.controllers.cita_controller import CitaController
from src.controllers.paciente_controller import PacienteController
from src.controllers.personal_controller import PersonalController
from src.controllers.inventario_controller import InventarioController
from src.utils.helpers import Helpers
from src.views.componentes.inputs import Entradas
from src.views.componentes.mensajes import Mensajes
from src.views.componentes.tablas import Tablas
from src.config.constantes import ESTADOS_CITA
class MenuDoctor:
    """Menu de Doctor"""
    
    # ========== INICIALIZA ==========
    def __init__(self) -> None:
        """Inicializa el Menu con los controladores de Consulta, Cita, Paciente, Personal e Inventario"""
        self.controlador_consultas = ConsultaController()
        self.controlador_citas = CitaController()
        self.controlador_pacientes = PacienteController()
        self.controlador_personal = PersonalController()
        self.controlador_inventario = InventarioController()
    
    # ========== MENU PRINCIPAL ==========
    def mostrar(self):
        """Muestra el Menu principal y maneja las opciones"""
        while True:
            Helpers.limpiar_pantalla()
            print("═" * 50)
            print("    MENÚ DOCTOR")
            print("═" * 50)
            print("\nCONSULTAS:")
            print("1. Ver mis citas del día")
            print("2. Ver mis citas futuras")
            print("3. Completar consulta")
            print("\nPACIENTES:")
            print("4. Buscar paciente")
            print("5. Ver historial clínico de paciente")
            print("\nINVENTARIO:")
            print("6. Consultar medicamentos disponibles")
            print("\n0. Cerrar sesión")
            print("═" * 50)
            
            # Ingresar opcion
            opcion = Entradas.pedir_entero("\nSeleccione una opcion", 0, 6)
            
            # Opciones
            if opcion == 0:
                print("\nCerrando sesion de Doctor...")
                Helpers.pausar()
                break
            
            if opcion == 1:
                self.ver_citas()
            elif opcion == 2:
                self.ver_citas_futuras()
            elif opcion == 3:
                self.completar_consulta()
            elif opcion == 4:
                self.buscar_paciente()
            elif opcion == 5:
                self.ver_historial_clinico()
            elif opcion == 6:
                self.medicamentos_disponibles()

    # ========== GESTION DE CONSULTAS ==========
    def ver_citas(self):
        """Opcion 1: Ver citas del dia"""
        Helpers.limpiar_pantalla()
        print("=" * 50)
        print("     VER CITAS DEL DIA")
        print("=" * 50)
        
        try:
            # Pedir ID
            id_doctor = Entradas.pedir_entero("\nIngrese su ID", 1)
            
            # Buscar doctor
            doctor_encontrado = self.controlador_personal.obtener_doctor_activo_por_id(id_doctor)
            
            # Verificar existencia
            if not doctor_encontrado["exito"]:
                Mensajes.mostrar(doctor_encontrado)
                return
            
            # Mostrar datos
            doctor = doctor_encontrado["datos"]
            print(f"Doctor {doctor._nombre} | Especialidad: {doctor.especialidad}")
            
            # Confirmar para continuar
            if not Entradas.confirmar_accion("\n¿Desea continuar?"):
                print("Busqueda cancelada")
                Helpers.pausar()
                return
            
            # Pedir estado de Citas
            print("\nSeleccione Estado:")
            print("1. Ver Citas Agendadas")
            print("2. Ver Citas Completadas")
            print("3. Ver Citas Canceladas")
            
            estado = Entradas.pedir_opcion("Ingrese el Estado", ESTADOS_CITA)
            
            # Buscar citas del dia
            citas_encontradas = self.controlador_citas.listar_agenda_actual_doctor(id_doctor, estado)
            
            # Verificar existencia
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
            Tablas.mostrar(f"CITAS {estado.upper()} DEL DIA", config, datos_tabla)

        except KeyboardInterrupt:
            print("\n\nAccion cancelada por el Doctor.")
            Helpers.pausar()
        except Exception as e:
            Mensajes.mostrar({"exito": False, "mensaje": f"Error inesperado: {str(e)}"})
    
    def ver_citas_futuras(self):
        """Opcion 2: Ver citas futuras"""
        Helpers.limpiar_pantalla()
        print("=" * 50)
        print("     VER CITAS FUTURAS")
        print("=" * 50)
        
        try:
            # Pedir ID
            id_doctor = Entradas.pedir_entero("\nIngrese su ID", 1)
            
            # Buscar doctor
            doctor_encontrado = self.controlador_personal.obtener_doctor_activo_por_id(id_doctor)
            
            # Verificar existencia
            if not doctor_encontrado["exito"]:
                Mensajes.mostrar(doctor_encontrado)
                return
            
            # Mostrar datos
            doctor = doctor_encontrado["datos"]
            print(f"Doctor {doctor._nombre} | Especialidad: {doctor.especialidad}")
            
            # Confirmar para continuar
            if not Entradas.confirmar_accion("\n¿Desea continuar?"):
                print("Busqueda cancelada")
                Helpers.pausar()
                return
            
            # Pedir estado de Citas
            print("\nSeleccione Estado:")
            print("1. Ver Futuras Citas Agendadas")
            print("2. Ver Futuras Citas Canceladas")
            
            estado = Entradas.pedir_opcion("Ingrese el Estado", ["Agendada", "Cancelada"])
            
            # Buscar citas futuras
            citas_encontradas = self.controlador_citas.listar_proximas_citas_doctor(id_doctor, estado)
            
            # Verificar existencia
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
            Tablas.mostrar(f"CITAS {estado.upper()} FUTURAS", config, datos_tabla)

        except KeyboardInterrupt:
            print("\n\nAccion cancelada por el Doctor.")
            Helpers.pausar()
        except Exception as e:
            Mensajes.mostrar({"exito": False, "mensaje": f"Error inesperado: {str(e)}"})

    def completar_consulta(self):
        """Opcion 3: Completar consulta"""
        Helpers.limpiar_pantalla()
        print("=" * 50)
        print("     COMPLETAR CONSULTA")
        print("=" * 50)

        try:
            # Pedir ID
            id_doctor = Entradas.pedir_entero("\nIngrese su ID", 1)
            
            # Buscar doctor
            doctor_encontrado = self.controlador_personal.obtener_doctor_activo_por_id(id_doctor)
            
            # Verificar existencia
            if not doctor_encontrado["exito"]:
                Mensajes.mostrar(doctor_encontrado)
                return
            
            # Mostrar datos
            doctor = doctor_encontrado["datos"]
            print(f"Doctor {doctor._nombre} | Especialidad: {doctor.especialidad}")
            
            # Confirmar para continuar
            if not Entradas.confirmar_accion("\n¿Desea continuar?"):
                print("Consulta cancelada")
                Helpers.pausar()
                return
            
            # Buscar citas agendadas para hoy
            citas_encontradas = self.controlador_citas.listar_agenda_actual_doctor(id_doctor, "Agendada")
            
            if not citas_encontradas["exito"]:
                Mensajes.mostrar(citas_encontradas)
                return
            
            # Mostrar citas
            citas = citas_encontradas["datos"]
            ids_permitidos = [] # IDs de citas para validar
            
            datos_tabla = []
            for cita in citas:
                ids_permitidos.append(cita.id_cita)
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
            Tablas.mostrar("CITAS AGENDADAS DEL DIA", config, datos_tabla)
            
            # Solicitar ID Cita
            ids_permitidos_str = [str(cita.id_cita) for cita in citas]
            id_cita_str = Entradas.pedir_opcion("ID de Cita", ids_permitidos_str)
            id_cita = int(id_cita_str)
            obj_cita = next((cita_buscar for cita_buscar in citas if cita_buscar.id_cita == id_cita))
            
            # Buscar paciente para detalles
            paciente_encontrado = self.controlador_pacientes.buscar_por_id(obj_cita.id_paciente)
            
            if not paciente_encontrado["exito"]:
                Mensajes.mostrar(paciente_encontrado)
                return
            
            paciente = paciente_encontrado["datos"]
            
            # Mostrar paciente y motivo de consulta
            Tablas.mostrar_detalle("DATOS DEL PACIENTE", {
                "ID": paciente.id_paciente, 
                "DNI": paciente._dni,
                "Nombre": paciente._nombre,
                "Fecha nacimiento": paciente._fecha_nacimiento,
                "Telefono": paciente._telefono,
                "Tipo de seguro": paciente.tipo_seguro,
                "Fecha de registro": paciente._fecha_registro,
                "Porcentaje de descuento": f"{paciente._porcentaje_descuento}%",
                "Historial de consultas": ", ".join(map(str, paciente.historial_consultas)) if paciente.historial_consultas else "Sin consultas",
                "Motivo de la consulta": obj_cita.motivo[:22] + "..." if len(obj_cita.motivo) > 25 else obj_cita.motivo
            })
            
            # Confirmacion para continuar
            if not Entradas.confirmar_accion("\n¿Desea continuar?"):
                print("Consulta cancelada")
                Helpers.pausar()
                return
            
            # Solicitar diagnostico
            diagnostico = Entradas.pedir_texto("\nIngrese diagnostico (minimo 20 caracteres)")
            
            # Solicitar tratamiento (si aplica)
            tratamiento = None
            if Entradas.confirmar_accion("\n¿Desea agregar tratamiento?"):
                tratamiento = Entradas.pedir_texto("Ingrese tratamiento (minimo 10 caracteres)")
            
            # Solicitar medicamentos (si aplica)
            recetas = []
            if Entradas.confirmar_accion("\n¿Desea agregar medicamentos?"):
                
                # Buscar medicamentos disponibles 
                medicamentos_encontrados = self.controlador_inventario.listar_medicamentos_disponibles()
                
                if not medicamentos_encontrados["exito"]:
                    Mensajes.mostrar(medicamentos_encontrados)
                    return
                
                # Mostrar medicamentos
                medicamentos = medicamentos_encontrados["datos"]
                ids_permitidos = [] # IDs de Medicamentos para validar
                
                datos_tabla = []
                for medicamento in medicamentos:
                    ids_permitidos.append(medicamento.id_medicamento)
                    datos_tabla.append({
                        "id_medicamento": medicamento.id_medicamento,
                        "nombre": medicamento.nombre,
                        "categoria": medicamento._categoria,
                        "stock_actual": medicamento.stock_actual,
                        "precio_unitario": medicamento.precio_unitario,
                        "fecha_vencimiento": medicamento.fecha_vencimiento
                    })
                
                config = [
                    ("id_medicamento", "ID Medicamento"),
                    ("nombre", "Nombre"),
                    ("categoria", "Categoria"),
                    ("stock_actual", "Unidades disponibles"),
                    ("precio_unitario", "Precio"),
                    ("fecha_vencimiento", "Fecha de Vencimiento")
                ]

                Tablas.mostrar("MEDICAMENTOS DISPONIBLES", config, datos_tabla)
                
                # Pedir medicamentos
                while True:
                    ids_permitidos_str = [str(medicamento.id_medicamento) for medicamento in medicamentos]
                    id_medicamento_str = Entradas.pedir_opcion("\nIngrese ID del medicamento", ids_permitidos_str)
                    id_medicamento = int(id_medicamento_str)
                    cantidad = Entradas.pedir_entero("Ingrese cantidad", 1)
                    recetas.append({"id_medicamento": id_medicamento, "cantidad": cantidad})
                    
                    if not Entradas.confirmar_accion("¿Desea agregar otro medicamento?"):
                        break
            
            # Mostrar resumen de consulta
            recetas_mostrar = None
            if recetas:
                items = [f"ID:{r['id_medicamento']}(x{r['cantidad']})" for r in recetas]
                recetas_mostrar = ", ".join(items)  
                
            Tablas.mostrar_detalle("RESUMEN DE LA CONSULTA", {
                "Paciente": paciente._nombre,
                "Diagnóstico": diagnostico[:40] + "..." if len(diagnostico) > 40 else diagnostico,
                "Tratamiento": tratamiento[:40] + "..." if tratamiento and len(tratamiento) > 40 else (tratamiento or "Sin tratamiento"),
                "Medicamentos": recetas_mostrar[:22] + "..." if recetas_mostrar and len(recetas_mostrar) > 25 else (recetas_mostrar or "Sin medicamentos")
            })          

            # Confirmacion
            if not Entradas.confirmar_accion("\n¿Confirma el registro de esta Consulta?"):
                print("Consulta cancelada")
                Helpers.pausar()
                return
            
            resultado = self.controlador_consultas.completar_consulta(
                id_cita=id_cita,
                id_doctor=id_doctor,
                diagnostico=diagnostico,
                tratamiento=tratamiento,
                recetas=recetas if recetas else None
            )
            
            # Mostrar resultado
            Mensajes.mostrar(resultado)
            
        except KeyboardInterrupt:
            print("\n\nAccion cancelada por el Doctor.")
            Helpers.pausar()
        except Exception as e:
            Mensajes.mostrar({"exito": False, "mensaje": f"Error inesperado: {str(e)}"})

    # ========== GESTION DE PACIENTES ==========
    def buscar_paciente(self):
        """Opcion 4: Buscar paciente"""
        Helpers.limpiar_pantalla()
        print("=" * 50)
        print("     BUSCAR PACIENTE")
        print("=" * 50)
        
        try:
            # Solicitar DNI:
            dni_paciente = Entradas.pedir_texto("\nIngrese DNI del paciente")
            
            # Buscar paciente
            paciente_encontrado = self.controlador_pacientes.buscar_por_dni(dni_paciente)
            
            # Verificar existencia
            if not paciente_encontrado["exito"]:
                Mensajes.mostrar(paciente_encontrado)
                return
            
            # Mostrar en formato detalles
            paciente = paciente_encontrado["datos"]
            
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
            
        except KeyboardInterrupt:
            print("\n\nAccion cancelada por el Doctor.")
            Helpers.pausar()
        except Exception as e:
            Mensajes.mostrar({"exito": False, "mensaje": f"Error inesperado: {str(e)}"})
    
    def ver_historial_clinico(self):
        """Opcion 5: Ver historial clinico de paciente"""
        Helpers.limpiar_pantalla()
        print("=" * 50)
        print("     VER HISTORIAL CLINICO")
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
                print("Busqueda cancelada")
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
    
    # ========== VER INVENTARIO ==========
    def medicamentos_disponibles(self):
        """Opción 6: Ver inventario de medicamentos"""
        Helpers.limpiar_pantalla()
        print("═" * 50)
        print("    CONSULTAR MEDICAMENTOS DISPONIBLES")
        print("═" * 50)
        print("\n⚠ Funcionalidad en desarrollo...")
        print("(Requiere implementar métodos en InventarioController)")
        Helpers.pausar()
