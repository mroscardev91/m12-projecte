from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from .models import User, BlockedUser
from . import db_manager as db
from .security import require_admin_role, require_admin_or_moderator_role
from .forms import BlockUserForm

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
    blocked_users = BlockedUser.query.with_entities(BlockedUser.user_id).all()
    blocked_user_ids = {bu.user_id for bu in blocked_users}
    return render_template('admin/users_list.html', users=users, blocked_user_ids=blocked_user_ids)


@admin_bp.route('/admin/users/<int:user_id>/block', methods=['GET', 'POST'])
@login_required
@require_admin_role.require(http_exception=403)
def block_user(user_id):
    user = User.query.get_or_404(user_id)
    form = BlockUserForm()

    if form.validate_on_submit():
        # Lógica para bloquear al usuario
        existing_block = BlockedUser.query.filter_by(user_id=user_id).first()
        if existing_block:
            flash(f'El usuario {user.name} ya está bloqueado.', 'warning')
        else:
            new_block = BlockedUser(user_id=user_id, reason=form.reason.data)
            db.session.add(new_block)
            db.session.commit()
            flash(f'Usuario {user.name} bloqueado por: {form.reason.data}', 'success')
        return redirect(url_for('admin_bp.admin_users'))

    return render_template('admin/block_user.html', form=form, user=user)

@admin_bp.route('/admin/users/<int:user_id>/unblock', methods=['POST'])
@login_required
@require_admin_role.require(http_exception=403)
def unblock_user(user_id):
    blocked_user = BlockedUser.query.filter_by(user_id=user_id).first()
    if blocked_user:
        db.session.delete(blocked_user)
        db.session.commit()
        flash(f'Usuari {blocked_user.user_id} desbloquejat.', 'success')
    else:
        flash('Usuari no trobat o ja desbloquejat.', 'warning')
    return redirect(url_for('admin_bp.admin_users'))