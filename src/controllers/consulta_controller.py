"""
Responsable de completar consultas medicas

"""
from src.utils.persistencia import Persistencia
from src.controllers.inventario_controller import InventarioController
from src.controllers.facturacion_controller import FacturacionController
from typing import List
from src.utils.validaciones import Validaciones
from src.models.consulta import Consulta
from src.models.paciente import Paciente
class ConsultaController:
    """
    Clase "controlador" encargada de completar una consulta
    
    Orqueta la logica y coordina las interacciones entra las capas:
    Vista, Modelo y Persistencia
    """
    
    # ========== INICIALIZA ==========
    def __init__(self) -> None:
        """
        Inicializa el controlador de Consulta configurando las rutas de los archivos
        de persistencia y controladores necesarios 
        
        Atributos:
            persistencia_consultas (Persistencia): Repositorio de datos para el registro de las Consultas
            persistencia_citas (Persistencia): Repositorio de datos de las citas que requieren una Consulta
            persistencia_pacientes (Persistencia): Repositorio de datos de los pacientes para su historial
            inventario_controller (InventarioController): Controlador del Inventario para los medicamentos a recetar
            facturacion_controller (FacturacionController): Controlador de las Facturas para el pago de la Consulta
        """
        
        self.persistencia_consultas = Persistencia("data/consultas.json")
        self.persistencia_citas = Persistencia("data/citas.json")
        self.persistencia_pacientes = Persistencia("data/pacientes.json")
        self.inventario_controller = InventarioController()
        self.facturacion_controller = FacturacionController()

    # ========== METODOS ==========
    def completar_consulta(self, 
        id_cita: int, 
        id_doctor: int, 
        diagnostico: str, 
        tratamiento: str | None = None, 
        recetas: List[dict] | None = None
    ) -> dict:
        
        """
        Completa una consulta medica
        
        Args:
            Datos necesarios para crear la instancia
        
        Returns:
            dict: {"exito": bool, "mensaje": str, "datos": dict | None}
        """
        # Validar IDs
        if not isinstance(id_cita, int) or id_cita <= 0:
            return {"exito": False, "mensaje": "Formato de ID de Cita invalido. Debe ser un numero entero positivo", "datos": None}
        
        if not isinstance(id_doctor, int) or id_doctor <= 0:
            return {"exito": False, "mensaje": "Formato de ID de Doctor invalido. Debe ser un numero entero positivo", "datos": None}
        
        # Validar diagnostico
        if not Validaciones.validar_longitud_minima(diagnostico, 20):
            return {"exito": False, "mensaje": "Diagnostico invalido. Debe ser texto con 20 caracteres minimo", "datos": None}
        
        # Validar tratamiento si aplica
        if tratamiento:
            if not Validaciones.validar_longitud_minima(tratamiento, 10):
                return {"exito": False, "mensaje": "Tratamiento invalido. Debe ser texto con 10 caracteres minimo", "datos": None}
        
        # Validar recetas si aplica
        if recetas:
            if not isinstance(recetas, list):
                return {"exito": False, "mensaje": "Recetas debe ser una lista", "datos": None}
            
            for i, receta in enumerate(recetas):
                if not isinstance(receta, dict):
                    return {"exito": False, "mensaje": f"Receta {i} debe ser un diccionario", "datos": None}
                
                if "id_medicamento" not in receta or "cantidad" not in receta:
                    return {"exito": False, "mensaje": f"Receta {i} debe tener 'id_medicamento' y 'cantidad'", "datos": None}
            
            receta_resultado = self.inventario_controller.procesar_recetas(recetas)
            if not receta_resultado["exito"]:
                return {"exito": False, "mensaje": f"{receta_resultado['mensaje']}", "datos": None}
        
        # Crear Consulta
        try:
            # Obtener cita
            cita = self.persistencia_citas.buscar_por_id(id_cita)
            if not cita:
                return {"exito": False, "mensaje": f"No se encontro una cita con el ID ({id_cita})", "datos": None}
            
            # Validar estado
            if cita["estado"] != "Agendada":
                return {"exito": False, "mensaje": f"Solo se pueden completar cita Agendadas. Estado de la cita: {cita['estado']}", "datos": None}

            # Validar doctor
            if cita["id_doctor"] != id_doctor:
                return {"exito": False, "mensaje": "Esta cita esta asignada a otro doctor", "datos": None}
            
            # Obtener paciente para historial
            id_paciente = cita["id_paciente"]
            paciente = self.persistencia_pacientes.buscar_por_id(id_paciente)
            
            if not paciente:
                return {"exito": False, "mensaje": "No se pudo acceder al registro del paciente", "datos": None}
            obj_paciente = Paciente.from_dict(paciente)
            
            # Crear instancia
            id_consulta = self._generar_id()
            consulta = Consulta(
                id_consulta=id_consulta,
                id_cita=id_cita,
                id_paciente=cita["id_paciente"],
                id_doctor=id_doctor,
                especialidad=cita["especialidad"],
                diagnostico=diagnostico,
                tratamiento=tratamiento
            )
            
            # Agregar recetas a la consulta si aplica
            if recetas:
                for receta in recetas:
                    consulta.agregar_receta(
                        receta["id_medicamento"],
                        receta["cantidad"]
                    )
            
            # Guardar consulta
            self.persistencia_consultas.agregar(consulta.to_dict())
            
            # Actualizar estado de la cita
            self.persistencia_citas.actualizar(id_cita, {"estado": "Completada"})
            
            # Agregar consulta al historial del paciente
            obj_paciente.agregar_consulta_historial(id_consulta)
            
            # Guardar cambios del paciente
            datos_actualizados = obj_paciente.to_dict()
            self.persistencia_pacientes.actualizar(
                obj_paciente.id_paciente,
                datos_actualizados
            )
            
            # Generar factura automaticamente
            resultado_factura = self.facturacion_controller.generar_factura_automatica(
                id_consulta=id_consulta,
                id_paciente=cita["id_paciente"],
                especialidad=cita["especialidad"],
                recetas=recetas
            )
            
            # Revertir todo si falla la factura
            if not resultado_factura["exito"]:
                self._revertir_consulta(id_consulta, id_cita, obj_paciente.id_paciente, recetas)
                return {"exito": False, "mensaje": "Error al generar factura", "datos": None}
            
            # Exito
            datos = {"id_consulta": id_consulta, "id_factura": resultado_factura["id_factura"]}
            return {
                "exito": True,
                "mensaje": "Consulta completada exitosamente",
                "datos": datos
            }
            
        except Exception as e:
            return {"exito": False, "mensaje": f"Error crítico: {str(e)}", "datos": None}

    def buscar_consulta(self, id_consulta: int) -> dict:
        """
        Busca una consulta por su ID.
        
        Args:
            id_consulta (int): ID de la consulta
        
        Returns:
            dict: {"exito": bool, "mensaje": str, "datos": Consulta | None}
        """
        if not isinstance(id_consulta, int) or id_consulta <= 0:
            return {
                "exito": False,
                "mensaje": "ID de consulta inválido",
                "datos": None
            }
        
        try:
            consulta_data = self.persistencia_consultas.buscar_por_id(id_consulta)
            
            if not consulta_data:
                return {
                    "exito": False,
                    "mensaje": f"No se encontró consulta con ID {id_consulta}",
                    "datos": None
                }
            
            consulta = Consulta.from_dict(consulta_data)
            
            return {
                "exito": True,
                "mensaje": "Consulta encontrada",
                "datos": consulta
            }
        
        except Exception as e:
            return {
                "exito": False,
                "mensaje": f"Error: {str(e)}",
                "datos": None
            }

    # ========== METODOS PRIVADOS ==========
    def _revertir_consulta(self, id_consulta: int, id_cita: int, id_paciente: int, recetas: List[dict] | None = None) -> None:
        """
        Revierte cambios si falla la generacion de la factura
        
        Args:
            id_consulta (int): ID de la consulta a cancelar
            id_cita (int): ID de la cita 
            id_paciente (int): ID del paciente
            recetas (List[dict] | None = None): Receta con medicamentos a revertir (si aplica)
        """
        try:
            # Eliminar consulta
            self.persistencia_consultas.eliminar(id_consulta)
            
            # Restablecer estado de cita
            self.persistencia_citas.actualizar(id_cita, {"estado": "Agendada"})
            
            # Borrar consulta del historial del paciente
            paciente_data = self.persistencia_pacientes.buscar_por_id(id_paciente)
            if paciente_data:
                historial_actual = paciente_data.get("historial_consultas", [])
                if id_consulta in historial_actual:
                    historial_actual.remove(id_consulta)
                
                self.persistencia_pacientes.actualizar(
                    id_paciente,
                    {"historial_consultas": historial_actual}
                )
            
            # Restaurar stock
            if recetas:
                self.inventario_controller.restaurar_stock(recetas)
        except Exception as e:
            print(f"ERROR CRITICO al revertir consulta {id_consulta}: {str(e)} ")

    def _generar_id(self) -> int:
        """
        Genera un ID de Consulta unico auto-incremental
        """
        return self.persistencia_consultas.generar_id_autoincremental()