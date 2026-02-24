"""
Menu del Administrador de Recursos Humanos
Gestiona personal, contratos y genera reportes

"""

from src.utils.helpers import Helpers
from src.controllers.personal_controller import PersonalController
from src.views.componentes.inputs import Entradas
from src.views.componentes.mensajes import Mensajes
from src.views.componentes.tablas import Tablas
from src.config.constantes import ROLES_PERSONAL, ESPECIALIDADES, DEPARTAMENTOS, JORNADAS, TURNOS, SALARIOS_BASE, TIPOS_CONTRATOS, MOTIVOS_BAJA

class MenuRRHH:
    """Menu principal del Administrador de Recursos Humanos"""
    
    def __init__(self) -> None:
        """Inicializa el menu con el controlador de Personal"""
        self.controlador = PersonalController()
        
    def mostrar(self):
        """Muestra el menu principal de RRHH y maneja las opciones"""
        while True:
            Helpers.limpiar_pantalla()
            print("═" * 50)
            print("    MENÚ ADMINISTRADOR DE RR.HH")
            print("═" * 50)
            print("\nGESTIÓN DE PERSONAL:")
            print("1. Registrar nuevo personal")
            print("2. Buscar personal")
            print("3. Modificar datos de personal")
            print("4. Dar de baja personal (inactivar)")
            print("5. Consultar personal por departamento")
            print("\nGESTIÓN DE CONTRATOS:")
            print("6. Ver contratos próximos a vencer")
            print("\nREPORTES:")
            print("7. Personal activo vs inactivo")
            print("8. Personal por departamento")
            print("9. Turnos asignados")
            print("\n0. Cerrar sesión")
            print("═" * 50)
            
            # Se ingresa una opcion y se valida (int)
            opcion = Entradas.pedir_entero("\nSeleccione una opcion", 0, 9)
            
            # Opciones
            if opcion == 1:
                self.registrar_personal()
            elif opcion == 2:
                self.buscar_personal()
            elif opcion == 3:
                self.modificar_personal()
            elif opcion == 4:
                self.inactivar_personal()
            elif opcion == 5:
                self.listar_por_departamento()
            elif opcion == 6:
                self.contratos_por_vencer()
            elif opcion == 7:
                self.reporte_activos_vs_inactivos()
            elif opcion == 8:
                self.reporte_por_departamento()
            elif opcion == 9:
                self.reporte_turnos()
            elif opcion == 0:
                print("\nCerrando sesión de RRHH...")
                Helpers.pausar()
                break
    
    # ========== GESTION DEL PERSONAL ==========
    
    def registrar_personal(self):
        """Opcion 1: Registrar nuevo personal"""
        Helpers.limpiar_pantalla()
        print("=" * 50)
        print("     REGISTRAR NUEVO PERSONAL")
        print("=" * 50)
        
        try:
            # Datos personales
            print("\n--- DATOS PERSONALES ---")
            dni = Entradas.pedir_texto("DNI (8 digitos)")
            nombre = Entradas.pedir_texto("Nombre completo")
            fecha_nac = Entradas.pedir_fecha("Fecha de nacimiento")
            telefono = Entradas.pedir_texto("Telefono (9 digitos)")
            
            # Datos laborales
            print("\n--- DATOS LABORALES ---")
            print("\nRoles disponibles:")
            for i, rol in enumerate(ROLES_PERSONAL, 1):
                print(f"     {i}. {rol}")
            rol = Entradas.pedir_opcion("seleccione rol", list(ROLES_PERSONAL))
            
            # Especialidad (solo si rol es Doctor)
            especialidad = None
            if rol == "Doctor":
                print("\nEspecialidades disponibles:")
                for i, espec in enumerate(ESPECIALIDADES, 1):
                    print(f"    {i}. {espec}")
                especialidad = Entradas.pedir_opcion("Seleccione especialidad", list(ESPECIALIDADES))
            
            # Departamentos
            print("\n--- ASIGNACION DE DEPARTAMENTOS ---")
            print("\nDepartamentos disponibles:")
            for id, valor in DEPARTAMENTOS.items():
                print(f"    {id}. {valor['nombre']}")
            departamentos = []
            while True:
                id_dep = Entradas.pedir_entero("ID del departamento a asignar", 1, 10)
                if id_dep in departamentos:
                    Mensajes.mostrar_advertencia("Este ID ya se encuentra seleccionado para este personal")
                else:
                    departamentos.append(id_dep)
                
                agregar_mas = Entradas.confirmar_accion("¿Desea asignar otro departamento?")
                if not agregar_mas:
                    break
            
            # Jornada
            print("\nJornadas disponibles:")
            for i, jornada in enumerate(JORNADAS, 1):
                print(f"    {i}. {jornada}")
            jornada = Entradas.pedir_opcion("Seleccione Jornada", list(JORNADAS))
            
            # Turno (Si jornada es Por turnos)
            turno = None
            if jornada == "Por turnos":
                print("\nTurnos disponibles:")
                for i, tur in enumerate(TURNOS, 1):
                    print(f"    {i}. {tur}")
                turno = Entradas.pedir_opcion("Seleccione turno", list(TURNOS))
            
            # Salario base (Seleccionado automaticamente)
            salario_base = SALARIOS_BASE[rol]
            
            # Fecha de contratacion 
            fecha_contratacion = Entradas.pedir_fecha("Fecha de contratacion")
            
            # Tipo de contrato
            print("\n--- DATOS DEL CONTRATO ---")
            print("\nTipos de contrato:")
            for i, tip in enumerate(TIPOS_CONTRATOS, 1):
                print(f"    {i}. {tip}")
            tipo_contrato = Entradas.pedir_opcion("Seleccione tipo de contrato", list(TIPOS_CONTRATOS))
            
            # Fecha fin (solo si tipo es Temporal)
            fecha_fin = None
            if tipo_contrato == "Temporal":
                fecha_fin = Entradas.pedir_fecha("Fecha fin del contrato")
            
            # Confirmar
            print("\n" + "-" * 50)
            if not Entradas.confirmar_accion("¿Confirma el registro de este personal?"):
                print("\nRegistro cancelado.")
                Helpers.pausar()
                return
            
            # Registrar
            resultado = self.controlador.registrar_personal(
                dni=dni,
                nombre=nombre,
                fecha_nacimiento=fecha_nac,
                telefono=telefono,
                rol=rol,
                especialidad=especialidad,
                departamentos=departamentos,
                jornada=jornada,
                turno=turno,
                salario_base=salario_base,
                fecha_contratacion=fecha_contratacion,
                tipo=tipo_contrato,
                fecha_fin=fecha_fin
            )
            
            #Mostrar resultado
            Mensajes.mostrar(resultado)
            
        except KeyboardInterrupt:
            print("\n\nRegistro cancelado por el usuario.")
            Helpers.pausar()
        except Exception as e:
            Mensajes.mostrar({"exito": False, "mensaje": f"Error inesperado: {str(e)}"})

    def buscar_personal(self):
        """Opción 2: Buscar personal por DNI"""
        Helpers.limpiar_pantalla()
        print("═" * 50)
        print("    BUSCAR PERSONAL")
        print("═" * 50)
        
        dni = Entradas.pedir_texto("\nIngrese DNI a buscar")
        
        resultado = self.controlador.buscar_por_dni(dni)
        
        if resultado["exito"]:
            personal = resultado["datos"]
            
            # Mostrar en formato detalle
            Tablas.mostrar_detalle("DATOS DEL PERSONAL", {
                "ID": personal.id_personal,
                "DNI": personal._dni,
                "Nombre": personal._nombre,
                "Fecha Nacimiento": personal._fecha_nacimiento,
                "Teléfono": personal._telefono,
                "Rol": personal.rol,
                "Especialidad": personal.especialidad or "N/A",
                "Departamentos": ", ".join(map(str, personal.departamentos)),
                "Jornada": personal._jornada,
                "Turno": personal._turno or "N/A",
                "Salario Base": f"S/ {personal._salario_base:.2f}",
                "Estado": personal.estado,
                "Fecha Contratación": personal._fecha_contratacion,
                "Fecha Baja": personal._fecha_baja or "N/A",
                "Motivo Baja": personal._motivo_baja or "N/A"
            })
        
            Helpers.pausar()
        else:
            Mensajes.mostrar(resultado)

    def modificar_personal(self):
        """Opcion 3: Modificar datos del personal"""
        Helpers.limpiar_pantalla()
        print("═" * 50)
        print("    MODIFICAR PERSONAL")
        print("═" * 50)
        
        id_personal = Entradas.pedir_entero("\nIngrese ID del personal", 1)
        
        print("\n¿Qué desea modificar?")
        print("1. Agregar departamento")
        print("2. Eliminar departamento")
        print("3. Cambiar especialidad")
        print("4. Cambiar turno")
        print("5. Cambiar jornada")
        print("6. Modificar salario base")
        print("0. Cancelar")
        
        opcion = Entradas.pedir_entero("\nSeleccione una opcion", 0, 6)
        
        if opcion == 0:
            print("Operacion cancelada")
            Helpers.pausar()
            return
        
        campo_modificar = {}

        # Opciones
        if opcion == 1:
            id_departamento = Entradas.pedir_entero("ID del departamento a agregar", 1, 10)
            campo_modificar = {"Agregar departamento": id_departamento}
        
        elif opcion == 2:
            id_departamento = Entradas.pedir_entero("ID del departamento a eliminar", 1, 10)
            campo_modificar = {"Eliminar departamento": id_departamento}
        
        elif opcion == 3:
            print("\nEspecialidades disponibles:")
            for i, espec in enumerate(ESPECIALIDADES, 1):
                print(f"    {i}. {espec}")
            nueva_especialidad = Entradas.pedir_opcion("Nueva especialidad", list(ESPECIALIDADES))
            campo_modificar = {"Especialidad": nueva_especialidad}
        
        elif opcion == 4:
            print("\nTurnos disponibles:")
            for i, tur in enumerate(TURNOS, 1):
                print(f"    {i}. {tur}")
            turno_nuevo = Entradas.pedir_opcion("Nuevo Turno", list(TURNOS))
            campo_modificar = {"Turno": turno_nuevo}
        
        elif opcion == 5:
            print("\nJornadas disponibles:")
            for i, jornada in enumerate(JORNADAS, 1):
                print(f"    {i}. {jornada}")
            nueva_jornada = Entradas.pedir_opcion("Nueva jornada", list(JORNADAS))
            
            if nueva_jornada == "Por turnos":
                print("\nTurnos disponibles:")
                for i, tur in enumerate(TURNOS, 1):
                    print(f"    {i}. {tur}")
                nuevo_turno = Entradas.pedir_opcion("Seleccione turno", list(TURNOS))
                campo_modificar = {"Jornada": nueva_jornada, "Turno": nuevo_turno}
            else:
                campo_modificar = {"Jornada": nueva_jornada}
        
        elif opcion == 6:
            sueldo_nuevo = Entradas.pedir_flotante("Nuevo salario", 1800.00, 20000.00)
            campo_modificar = {"Salario base": sueldo_nuevo}
        
        # Confirmar
        if Entradas.confirmar_accion("¿Confirma la modificación?"):
            resultado = self.controlador.modificar_personal(id_personal, campo_modificar)
            Mensajes.mostrar(resultado)
        else:
            print("\nModificacion cancelada")
            Helpers.pausar()

    def inactivar_personal(self):
        """Opcion 4: Dar de baja a un personal"""
        Helpers.limpiar_pantalla()
        print("═" * 50)
        print("    DAR DE BAJA PERSONAL")
        print("═" * 50)
        
        id_personal = Entradas.pedir_entero("\nIngrese ID del personal", 1)
        fecha_baja = Entradas.pedir_fecha("Fecha de baja")
        
        print("\nMotivos de baja:")
        for i, baja in enumerate(MOTIVOS_BAJA, 1):
            print(f"    {i}. {baja}")
        motivo_baja = Entradas.pedir_opcion("Seleccione motivo", list(MOTIVOS_BAJA))
        
        if Entradas.confirmar_accion(f"¿Confirma dar de baja al personal ID {id_personal}?"):
            resultado = self.controlador.inactivar_personal(id_personal, fecha_baja, motivo_baja)
            Mensajes.mostrar(resultado)
        else:
            print("\nOperación cancelada.")
            Helpers.pausar()

    def listar_por_departamento(self):
        """Opción 5: Consultar personal por departamento"""
        Helpers.limpiar_pantalla()
        print("═" * 50)
        print("    PERSONAL POR DEPARTAMENTO")
        print("═" * 50)
        
        id_depto = Entradas.pedir_entero("\nIngrese ID del departamento", 1, 10)
        
        resultado = self.controlador.listar_por_departamento(id_depto)
        
        if resultado["exito"] and resultado["datos"]:
            # Preparar datos para tabla
            datos_tabla = []
            for personal in resultado["datos"]:
                datos_tabla.append({
                    "id": personal.id_personal,
                    "nombre": personal._nombre,
                    "rol": personal.rol,
                    "jornada": personal._jornada,
                    "estado": personal.estado
                })
            
            config = [
                ("id", "ID"),
                ("nombre", "Nombre"),
                ("rol", "Rol"),
                ("jornada", "Jornada"),
                ("estado", "Estado")
            ]
            
            nombre_departamento = DEPARTAMENTOS[id_depto]["nombre"]
            Tablas.mostrar(f"PERSONAL DEL DEPARTAMENTO {nombre_departamento}", config, datos_tabla)
            Helpers.pausar()
        else:
            Mensajes.mostrar(resultado)

    # ========== GESTIÓN DE CONTRATOS ==========

    def contratos_por_vencer(self):
        """Opción 6: Ver contratos próximos a vencer"""
        Helpers.limpiar_pantalla()
        print("═" * 50)
        print("    CONTRATOS PRÓXIMOS A VENCER")
        print("═" * 50)
        print("\n⚠ Funcionalidad en desarrollo...")
        print("(Requiere implementar métodos en ReporteController)")
        Helpers.pausar()

    # ========== REPORTES ==========

    def reporte_activos_vs_inactivos(self):
        """Opción 7: Reporte de personal activo vs inactivo"""
        Helpers.limpiar_pantalla()
        print("═" * 50)
        print("    REPORTE: PERSONAL ACTIVO VS INACTIVO")
        print("═" * 50)
        print("\n⚠ Funcionalidad en desarrollo...")
        print("(Requiere implementar métodos en ReporteController)")
        Helpers.pausar()

    def reporte_por_departamento(self):
        """Opción 8: Personal por departamento"""
        Helpers.limpiar_pantalla()
        print("═" * 50)
        print("    REPORTE: PERSONAL POR DEPARTAMENTO")
        print("═" * 50)
        print("\n⚠ Funcionalidad en desarrollo...")
        print("(Requiere implementar métodos en ReporteController)")
        Helpers.pausar()

    def reporte_turnos(self):
        """Opción 9: Turnos asignados"""
        Helpers.limpiar_pantalla()
        print("═" * 50)
        print("    REPORTE: TURNOS ASIGNADOS")
        print("═" * 50)
        print("\n⚠ Funcionalidad en desarrollo...")
        print("(Requiere implementar métodos en ReporteController)")
        Helpers.pausar()