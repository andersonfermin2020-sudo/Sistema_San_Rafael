"""
Excepciones personalisadas del sistema de acuerdo a la logica de negocio del Hospital

"""
class HospitalException(Exception):
    """
    Excepción base para el sistema hospitalario.
    
    Todas las excepciones personalizadas del sistema deben heredar de esta clase.
    Esto permite identificar y capturar errores específicos de la lógica de negocio
    separándolos de los errores de programación (como ValueError o TypeError).
    
    Ejemplo:
        >>> try:
        ...     logica_del_sistema()
        ... except HospitalException as e:
        ...     # Captura DNIDuplicado, StockInsuficiente, etc.
        ...     print(f"Error del sistema: {e.mensaje}")
    """

    def __init__(self, mensaje="Ha ocurrido un error en el sistema hospitalario"):
        """
        Constructor de la excepción base.

        Args:
            mensaje (str): Mensaje descriptivo del error.
            Por defecto es un mensaje genérico.
        """
        self.mensaje = mensaje
        # Inicializamos la clase Exception de Python con el mensaje
        super().__init__(self.mensaje)

class DNIDuplicadoException(HospitalException):
    """
    Se lanza cuando se intenta registrar un DNI duplicado.
    
    Esta excepción se utiliza en los controladores de Personal y Paciente
    para prevenir que se registre el mismo DNI dos veces en el sistema,
    violando la regla de negocio RN-01.1 y RN-06.1.
    
    Attributos:
        mensaje (str): Descripción detallada del error
    
    Ejemplo:
        En PersonalController:
        >>> if self._dni_existe(dni):
        ...     raise DNIDuplicadoException(f"El DNI {dni} ya está registrado en Personal")
        
        En PacienteController:
        >>> paciente_existente = self.persistencia.buscar_por_dni(dni)
        >>> if paciente_existente:
        ...     raise DNIDuplicadoException(f"Ya existe un paciente con DNI {dni}")
    """
    
    def __init__(self, mensaje="El DNI ya existe en el sistema"):
        """
        Inicializa la excepción con un mensaje descriptivo.
        
        Args:
            mensaje (str, optional): Mensaje de error personalizado.
            Por defecto: "El DNI ya existe en el sistema"
        
        Ejemplo:
            >>> # Con mensaje personalizado
            >>> exc = DNIDuplicadoException("El DNI 12345678 está duplicado")
            >>> print(exc.mensaje)
            El DNI 12345678 está duplicado
            
            >>> # Con mensaje por defecto
            >>> exc = DNIDuplicadoException()
            >>> print(exc.mensaje)
            El DNI ya existe en el sistema
        """
        self.mensaje = mensaje
        super().__init__(self.mensaje)

class RecursoNoEncontradoException(HospitalException):
    """ 
    Se lanza cuando se intenta buscar una entidad (paciente, personal, medicamento, etc) 
    que no esta registrado/a en el sistema 
    
    Atributos:
        mensaje (str): Descripcion detallada del error
        recurso_tipo (str): (Opcional) - Detalla la entidad/recurso no encontrado/a
    
    Ejemplo:
        if not buscar_paciente(DNI):
            raise RecursoNoEncontradoException(f"El paciente con DNI {DNI} no se encuentra registrado")
    """
    
    def __init__(self, mensaje="El recurso o entidad solicitado/a no fue encontrado/a", recurso_tipo=None):
        
        """
        Inicializa la excepcion con un mensaje descriptivo y un atributo opcional
        
        Args:
            mensaje (str, opcional): Mensaje de error personalizado
            recurso_tipo (str, opcional): Representa la entidad/recurso no encontrado
        """
        
        self.mensaje = mensaje
        super().__init__(mensaje)
        self.recurso_tipo = recurso_tipo

class EstadoInvalidoException(HospitalException):
    """
    Se lanza cuando se intenta hacer una operacion en un estado incorrecto
    ej: Pagar una factura ya pagada, cancelar una consulta ya cancelada, etc
    
    Atributos:
        mensaje (str): Describe el mensaje del error
        estado_actual (str): (Opcional) - Estado actual de la entidad
        estado_requerido (str): (Opcional) - Estado requerido para realizar la operacion
        
    Ejemplo:
        (El usario selecciono pagar cuenta en el menu)
        
        if cuenta_encontrada.estado == "pagada":
            raise EstadoInvalidoException("No se puede realizar esta operacion. La cuenta ya se encuentra pagada")
    """
    
    def __init__(self, mensaje="La operación no es válida en el estado actual", estado_actual=None, estado_requerido=None):
        
        """
        Inicializa la excepcion con un mensaje descriptivo y dos atributos opcionales
        
        Args:
            mensaje (str, opcional): Mensaje de error personalizado
            estado_actual (str, opcional): Representa el estado actual de la entidad
            estado_requerido (str, opcional): Representa el estado requerido de la entidad
        """
        
        self.mensaje = mensaje
        super().__init__(mensaje)
        self.estado_actual = estado_actual
        self.estado_requerido = estado_requerido

class StockInsuficienteException(HospitalException):
    """
    Se lanza cuando se intenta recetar una cantidad de un medicamento
    mayor al stock disponible
    
    Atributos:
        mensaje (str): Describe el mensaje del error
        stock_disponible (int): (Opcional) - Cantidad de medicamentos disponible
        cantidad_solicitada (int): (Opcional) - Cantidad solicitada del medicamento
        
    Ejemplo:
    cantidad_solicidad = 10
    cantidad_disponible = medicamento_encontrado.cantidad
    
    try:
        if cantidad_solicitada > cantidad_disponible:
            raise StockInsuficienteException("Operacion invalida. Stock insuficiente en el inventario", cantidad_disponible, cantidad_solicitada)
    except StockInsuficienteException as e:
        print(e.mensaje)
        if e.cantidad_disponible is not None and e.cantidad_solicitada is not None:
            print(f"Stock disponible del medicamento {medicamento_encontrado.nombre}: {e.cantidad_disponible}")
            print(f"Cantidad solicitada: {e.cantidad_solicitada}")
    """
    
    def __init__(self, mensaje="Stock insuficiente para completar la operación", cantidad_disponible=None, cantidad_solicitada=None):
        
        """
        Inicializa la excepcion con un mensaje descriptivo y dos atributos opcionales
        
        Args:
            mensaje (str, opcional): Mensaje de error personalizado
            cantidad_disponible (int, opcional): Representa la cantidad disponible del medicamento
            cantidad_solicitada (int, opcional): Representa la cantidad solicitada del medicamento
        """
        
        self.mensaje = mensaje
        super().__init__(mensaje)
        self.cantidad_disponible = cantidad_disponible
        self.cantidad_solicitada = cantidad_solicitada

class MedicamentoVencidoException(HospitalException):
    """
    Se lanza cuando se intenta recetar un medicamento que se encuentra vencido
    
    Atributos:
        mensaje (str): Descripcion detallada del error
        
    Ejemplo:
    
    fecha_actual: date.today()
    fecha_medicamento = medicamento_encontrado.fecha
    
    if fecha_actual > fecha_medicamento:
        raise MedicamentoVencidoException(f"El medicamento {medicamento_encontrado.nombre} se encuentra vencido.")
    
    """
    
    def __init__(self, mensaje="El medicamento está vencido"):
        
        """
        Inicializa la excepción con un mensaje descriptivo
        
        Args:
        
        mensaje (str, opcional): Mensaje de error personalizado
        Por defecto: "El medicamento está vencido"
        """
        
        self.mensaje = mensaje
        super().__init__(mensaje)

class PermisosDenegadosException(HospitalException):
    """
    Se lanza cuando un usuario desea realizar una accion que su rol no le permite
    
    Atributos:
    mensaje (str): Descripcion detallada del error
    
    Ejemplo:
    (menu de principal, se le pide al usario seleccionar su rol)
    
    selecciona doctor
    
    se le pide que ingrese su DNI 
    
    if usuario_encontrado.estado != "doctor":
        raise PermisosDenegadosException(f"Para acceder al menu de doctores debe de ser uno. Profesion del usuario actual: {usuario_encontrado.estado}")
    """
    
    def __init__(self, mensaje="No tiene permisos para realizar esta acción"):
        
        """
        Inicializa la excepción con un mensaje descriptivo.
        
        Args:
            mensaje (str, optional): Mensaje de error personalizado.
            Por defecto: No tiene permisos para realizar esta acción
        """

        self.mensaje = mensaje
        super().__init__(mensaje)

class ValidationException(HospitalException):
    """ 
    Se lanza cuando falla cualquier validacion de datos (formato, rango, etc)
    
    Atributos:
        mensaje (str): Descripcion detallada del error
        
    Ejemplo:
    nombre_persona: "a"
    
    if len(nombre_persona) < 3:
        raise ValidationException("El nombre a registrar debe de tener entre 3 y 100 caracteres.")
    
    """
    
    def __init__(self, mensaje="Error de validación de datos"):
        """
        Inicializa la excepción con un mensaje descriptivo.
        
        Args:
            mensaje (str, optional): Mensaje de error personalizado.
            Por defecto: "Error de validación de datos"
        """

        self.mensaje = mensaje
        super().__init__(mensaje)
