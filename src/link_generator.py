"""
Servicio de generación de enlaces para regalos digitales
Rohayhu Celebra! - Dashboard Integrado
"""

import re
from urllib.parse import urlencode


class LinkGenerator:
    """Generador de enlaces para regalos digitales"""
    
    BASE_URL = "https://rohayhu-celebra-regalos.netlify.app/"
    
    @staticmethod
    def extract_google_drive_id(url):
        """
        Extrae el ID de un enlace de Google Drive
        
        Args:
            url (str): URL de Google Drive
            
        Returns:
            str: ID extraído o cadena vacía si no es válido
        """
        if not url:
            return ""
            
        # Expresión regular para encontrar el ID en varias formas de URL de Google Drive
        regex = r'/d/([a-zA-Z0-9_-]+)'
        match = re.search(regex, url)
        
        if match and match.group(1):
            return match.group(1)
        
        return ""
    
    @staticmethod
    def validate_item(item_type, url):
        """
        Valida un elemento del regalo
        
        Args:
            item_type (str): Tipo de elemento (video, audio, pdf, link)
            url (str): URL del elemento
            
        Returns:
            tuple: (is_valid, processed_url, error_message)
        """
        if not url:
            return False, "", "URL no puede estar vacía"
        
        # Para archivos de Google Drive, extraer el ID
                if item_type in ['video', 'audio', 'pdf', 'storybook']:
            drive_id = LinkGenerator.extract_google_drive_id(url)
            if not drive_id:
                return False, "", f"El enlace para {item_type.upper()} no parece ser un enlace válido de Google Drive"
            
            # CORREGIDO: Usar formato /view que funciona correctamente para todos los tipos
            processed_url = f"https://drive.google.com/file/d/{drive_id}/view"
            
            return True, processed_url, ""
        
        # Para enlaces externos, validar que sea una URL válida
        elif item_type == 'link':
            if not url.startswith(('http://', 'https://')):
                return False, "", "El enlace debe comenzar con http:// o https://"
            return True, url, ""
        
        return False, "", f"Tipo de elemento no válido: {item_type}"
    
    @staticmethod
    def generate_gift_link(recipient_name, items, is_kit=False):
        """
        Genera un enlace de regalo personalizado
        
        Args:
            recipient_name (str): Nombre del destinatario
            items (list): Lista de elementos del regalo
            is_kit (bool): Si es un kit de recuerdos o regalo individual
            
        Returns:
            dict: Resultado con success, url y message
        """
        try:
            if not recipient_name:
                return {
                    "success": False,
                    "url": "",
                    "message": "El nombre del receptor es obligatorio"
                }
            
            if not items:
                return {
                    "success": False,
                    "url": "",
                    "message": "Debes añadir al menos un componente de regalo"
                }
            
            # Validar elementos
            validated_items = []
            for i, item in enumerate(items):
                item_type = item.get('type', '')
                item_url = item.get('url', '')
                
                is_valid, processed_url, error_msg = LinkGenerator.validate_item(item_type, item_url)
                if not is_valid:
                    return {
                        "success": False,
                        "url": "",
                        "message": f"Error en elemento #{i+1}: {error_msg}"
                    }
                
                validated_items.append({
                    'type': item_type,
                    'url': processed_url
                })
            
            # Construir parámetros de URL
            params = {'nombre': recipient_name}
            
            if is_kit:
                # Para kits, permitir múltiples elementos
                params['kit'] = 'true'
                for i, item in enumerate(validated_items):
                    params[f'tipo{i+1}'] = item['type']
                    params[f'url{i+1}'] = item['url']
            else:
                # Para regalo individual, solo un elemento
                if len(validated_items) > 1:
                    return {
                        "success": False,
                        "url": "",
                        "message": "Para un regalo individual (no kit), solo puedes añadir un componente"
                    }
                
                item = validated_items[0]
                params['tipo'] = item['type']
                params['url'] = item['url']
            
            # Generar URL final
            final_url = LinkGenerator.BASE_URL + '?' + urlencode(params)
            
            return {
                "success": True,
                "url": final_url,
                "message": "Enlace generado exitosamente"
            }
            
        except Exception as e:
            return {
                "success": False,
                "url": "",
                "message": f"Error interno: {str(e)}"
            }
    
    @staticmethod
    def get_item_types():
        """
        Retorna los tipos de elementos disponibles
        
        Returns:
            dict: Tipos de elementos con sus descripciones
        """
        return {
            'video': {
                'label': 'VIDEO',
                'placeholder': 'Pega el enlace para compartir de Google Drive',
                'description': 'Video desde Google Drive'
            },
            'audio': {
                'label': 'AUDIO',
                'placeholder': 'Pega el enlace para compartir de Google Drive',
                'description': 'Audio desde Google Drive'
            },
            'pdf': {
                'label': 'PDF',
                'placeholder': 'Pega el enlace para compartir de Google Drive',
                'description': 'Documento PDF desde Google Drive'
            },
            'link': {
                'label': 'LINK',
                'placeholder': 'Pega la URL completa del enlace externo',
                'description': 'Enlace externo'
            }
        }
