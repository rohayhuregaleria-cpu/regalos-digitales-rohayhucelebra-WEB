from .user import db  # <-- ¡CLAVE! Importamos la instancia 'db' desde user.py
from datetime import datetime

class Gift(db.Model):
    __tablename__ = 'gifts'

    id = db.Column(db.Integer, primary_key=True)
    recipient_name = db.Column(db.String(120), nullable=False)
    recipient_email = db.Column(db.String(120), nullable=False)
    sender_name = db.Column(db.String(120), nullable=False)
    gift_url = db.Column(db.String(500), nullable=False)
    sent_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    is_opened = db.Column(db.Boolean, default=False)
    opened_at = db.Column(db.DateTime, nullable=True)

    # Opcional: Relación con la tabla User
    # sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    # sender = db.relationship('User', backref=db.backref('sent_gifts', lazy=True))

    def __repr__(self):
        return f'<Gift {self.id} to {self.recipient_email}>'
