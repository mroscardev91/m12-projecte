from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from config import Config 

db_manager = SQLAlchemy()

def create_app():
    # Construct the core app object
    app = Flask(__name__)

    # Configura la aplicación con la clase Config de config.py
    app.config.from_object(Config)
    # ruta absoluta d'aquesta carpeta
    basedir = os.path.abspath(os.path.dirname(__file__)) 

    # paràmetre que farà servir SQLAlchemy per a connectar-se
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + basedir + "/../database.db"
    # mostre als logs les ordres SQL que s'executen
    app.config["SQLALCHEMY_ECHO"] = True

    # Inicialitza els plugins
    db_manager.init_app(app)

    with app.app_context():
        from . import routes_main

        # Registra els blueprints
        app.register_blueprint(routes_main.main_bp)

    app.logger.info("Aplicació iniciada")

    return app