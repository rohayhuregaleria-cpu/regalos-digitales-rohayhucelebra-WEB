import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from src.config import Config

def send_gift_email(recipient_name, recipient_email, sender_name, gift_url, sendgrid_api_key=None):
    """
    Envía un correo electrónico de regalo personalizado usando SendGrid.
    
    Args:
        recipient_name (str): Nombre del destinatario
        recipient_email (str): Email del destinatario
        sender_name (str): Nombre del remitente
        gift_url (str): URL del regalo
        sendgrid_api_key (str): Clave API de SendGrid
    
    Returns:
        dict: Resultado del envío con status y mensaje
    """
    try:
        # Usar la clave API de la configuración si no se proporciona
        if sendgrid_api_key is None:
            sendgrid_api_key = Config.SENDGRID_API_KEY
        
        # Ruta de la plantilla de email (relativa al directorio raíz del proyecto)
        email_template_path = "plantilla_email.html"
        
        # Leer la plantilla de correo electrónico
        with open(email_template_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Reemplazar marcadores de posición
        html_content = html_content.replace('[Nombre del Destinatario]', recipient_name)
        html_content = html_content.replace('[Nombre del Remitente]', sender_name)
        html_content = html_content.replace('URL_DEL_REGALO_AQUI', gift_url)

        # Asunto del correo electrónico
        subject = f'🎁 {sender_name} te ha enviado un regalo especial'

        # Crear el mensaje de correo electrónico
        message = Mail(
            from_email='rohayhuregaleria@gmail.com',  # Remitente verificado en SendGrid
            to_emails=recipient_email,
            subject=subject,
            html_content=html_content
        )

        # Enviar el correo
        sendgrid_client = SendGridAPIClient(sendgrid_api_key)
        response = sendgrid_client.send(message)
        
        return {
            'success': True,
            'status_code': response.status_code,
            'message': f'Correo enviado exitosamente a {recipient_email}'
        }
        
    except FileNotFoundError:
        return {
            'success': False,
            'message': 'No se pudo encontrar la plantilla de correo electrónico'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Error al enviar el correo: {str(e)}'
        }
