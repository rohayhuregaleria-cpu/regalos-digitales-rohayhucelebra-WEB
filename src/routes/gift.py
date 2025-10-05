import os
import sendgrid
from flask import Blueprint, request, jsonify, redirect
from datetime import datetime

# Importamos la instancia de la BD y el Modelo desde nuestro paquete 'models'
from src.models import db, Gift 
from src.email_service import send_gift_email

gift_bp = Blueprint('gift', __name__)

@gift_bp.route('/send-gift', methods=['POST'])
def send_gift():
    """
    Endpoint para enviar un correo de regalo, guardar el registro en la BD
    y generar un enlace de seguimiento.
    """
    try:
        data = request.get_json()
        
        # 1. Validar que todos los campos requeridos estén presentes
        required_fields = ['recipient_name', 'recipient_email', 'sender_name', 'gift_url']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'El campo {field} es requerido'}), 400
        
        # 2. Crear la instancia del regalo para la base de datos
        new_gift = Gift(
            recipient_name=data['recipient_name'],
            recipient_email=data['recipient_email'],
            sender_name=data['sender_name'],
            gift_url=data['gift_url']  # Guardamos la URL final de destino
        )

        # 3. Añadir a la sesión y hacer 'flush' para obtener el ID del nuevo regalo
        db.session.add(new_gift)
        db.session.flush()

        # 4. Construir la URL de seguimiento única para este regalo
        #    Esta URL apuntará a nuestro endpoint '/track/<gift_id>'
        base_url = "https://packaging-regalos-digitales.onrender.com"
        tracking_url = f"{base_url}/api/track/{new_gift.id}"

        # 5. Preparar y enviar el correo electrónico
        sendgrid_api_key = os.environ.get('SENDGRID_API_KEY' )
        if not sendgrid_api_key:
            raise ValueError("La clave de API de SendGrid (SENDGRID_API_KEY) no está configurada.")

        # ¡IMPORTANTE! Pasamos la 'tracking_url' a la plantilla del correo,
        # no la 'gift_url' original.
        result = send_gift_email(
            recipient_name=data['recipient_name'],
            recipient_email=data['recipient_email'],
            sender_name=data['sender_name'],
            gift_url=tracking_url,
            sendgrid_api_key=sendgrid_api_key
        )
        
        # 6. Gestionar la transacción de la base de datos
        if result['success']:
            # Si el correo se envió con éxito, confirmamos los cambios en la BD
            db.session.commit()
            return jsonify(result), 200
        else:
            # Si el envío del correo falló, revertimos la inserción en la BD
            db.session.rollback()
            return jsonify(result), 500
            
    except Exception as e:
        # Si ocurre cualquier otro error, revertimos la transacción
        db.session.rollback()
        print(f"Error en /send-gift: {str(e)}")
        return jsonify({'success': False, 'message': f'Error interno del servidor: {str(e)}'}), 500


@gift_bp.route('/track/<int:gift_id>', methods=['GET'])
def track_gift_opening(gift_id):
    """
    Este endpoint se llama cuando el usuario hace clic en el botón del correo.
    Registra la apertura y redirige al destino final.
    """
    try:
        # Buscar el regalo en la base de datos por su ID
        gift_to_track = Gift.query.get(gift_id)

        if not gift_to_track:
            return "Regalo no encontrado o enlace inválido.", 404

        # Marcar como abierto y guardar la fecha (solo la primera vez)
        if not gift_to_track.is_opened:
            gift_to_track.is_opened = True
            gift_to_track.opened_at = datetime.utcnow()
            db.session.commit()

        # Redirigir al usuario a la URL final y original del regalo
        return redirect(gift_to_track.gift_url)

    except Exception as e:
        print(f"Error al rastrear el regalo {gift_id}: {str(e)}")
        # Si algo falla, como mínimo intentamos redirigir al usuario
        # para no romper su experiencia.
        gift_to_track = Gift.query.get(gift_id)
        if gift_to_track:
            return redirect(gift_to_track.gift_url)
        # Si ni siquiera podemos encontrar el regalo, mostramos un error.
        return "Ha ocurrido un error al procesar tu solicitud.", 500


@gift_bp.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificar que la API está funcionando."""
    return jsonify({
        'success': True,
        'message': 'API de Rohayhu Celebra funcionando correctamente'
    }), 200

