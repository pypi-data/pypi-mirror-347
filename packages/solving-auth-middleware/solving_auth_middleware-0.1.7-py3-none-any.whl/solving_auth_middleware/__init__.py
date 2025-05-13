from flask import Flask
from .config import Config
from .middleware import requires_permissions

__version__ = '0.1.7'

def create_app(config_class=Config):
    """Crée et configure une nouvelle instance de l'application Flask."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    config_class.init_app(app)
    return app

__all__ = ['create_app', 'requires_permissions', 'Config']
