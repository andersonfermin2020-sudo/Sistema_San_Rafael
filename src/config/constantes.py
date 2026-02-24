"""
Constantes del sistema 

"""

# Roles de Personal
ROLES_PERSONAL = ["Doctor", "Enfermera", "Administrativo"]

# Especialidades Medicas
ESPECIALIDADES = ["Medicina General", "Pediatria", "Cardiologia"]

# Departamentos
DEPARTAMENTOS = {
    1: {"nombre": "Emergencia", "descripcion": "Atención de urgencias y emergencias médicas"},
    2: {"nombre": "Pediatría", "descripcion": "Atención médica para niños y adolescentes"},
    3: {"nombre": "Cardiología", "descripcion": "Diagnóstico y tratamiento de enfermedades del corazón"},
    4: {"nombre": "Traumatología", "descripcion": "Tratamiento de lesiones del sistema musculoesquelético"},
    5: {"nombre": "Ginecología", "descripcion": "Atención de la salud femenina y reproductiva"},
    6: {"nombre": "Medicina General", "descripcion": "Consultas médicas generales"},
    7: {"nombre": "Farmacia", "descripcion": "Dispensación y control de medicamentos"},
    8: {"nombre": "Laboratorio", "descripcion": "Análisis clínicos y diagnósticos"},
    9: {"nombre": "Radiología", "descripcion": "Estudios de imagen y diagnóstico por imagen"},
    10: {"nombre": "Administración", "descripcion": "Gestión administrativa del hospital"}
}

# Tipos de Contrato
TIPOS_CONTRATOS = ["Temporal", "Indefinido", "Por honorarios"]

# Estados de Contrato
ESTADOS_CONTRATO = ["Activo", "Vencido", "Finalizado"]

# Jornadas Laborales
JORNADAS = ["Medio tiempo", "Tiempo completo", "Por turnos"]

# Turnos
TURNOS = ["Manana", "Tarde", "Noche"]

# Estados de Personal
ESTADOS_PERSONAL = ["Activo", "Inactivo"]

# Motivos de Baja
MOTIVOS_BAJA = ["Renuncia", "Despido", "Fin de contrato"]

# Tipos de Seguro 
TIPOS_SEGURO = {
    "Ninguno": 0,
    "Publico": 20,
    "Privado": 50
}

# Estado de Cita
ESTADOS_CITA = ["Agendada", "Completada", "Cancelada"]

# Categorias de Medicamentos 
CATEGORIAS_MEDICAMENTO = [
    "Analgesico",
    "Antibiotico",
    "Antiinflamatorio",
    "Vitamina",
    "Otro"
]

# Estados de Factura
ESTADOS_FACTURA = ["Pendiente", "Pagada", "Cancelada"]

# Metodos de Pago
METODOS_PAGO = ["Efectivo", "Tarjeta de credito", "Tarjeta de Debito", "Transferencia Bancaria"]

# Tipos de Movimiento Inventario
TIPOS_MOVIMIENTO = ["Entrada", "Salida"]

# Costos de Consulta por Especialidad
COSTOS_CONSULTA = {
    "Medicina General": 80.00,
    "Pediatria": 100.00,
    "Cardiologia": 150.00
}

# Salarios Base por Rol
SALARIOS_BASE = {
    "Doctor": 5000.00,
    "Enfermera": 2500.00,
    "Administrativo": 1800.00
}