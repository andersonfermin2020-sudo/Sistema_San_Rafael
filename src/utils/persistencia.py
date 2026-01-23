"""
Manejo de operaciones sobre archivos JSON

"""
import json
import os
from typing import List, Dict, Any, Optional
class Persistencia:
    """
    Maneja operaciones CRUD sobre archivos JSON.
    
    Cada instancia trabaja con UN archivo JSON específico.
    """

    def __init__(self, archivo: str):
        """
        Inicializa con la ruta del archivo
        
        Args:
            archivo (str): Ruta del archivo que manejara la instancia ej: data/personal.json
        
        """
        
        self.archivo = archivo
        # Nos aseguramos que el archivo exista
        self._inicializar_archivo()

    def _inicializar_archivo(self):
        """Crea el archivo si no existe con una lista vacia"""
        
        # Verificar que el archivo exista, si no existe lo crea 
        if not os.path.exists(self.archivo):
            directorio = os.path.dirname(self.archivo)
            if directorio and not os.path.exists(directorio):
                os.makedirs(directorio)
            
            with open(self.archivo, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    def leer_todos(self) -> List[Dict]:
        """
        Lee todos los registros del archivo
        
        Returns: 
            List[Dict]: Lista de diccionarios
        
        """
        
        # Leemos el archivo con los datos y los retornas en estructuras propias del programa
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                return json.load(f)
            
        # Si hubo un error de json se retorna una lista vacia
        except json.JSONDecodeError:
            return []
        
        # Si hubo otro tipo de error se lanza una exception con un mensaje
        except Exception as e:
            raise Exception(f"Error al leer {self.archivo}: {str(e)}")

    def guardar_todos(self, datos: List[Dict]) -> bool:
        """
        Sobrescribe el archivo con nuevos datos
        
        Args:
            List[Dict]: Lista de diccionarios a guardar
            
        Returns:
            bool: True si se guardaron los datos correctamente

        """
        # Sobreescribimos el archivo con los nuevos datos
        try:
            with open(self.archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
            return True
        
        # Se lanza un Exception si algo salio mal
        except Exception as e:
            raise Exception(f"Error al guardar {self.archivo}: {str(e)}")

    def agregar(self, registro: Dict) -> bool:
        """
        Agrega un registro al archivo
        
        Args:
            registro (Dict): Diccionario nuevo a guardar
            
        Returns:
            bool: True si se guardo correctamente
        
        """
        # Capturamos todos los datos del archivo
        datos = self.leer_todos()
        
        # Agregamos el registro
        datos.append(registro)
        
        # Llamamos al metodo de guardar todo y retornamos su resultado
        return self.guardar_todos(datos)

    def buscar_por_id(self, id_valor: int, campo_id: str = None) -> Optional[Dict]:
        """
        Busca un registro por su ID
        
        Args:
            id_valor (int): valor a buscar
            campo_id (str | None): Campo del ID, si no se especifica se infiere del archivo
            
        Returns:
            Diccionario si encontro el registro. None si no lo encontro
        """
        # Si no se especifico el nombre del campo lo deducimos por el nombre del archivo
        if campo_id is None:
            nombre_archivo = os.path.basename(self.archivo).replace('.json', '')
            campo_id = f"id_{nombre_archivo[:-1]}" if nombre_archivo.endswith('s') else f"id_{nombre_archivo}"
            
        datos = self.leer_todos()
        
        # Si se encontro un registro con ese ID se retorna
        for registro in datos:
            if registro.get(campo_id) == id_valor:
                return registro
            
        # Si no se encontro se retorna None
        return None

    def buscar(self, criterios: Dict) -> List[Dict]:
        """
        Busca registros que cumplan criterios
        
        Args:
            criterios (Dict): Diccionario con valores a buscar 
            
        Returs:
            List[Dict]: Lista de diccionario con registros que cumplen los criterios
        """
        
        datos = self.leer_todos()
        resutados = []
        
        # Buscamos registros que cumplan todos los criterios
        for registro in datos:
            cumple = True
            for llave, valor in criterios.items():
                if registro.get(llave) != valor:
                    cumple = False
                    break
            if cumple:
                resutados.append(registro)
        
        # Se retorna los registros encontrados o una lista vacia
        return resutados

    def actualizar(self, id_valor: int, campos_actualizar: Dict, campo_id: str = None) -> bool:
        """
        Actualiza campos de un registro
        
        Args:
            id_valor (int): ID a buscar
            campos_actualizar (Dict): Diccionario con los valores a actualizar
            campo_id (str | None): Nombre del campo del ID
            
        Returns:
            bool: True si se encontro
        """
        
        # Si no se especifico el nombre del campo del ID se infiere mendiente el nombre del archivo
        if campo_id is None:
            nombre_archivo = os.path.basename(self.archivo).replace('.json', '')
            campo_id = f"id_{nombre_archivo[:-1]}" if nombre_archivo.endswith('s') else f"id_{nombre_archivo}"
            
        datos = self.leer_todos()
        
        # Buscamos el registro por ID para actualizar los datos
        for registro in datos:
            if registro.get(campo_id) == id_valor:
                registro.update(campos_actualizar)
                return self.guardar_todos(datos)
        
        # Si no se encontro se retorna False
        return False

    def eliminar(self, id_valor: int, campo_id: str = None) -> bool:
        """
        Elimina un registro (NO usar en Personal/Pacientes)
        
        NOTA: Este metodo aplica para registros que no sean de pacientes/personal por politicas del negocio
        
        Args:
            id_valor (int): ID a buscar para eliminar registro
            campo_id (str | None): Nombre del campo del ID
        
        Returns:
            bool: True si se logro eliminar el registro
        
        """
        
        # Si no se especifica el campo del ID se infiere mediante el nombre del archivo
        if campo_id is None:
            nombre_archivo = os.path.basename(self.archivo).replace('.json', '')
            campo_id = f"id_{nombre_archivo[:-1]}" if nombre_archivo.endswith('s') else f"id_{nombre_archivo}"
            
        datos = self.leer_todos()
        
        # Se guardan los registros que no tengan ese ID
        datos_obtenidos = [dato for dato in datos if dato.get(campo_id) != id_valor]
        
        if len(datos_obtenidos) < len(datos):
            return self.guardar_todos(datos_obtenidos)
        return False

    def generar_id_autoincremental(self, campo_id: str = None) -> int:
        """
        Genera un ID único auto-incremental
        
        Args:
            campo_id (str): Nombre del campo del ID
            
        Returns:
            int: Nuevo ID (maximo + 1)
        """
        datos = self.leer_todos()
        
        # Si no tiene registros retornamos 1
        if not datos:
            return 1
        
        # Si no se especifica el campo del ID se infiere mediante el nombre del archivo
        if campo_id is None:
            nombre_archivo = os.path.basename(self.archivo).replace('.json', '')
            campo_id = f"id_{nombre_archivo[:-1]}" if nombre_archivo.endswith('s') else f"id_{nombre_archivo}"
        
        # En contramos el mayor ID y retornamos (mayor + 1)
        maximo_id = max([dato.get(campo_id, 0) for dato in datos])
        return maximo_id + 1
