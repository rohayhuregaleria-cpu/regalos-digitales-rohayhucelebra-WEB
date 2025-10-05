from flask_sqlalchemy import SQLAlchemy

# Esta es la instancia ÚNICA de la base de datos para toda la app.
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users' # Es buena práctica definir el nombre de la tabla
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email # Corregí un typo aquí, era 'Email' con mayúscula
        }
