import os

from flask import Blueprint, request, jsonify
from src.email_service import send_gift_email

gift_bp = Blueprint('gift', __name__)

@gift_bp.route('/send-gift', methods=['POST'])
def send_gift():
    """
    Endpoint para enviar un correo electrónico de regalo.
    
    Espera un JSON con:
    - recipient_name: Nombre del destinatario
    - recipient_email: Email del destinatario
    - sender_name: Nombre del remitente
    - gift_url: URL del regalo
    """
    try:
        data = request.get_json()
        
        # Validar que todos los campos requeridos estén presentes
        required_fields = ['recipient_name', 'recipient_email', 'sender_name', 'gift_url']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'message': f'El campo {field} es requerido'
                }), 400
        
        # Clave API de SendGrid (en un entorno de producción, esto debería estar en variables de entorno)      
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))

        
        # Enviar el correo
        result = send_gift_email(
            recipient_name=data['recipient_name'],
            recipient_email=data['recipient_email'],
            sender_name=data['sender_name'],
            gift_url=data['gift_url'],
            sendgrid_api_key=sendgrid_api_key
        )
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error interno del servidor: {str(e)}'
        }), 500

@gift_bp.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificar que la API está funcionando."""
    return jsonify({
        'success': True,
        'message': 'API de Rohayhu Celebra funcionando correctamente'
    }), 200
