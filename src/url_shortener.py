"""
Servicio de acortador de URLs usando TinyURL
Rohayhu Celebra! - Dashboard Integrado
"""

import requests
from urllib.parse import quote


class URLShortener:
    """Servicio para acortar URLs usando TinyURL"""
    
    TINYURL_API = "http://tinyurl.com/api-create.php"
    
    @staticmethod
    def shorten_url(long_url, alias=None):
        """
        Acorta una URL usando TinyURL
        
        Args:
            long_url (str): URL larga a acortar
            alias (str): Alias personalizado opcional
            
        Returns:
            dict: Resultado con success, short_url y message
        """
        try:
            if not long_url:
                return {
                    "success": False,
                    "short_url": "",
                    "message": "URL no puede estar vacía"
                }
            
            # Preparar parámetros para TinyURL
            params = {
                'url': long_url
            }
            
            # Agregar alias si se proporciona
            if alias:
                # Limpiar alias (solo letras, números y guiones)
                clean_alias = ''.join(c for c in alias if c.isalnum() or c in '-_')
                if clean_alias:
                    params['alias'] = clean_alias
            
            # Hacer solicitud a TinyURL
            response = requests.get(URLShortener.TINYURL_API, params=params, timeout=10)
            
            if response.status_code == 200:
                short_url = response.text.strip()
                
                # Verificar si la respuesta es una URL válida
                if short_url.startswith('http'):
                    return {
                        "success": True,
                        "short_url": short_url,
                        "message": "URL acortada exitosamente"
                    }
                else:
                    # TinyURL devuelve un mensaje de error
                    return {
                        "success": False,
                        "short_url": long_url,  # Devolver URL original como fallback
                        "message": f"Error de TinyURL: {short_url}"
                    }
            else:
                return {
                    "success": False,
                    "short_url": long_url,  # Devolver URL original como fallback
                    "message": f"Error HTTP: {response.status_code}"
                }
                
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "short_url": long_url,  # Devolver URL original como fallback
                "message": "Timeout al conectar con TinyURL"
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "short_url": long_url,  # Devolver URL original como fallback
                "message": f"Error de conexión: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "short_url": long_url,  # Devolver URL original como fallback
                "message": f"Error interno: {str(e)}"
            }
    
    @staticmethod
    def create_gift_alias(recipient_name, gift_type="regalo"):
        """
        Crea un alias personalizado para el regalo
        
        Args:
            recipient_name (str): Nombre del destinatario
            gift_type (str): Tipo de regalo
            
        Returns:
            str: Alias sugerido
        """
        try:
            # Limpiar nombre del destinatario
            clean_name = ''.join(c for c in recipient_name.lower() if c.isalnum())
            
            # Crear alias corto
            if len(clean_name) > 10:
                clean_name = clean_name[:10]
            
            alias = f"{gift_type}-{clean_name}"
            return alias
            
        except Exception:
            # Si hay error, devolver alias genérico
            return f"{gift_type}-especial"


# Función de compatibilidad
def shorten_gift_url(long_url, recipient_name=None):
    """
    Función de compatibilidad para acortar URLs de regalo
    
    Args:
        long_url (str): URL larga del regalo
        recipient_name (str): Nombre del destinatario (opcional)
        
    Returns:
        dict: Resultado del acortamiento
    """
    alias = None
    if recipient_name:
        alias = URLShortener.create_gift_alias(recipient_name)
    
    return URLShortener.shorten_url(long_url, alias)
