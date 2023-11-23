from flask import Blueprint, render_template
from flask_login import current_user, login_required
from .models import User
from . import db_manager as db

# Crear un Blueprint anomenat 'admin'
admin_bp = Blueprint(
    "admin_bp", __name__, template_folder="templates", static_folder="static"
)

# Ruta per a la pàgina principal d'administració
@admin_bp.route('/')
def admin_index():
    return render_template('admin/index.html')