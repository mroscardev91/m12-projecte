from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from config import Config 
from flask_login import LoginManager
from flask_principal import Principal


db_manager = SQLAlchemy()
login_manager = LoginManager()
principal_manager =  Principal()

def create_app():
    # Construct the core app object
    app = Flask(__name__)
    login_manager.init_app(app)
    # Configura la aplicación con la clase Config de config.py
    app.config.from_object(Config)
    # ruta absoluta d'aquesta carpeta
    basedir = os.path.abspath(os.path.dirname(__file__)) 

    # paràmetre que farà servir SQLAlchemy per a connectar-se
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + basedir + "/../database.db"
    # mostre als logs les ordres SQL que s'executen
    app.config["SQLALCHEMY_ECHO"] = True

    # Inicialitza els plugins
    login_manager.init_app(app)
    db_manager.init_app(app)
    principal_manager.init_app(app)
    
    with app.app_context():
        from . import routes_main, routes_auth, routes_admin

        # Registra els blueprints
        app.register_blueprint(routes_main.main_bp)
        app.register_blueprint(routes_auth.auth_bp)
        app.register_blueprint(routes_admin.admin_bp)
        

    app.logger.info("Aplicació iniciada")

    return app