from flask import Blueprint, redirect, render_template, url_for, flash, request
from .forms import RegisterForm, LoginForm, ResendVerificationForm
from flask_login import login_user, current_user, logout_user, login_required
from . import login_manager
from .models import User, BlockedUser
from . import db_manager as db
from werkzeug.security import generate_password_hash, check_password_hash
from .security import notify_identity_changed
import secrets
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

auth_bp = Blueprint(
    "auth_bp", __name__, template_folder="templates", static_folder="static"
)

@auth_bp.route('/profile')
@login_required
def profile():
    user = current_user
    blocked = BlockedUser.query.filter_by(user_id=user.id).first()
    return render_template('auth/profile.html', user=user, blocked=blocked)

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
            if user.verified:
                login_user(user)
                notify_identity_changed()
                next_page = request.args.get('next')
                return redirect(next_page or url_for('main_bp.product_list'))
            else:
                flash('Please verify your email address', 'warning')
                return redirect(url_for('main_bp.init'))  
        else:
            flash('Login fallit. Si us plau, comprova el teu email i contrasenya', 'danger')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def auth_register():
    form = RegisterForm()
    token = secrets.token_urlsafe(20)
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(name=form.username.data, email=form.email.data, password=hashed_password, role='wanner', email_token=token, verified = 0)
        
        db.session.add(new_user)
        db.session.commit()

        send_verification_email(new_user.email, new_user.name, token)
        flash('Registre completat amb èxit. Ara pots iniciar sessió.', 'success')
        return redirect(url_for('auth_bp.auth_login'))  # Redirigeix a la pàgina de login
    #return redirect(url_for('main_bp.product_list'))
    return render_template('auth/register.html', form = form)

@auth_bp.route('/logout')
def auth_logout():
    logout_user()
    flash('Sessió tancada correctament', 'success')
    return redirect(url_for('auth_bp.auth_login')) 

def send_verification_email(user_email, username, token):
    # Configuració del servidor SMTP (exemple amb Gmail)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "2daw.equip11@fp.insjoaquimmir.cat"  
    smtp_password = "t4CxjcNws3iwanZ3"  

    # Crear el missatge
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = user_email
    msg['Subject'] = "Verifica el teu correu electrònic"

    # Cos del missatge
    body = f"Hola {username},\n\nBenvingut/da! Si us plau, verifica el teu correu electrònic clicant en aquest enllaç:\n"
    body += f"http://127.0.0.1:5000/verify/{username}/{token}"  
    msg.attach(MIMEText(body, 'plain'))

    # Enviar el correu
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)
    server.send_message(msg)
    server.quit()

@auth_bp.route('/verify/<name>/<email_token>')
def verify_email(name, email_token):
    # Busca l'usuari a la base de dades
    user = User.query.filter_by(name=name, email_token=email_token).first()

    if user and not user.verified:
        user.verified = True
        db.session.commit()
        flash('Your email has been verified!', 'success')
        return redirect(url_for('auth_bp.auth_login'))
    else:
        flash('Invalid or expired verification link', 'danger')
        return redirect(url_for('main_bp.init'))



@auth_bp.route('/resend', methods=['GET', 'POST'])
def resend_verification():
    form = ResendVerificationForm()
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()

        if user and not user.verified:
            # Generar un nou token
            new_token = secrets.token_urlsafe(20)
            user.email_token = new_token
            db.session.commit()

            # Enviar correu
            sender_email = "2daw.equip11@fp.insjoaquimmir.cat"
            receiver_email = user.email
            password = "t4CxjcNws3iwanZ3"

            message = MIMEText(f"Per verificar el teu compte, si us plau, segueix aquest enllaç: {url_for('auth_bp.verify_email', name=user.name, email_token=new_token, _external=True)}")
            message['Subject'] = "Verificació de Correu"
            message['From'] = sender_email
            message['To'] = receiver_email

            # Enviar el correu
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())

            flash('Un nou correu de verificació ha estat enviat.', 'success')
        else:
            flash('No s\'ha trobat cap usuari amb aquest correu o ja està verificat.', 'error')

        return redirect(url_for('auth_bp.resend_verification'))

    return render_template('auth/resend_verification.html', form=form)

