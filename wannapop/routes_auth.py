from flask import Blueprint, redirect, render_template, url_for, flash, request
from .forms import RegisterForm, LoginForm
from flask_login import login_user, current_user, logout_user
from . import login_manager
from .models import User
from .forms import LoginForm
from . import db_manager as db
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint(
    "auth_bp", __name__, template_folder="templates", static_folder="static"
)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route('/login', methods=['GET', 'POST'])
def auth_login():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.product_list'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main_bp.product_list'))  
        else:
            flash('Login fallit. Si us plau, comprova el teu email i contrasenya', 'danger')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def auth_register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(name=form.username.data, email=form.email.data, password=hashed_password, role='wanner')
        
        db.session.add(new_user)
        db.session.commit()

        flash('Registre completat amb èxit. Ara pots iniciar sessió.', 'success')
        return redirect(url_for('auth_bp.auth_login'))  # Redirigeix a la pàgina de login
    #return redirect(url_for('main_bp.product_list'))
    return render_template('auth/register.html', form = form)

@auth_bp.route('/logout')
def auth_logout():
    logout_user()
    flash('Sessió tancada correctament', 'success')
    return redirect(url_for('auth_bp.auth_login')) 

