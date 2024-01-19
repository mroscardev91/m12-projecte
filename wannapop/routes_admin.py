from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app, redirect, url_for, request
from flask_login import current_user, login_required
from .models import User, BlockedUser, Product, BannedProducts, Category
from .security import require_admin_role, require_admin_or_moderator_role, require_moderator_role
from .forms import BlockUserForm

# Crear un Blueprint anomenat 'admin'
admin_bp = Blueprint(
    "admin_bp", __name__, template_folder="templates", static_folder="static"
)

def get_ban_reason(product_id):
    banned_product = BannedProducts.query.filter_by(product_id=product_id).first()

    if banned_product:
        return banned_product.reason
    else:
        return None

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
    users = User.get_all()
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

@admin_bp.route('/products/list/admin')
@login_required
@require_moderator_role.require(http_exception=403)
def product_list():
    # select amb join que retorna una llista dwe resultats
    products_with_category = Product.get_all_with(Category)
    
    banned_products = [banned.product_id for banned in BannedProducts.query.all()]

    
    return render_template('admin/list.html', products_with_category = products_with_category, banned_products=banned_products)

@admin_bp.route('/products/read/<int:product_id>/admin')
@login_required
@require_moderator_role.require(http_exception=403)
def product_read(product_id):
    # select amb join i 1 resultat
    (product, category) = Product.get_with(product_id, Category)
    # Verifica si el producto está prohibido y obtén la razón del ban
    ban_reason = get_ban_reason(product_id)

    return render_template('admin/read.html', product=product, category=category, ban_reason=ban_reason)

@admin_bp.route('/admin/products/<int:product_id>/ban', methods=['POST'])
@login_required
@require_moderator_role.require(http_exception=403)
def ban_product(product_id):
    product = Product.get(product_id)

    if product:
        # Verifica si el producto ya está en la lista de productos prohibidos
        existing_ban = BannedProducts.query.filter_by(product_id=product_id).first()

        if not existing_ban:
            # Si no está prohibido, obtén el nombre del producto y redirige a la ruta para ingresar la razón
            product_name = product.title
            return redirect(url_for('admin_bp.enter_ban_reason', product_id=product_id, product_name=product_name))
        else:
            return {"message": "El producto ya está prohibido"}, 400
    else:
        return {"message": "Producto no encontrado"}, 404

@admin_bp.route('/admin/products/<int:product_id>/enter_ban_reason', methods=['GET', 'POST'])
@login_required
@require_moderator_role.require(http_exception=403)
def enter_ban_reason(product_id):
    if request.method == 'POST':
        # Recuperar la razón del formulario y agregar el registro a la tabla de productos prohibidos
        reason = request.form.get('reason')
        banned_products = BannedProducts(product_id=product_id, reason=reason)
        banned_products.save()
        current_app.logger.info(f'Producto {product_id} prohibido por el administrador')
        return render_template('admin/ban_product.html', product_id=product_id, reason=reason)
    
    # Si es una solicitud GET, simplemente renderiza el formulario para ingresar la razón
    product_name = request.args.get('product_name', '')
    return render_template('admin/ban_product.html', product_id=product_id, product_name=product_name)

@admin_bp.route('/admin/products/<int:product_id>/unban', methods=['POST'])
@login_required
@require_moderator_role.require(http_exception=403)
def unban_product(product_id):
    product = Product.query.get(product_id)

    if product:
        # Verifica si el producto está en la lista de productos prohibidos y lo elimina
        banned_product = BannedProducts.query.filter_by(product_id=product_id).first()

        if banned_product:
            banned_product.delete()
            current_app.logger.info(f'Producto {product_id} desprohibido por el administrador')
            return redirect(url_for('admin_bp.product_list'))
        else:
            return redirect(url_for('admin_bp.product_list'))
    else:
        return redirect(url_for('admin_bp.product_list'))