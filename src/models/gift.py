# Archivo: src/models/gift.py

from . import db  # Importamos la instancia 'db' desde el __init__.py del paquete
from datetime import datetime

class Gift(db.Model):
    """
    Representa un regalo digital enviado a través del sistema.
    """
    __tablename__ = 'gifts'

    id = db.Column(db.Integer, primary_key=True)
    
    # Llave foránea opcional para vincular con el sistema de pedidos
    order_id = db.Column(db.String(120), nullable=True, index=True)

    # Información del regalo
    recipient_name = db.Column(db.String(120), nullable=False)
    recipient_email = db.Column(db.String(120), nullable=False)
    sender_name = db.Column(db.String(120), nullable=False)
    
    # URL final del regalo (el packaging digital)
    gift_url = db.Column(db.String(500), nullable=False)
    
    # Campos de seguimiento y auditoría
    sent_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_opened = db.Column(db.Boolean, default=False)
    opened_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<Gift {self.id} for Order {self.order_id or "N/A"}>'

