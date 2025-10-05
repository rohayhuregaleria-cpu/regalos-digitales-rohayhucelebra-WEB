"""
Rutas API para la generación de enlaces de regalo
Rohayhu Celebra! - Dashboard Integrado
"""

from flask import Blueprint, request, jsonify
from src.link_generator import LinkGenerator

link_bp = Blueprint('link', __name__)


@link_bp.route('/generate-link', methods=['POST'])
def generate_link():
    """
    Genera un enlace de regalo personalizado
    
    Expected JSON payload:
    {
        "recipient_name": "María González",
        "is_kit": false,
        "items": [
            {
                "type": "video",
                "url": "https://drive.google.com/file/d/1ABC123/view"
            }
        ]
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "url": "",
                "message": "No se recibieron datos"
            }), 400
        
        recipient_name = data.get('recipient_name', '').strip()
        is_kit = data.get('is_kit', False)
        items = data.get('items', [])
        
        # Generar el enlace usando el servicio
        result = LinkGenerator.generate_gift_link(
            recipient_name=recipient_name,
            items=items,
            is_kit=is_kit
        )
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            "success": False,
            "url": "",
            "message": f"Error interno del servidor: {str(e)}"
        }), 500


@link_bp.route('/item-types', methods=['GET'])
def get_item_types():
    """
    Obtiene los tipos de elementos disponibles para los regalos
    """
    try:
        item_types = LinkGenerator.get_item_types()
        return jsonify({
            "success": True,
            "item_types": item_types
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error interno del servidor: {str(e)}"
        }), 500


@link_bp.route('/validate-drive-url', methods=['POST'])
def validate_drive_url():
    """
    Valida una URL de Google Drive y extrae el ID
    
    Expected JSON payload:
    {
        "url": "https://drive.google.com/file/d/1ABC123/view"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "message": "No se recibieron datos"
            }), 400
        
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({
                "success": False,
                "message": "URL no puede estar vacía"
            }), 400
        
        drive_id = LinkGenerator.extract_google_drive_id(url)
        
        if drive_id:
            return jsonify({
                "success": True,
                "drive_id": drive_id,
                "message": "URL de Google Drive válida"
            }), 200
        else:
            return jsonify({
                "success": False,
                "drive_id": "",
                "message": "URL de Google Drive no válida"
            }), 400
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error interno del servidor: {str(e)}"
        }), 500
