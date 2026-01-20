"""
Constantes del sistema 

"""

# Roles de Personal
ROLES_PERSONAL = ["Doctor", "Enfermera", "Administrativo"]

# Especialidades Medicas
ESPECIALIDADES = ["Medicina General", "Pediatria", "Cardiologia"]

# Tipos de Contrato
TIPOS_CONTRATOS = ["Temporal", "Indefinido", "Por honorarios"]

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