import os
import sys
from flask import Flask, send_from_directory

# --- Configuración de Rutas del Proyecto ---
# NO CAMBIAR ESTO: Permite que la app encuentre los módulos en 'src'
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# --- Importaciones de la Aplicación ---
from src.config import config
from src.models import db  # Importación ÚNICA y centralizada de la instancia de la BD
from src.routes.user import user_bp
from src.routes.gift import gift_bp
from src.routes.link_generator_routes import link_bp

# --- Creación y Configuración de la App Flask ---

def create_app():
    """
    Función de fábrica para crear la aplicación Flask.
    Esto hace que la app sea más modular y fácil de probar.
    """
    # Determinar el entorno (producción o desarrollo)
    config_name = os.environ.get('FLASK_ENV', 'development')
    app_config = config.get(config_name, config['default'])

    # Crear la instancia de la aplicación Flask
    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
    
    # Cargar la configuración desde el objeto (ej. SECRET_KEY, DATABASE_URL)
    app.config.from_object(app_config)

    # --- Inicialización de Componentes ---

    # Inicializar la base de datos con la app
    db.init_app(app)

    # --- Registro de Blueprints (Rutas) ---
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(gift_bp, url_prefix='/api')
    app.register_blueprint(link_bp, url_prefix='/api')

    # --- Creación de Tablas de la Base de Datos ---
    with app.app_context():
        # Crea todas las tablas (users, gifts) si no existen.
        # En un entorno de producción más avanzado, esto se manejaría con migraciones (Alembic).
        db.create_all()

    # --- Rutas Estáticas y de Raíz ---
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        static_folder_path = app.static_folder
        if static_folder_path is None:
            return "Static folder not configured", 404

        if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
            return send_from_directory(static_folder_path, path)
        else:
            index_path = os.path.join(static_folder_path, 'index.html')
            if os.path.exists(index_path):
                return send_from_directory(static_folder_path, 'index.html')
            else:
                return "index.html not found", 404
    
    return app

# --- Punto de Entrada para Ejecución ---

# Crear la aplicación usando la función de fábrica
app = create_app()

if __name__ == '__main__':
    # Este bloque solo se ejecuta cuando corres 'python src/main.py' localmente
    port = int(os.environ.get('PORT', 5000))
    # El modo debug se activa si FLASK_ENV no es 'production'
    debug = app.config.get('DEBUG', False)
    app.run(host='0.0.0.0', port=port, debug=debug)


