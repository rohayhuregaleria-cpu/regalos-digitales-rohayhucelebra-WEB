import os
import sendgrid  # <-- ¡IMPORTANTE! Esta línea faltaba
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
        
        # 1. Validar que todos los campos requeridos estén presentes
        required_fields = ['recipient_name', 'recipient_email', 'sender_name', 'gift_url']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'message': f'El campo {field} es requerido'
                }), 400
        
        # 2. Obtener la clave API de las variables de entorno
        sendgrid_api_key = os.environ.get('SENDGRID_API_KEY')
        if not sendgrid_api_key:
            # Si la clave no está configurada, falla con un error claro
            raise ValueError("La clave de API de SendGrid (SENDGRID_API_KEY) no está configurada en el servidor.")

        # 3. Enviar el correo (toda la lógica peligrosa está DENTRO del try)
        result = send_gift_email(
            recipient_name=data['recipient_name'],
            recipient_email=data['recipient_email'],
            sender_name=data['sender_name'],
            gift_url=data['gift_url'],
            sendgrid_api_key=sendgrid_api_key
        )
        
        # 4. Devolver el resultado
        if result['success']:
            return jsonify(result), 200
        else:
            # Si send_gift_email reportó un fallo, lo pasamos al cliente
            return jsonify(result), 500
            
    except Exception as e:
        # Si cualquier cosa en el bloque 'try' falla, este 'except' lo atrapará
        print(f"Error en /send-gift: {str(e)}") # Imprime el error en los logs de Render para depuración
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
