# Archivo: src/routes/gift.py

import os
from flask import Blueprint, request, jsonify, redirect
from datetime import datetime
from src.models import db
from src.models.gift import Gift
from src.email_service import send_gift_email

gift_bp = Blueprint('gift', __name__)

@gift_bp.route('/send-gift', methods=['POST'])
def send_gift():
    """
    Endpoint principal para enviar un regalo.
    Guarda el registro en la BD y envía el correo con un enlace de seguimiento.
    """
    try:
        data = request.get_json()
        
        required_fields = ['recipient_name', 'recipient_email', 'sender_name', 'gift_url']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'El campo {field} es requerido'}), 400
        
        # 1. Crear la instancia del regalo con los datos recibidos
        new_gift = Gift(
            order_id=data.get('order_id'),  # Acepta el order_id si viene, si no, será None
            recipient_name=data['recipient_name'],
            recipient_email=data['recipient_email'],
            sender_name=data['sender_name'],
            gift_url=data['gift_url']
        )
        
        db.session.add(new_gift)
        db.session.flush()  # Asigna un ID al 'new_gift' sin hacer commit todavía

        # 2. Construir la URL de seguimiento única para este regalo
        base_url = "https://packaging-regalos-digitales.onrender.com"
        tracking_url = f"{base_url}/api/track/{new_gift.id}"

        # 3. Enviar el correo usando la URL de seguimiento
        sendgrid_api_key = os.environ.get('SENDGRID_API_KEY' )
        if not sendgrid_api_key:
            raise ValueError("La clave de API de SendGrid (SENDGRID_API_KEY) no está configurada.")

        result = send_gift_email(
            recipient_name=data['recipient_name'],
            recipient_email=data['recipient_email'],
            sender_name=data['sender_name'],
            gift_url=tracking_url,  # ¡Importante! Usamos la URL de seguimiento
            sendgrid_api_key=sendgrid_api_key
        )
        
        # 4. Confirmar o deshacer la operación en la base de datos
        if result['success']:
            db.session.commit()  # Si el correo se envió, guardamos permanentemente en la BD
            return jsonify(result), 200
        else:
            db.session.rollback()  # Si el correo falló, no guardamos nada
            return jsonify(result), 500
            
    except Exception as e:
        db.session.rollback()  # Si ocurre cualquier otro error, deshacemos todo
        print(f"Error en /send-gift: {str(e)}")
        return jsonify({'success': False, 'message': f'Error interno del servidor: {str(e)}'}), 500

@gift_bp.route('/track/<int:gift_id>', methods=['GET'])
def track_gift_opening(gift_id):
    """
    Endpoint que es llamado cuando el usuario hace clic en el botón del correo.
    Registra la apertura y redirige al usuario al regalo final.
    """
    try:
        gift_to_track = db.session.get(Gift, gift_id)

        if not gift_to_track:
            return "Regalo no encontrado.", 404

        # Solo registramos la primera apertura
        if not gift_to_track.is_opened:
            gift_to_track.is_opened = True
            gift_to_track.opened_at = datetime.utcnow()
            db.session.commit()

        # Redirigimos al usuario a la URL final del regalo
        return redirect(gift_to_track.gift_url)

    except Exception as e:
        print(f"Error en /track/{gift_id}: {str(e)}")
        return "Ha ocurrido un error al procesar tu regalo.", 500

@gift_bp.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificar que la API está funcionando."""
    return jsonify({'success': True, 'message': 'API de Rohayhu Celebra funcionando correctamente'}), 200
