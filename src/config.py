"""
Configuración para la aplicación Flask
Rohayhu Celebra! - Dashboard Integrado
"""

import os


class Config:
    """Configuración base"""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
    
    # Base de datos
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    FLASK_ENV = 'development'


class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    FLASK_ENV = 'production'


# Configuración por defecto
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
