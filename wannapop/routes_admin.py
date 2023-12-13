from flask import Blueprint, render_template, current_app
from flask_login import current_user, login_required
from .models import User, Product, BannedProducts
from . import db_manager as db
from .security import require_admin_role, require_admin_or_moderator_role, require_moderator_role

# Crear un Blueprint anomenat 'admin'
admin_bp = Blueprint(
    "admin_bp", __name__, template_folder="templates", static_folder="static"
)

# Ruta per a la pàgina principal d'administració
@admin_bp.route('/admin')
@login_required
@require_admin_or_moderator_role.require(http_exception=403)
def admin_index():
    current_app.logger.info('Accés a la pàgina d\'administració')
    return render_template('admin/index.html')

@admin_bp.route('/admin/users')
@login_required
@require_admin_role.require(http_exception=403)
def admin_users():
    current_app.logger.info('Accés a la pàgina d\'administració d\'usuaris')
    users = db.session.query(User).all()
    return render_template('admin/users_list.html', users=users)

@admin_bp.route('/admin/products/<int:product_id>/ban', methods=['POST'])
@login_required
@require_moderator_role.require(http_exception=403)
def ban_product(product_id):
    product = Product.query.get(product_id)

    if product:
        # Verifica si el producto ya está en la lista de productos prohibidos
        existing_ban = BannedProducts.query.filter_by(product_id=product_id).first()

        if not existing_ban:
            # Si no está prohibido, crea un registro en la tabla de productos prohibidos
            banned_products = BannedProducts(product_id=product_id, reason="Razón opcional")
            db.session.add(banned_products)
            db.session.commit()
            current_app.logger.info(f'Producto {product_id} prohibido por el administrador')
            return {"message": f"Producto {product_id} prohibido exitosamente"}, 200
        else:
            return {"message": "Producto ya está prohibido"}, 400
    else:
        return {"message": "Producto no encontrado"}, 404

@admin_bp.route('/admin/products/<int:product_id>/unban', methods=['POST'])
@login_required
@require_moderator_role.require(http_exception=403)
def unban_product(product_id):
    product = Product.query.get(product_id)

    if product:
        # Verifica si el producto está en la lista de productos prohibidos y lo elimina
        banned_products = BannedProducts.query.filter_by(product_id=product_id).first()

        if banned_products:
            db.session.delete(banned_products)
            db.session.commit()
            current_app.logger.info(f'Producto {product_id} desprohibido por el administrador')
            return {"message": f"Producto {product_id} desprohibido exitosamente"}, 200
        else:
            return {"message": "Producto no está prohibido"}, 400
    else:
        return {"message": "Producto no encontrado"}, 404