from flask import Blueprint, render_template
from flask_login import current_user, login_required
from .models import User
from . import db_manager as db
from .security import require_admin_role, require_admin_or_moderator_role

# Crear un Blueprint anomenat 'admin'
admin_bp = Blueprint(
    "admin_bp", __name__, template_folder="templates", static_folder="static"
)

# Ruta per a la pàgina principal d'administració
@admin_bp.route('/admin')
@login_required
@require_admin_or_moderator_role.require(http_exception=403)
def admin_index():
    return render_template('admin/index.html')

@admin_bp.route('/admin/users')
@login_required
@require_admin_role.require(http_exception=403)
def admin_users():
    users = db.session.query(User).all()
    return render_template('admin/users_list.html', users=users)