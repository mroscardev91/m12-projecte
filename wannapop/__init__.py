from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
import os
from config import Config 
from flask_login import LoginManager
from flask_principal import Principal
from logging.handlers import RotatingFileHandler
import logging
from flask_httpauth import HTTPBasicAuth
from flask_wtf.csrf import CSRFProtect
from flask import current_app


db_manager = SQLAlchemy()
login_manager = LoginManager()
principal_manager = Principal()

def create_app():
    # Construct the core app object
    app = Flask(__name__)
    # Configura la aplicación con la clase Config de config.py
    app.config.from_object(Config)
    # ruta absoluta d'aquesta carpeta
    basedir = os.path.abspath(os.path.dirname(__file__)) 
    app.debug = True
    # paràmetre que farà servir SQLAlchemy per a connectar-se
    # app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + basedir + "/../database.db"
    # mostre als logs les ordres SQL que s'executen
    app.config["SQLALCHEMY_ECHO"] = True

    log_handler = RotatingFileHandler('app.log', maxBytes=10240, backupCount=3)
    log_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
    ))
    app.logger.addHandler(log_handler)

    log_level = app.config.get('LOG_LEVEL')
    if log_level not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
        raise ValueError('Nivell de registre no vàlid')
    app.logger.setLevel(getattr(logging, log_level))


    # Inicialitza els plugins
    login_manager.init_app(app)
    db_manager.init_app(app)
    principal_manager.init_app(app)
    toolbar = DebugToolbarExtension(app)
    
    with app.app_context():
        from . import routes_main, routes_auth, routes_admin
        from .api import api_bp

        # Registra els blueprints
        app.register_blueprint(routes_main.main_bp)
        app.register_blueprint(routes_auth.auth_bp)
        app.register_blueprint(routes_admin.admin_bp)
        app.register_blueprint(api_bp, url_prefix='/api/v1.0')

    app.logger.info("Aplicació iniciada")

    return app