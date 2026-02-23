"""Funciones de mensajes para mostrar al usuario reutulizables en el sistema"""
class Mensajes:
    """Componente encargado de la retroalimentacion visual en consola"""
    
    @staticmethod
    def mostrar(resultado: dict):
        """
        Analiza el diccionario del controlador y muestra el mensaje con el 
        estilo correspondiente (Exito o Error)
        """
        
        # Extraemos el valor del exito y del mensaje
        exito = resultado.get("exito", False)
        mensaje = resultado.get("mensaje", "Sin mensaje descriptivo")
        
        if exito:
            # Buscamos informacion adicional (id, datos, etc)
            informacion = {k: v for k, v in resultado.items() if k not in ['exito', 'mensaje']}
            Mensajes._plantilla_exito(mensaje, informacion)
        else:
            Mensajes._plantilla_error(mensaje)
    
    @staticmethod
    def _plantilla_exito(mensaje: str, info: dict):
        """Muestra mensaje de exito segun la plantilla del diseno"""
        
        print("\n" + "=" * 50)
        print(f"  ✓ ÉXITO: {mensaje}")
        
        # Si hay datos adicionales se muestran
        if info:
            for clave, valor in info.items():
                print(f"  {clave.upper()}: {valor}")
        
        print("="*50)
        input("\nPresione Enter para continuar...")
    
    @staticmethod
    def _plantilla_error(mensaje: str):
        """Muestra mensaje de error segun la plantilla del diseno"""
        
        print("\n" + "=" * 50)
        print(f"  ✗ ERROR: {mensaje}")
        print("  Sugerencia: Verifique los datos e intente nuevamente.")
        print("=" * 50)
        input("\nPresione Enter para continuar...") 
    
    @staticmethod
    def mostrar_advertencia(mensaje: str):
        """Para casos que no vienen del controlador pero requieren atención."""
        print(f"\n  ! ADVERTENCIA: {mensaje}")
        input("Presione Enter para continuar...")