from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, DecimalField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, NumberRange, InputRequired, Email
import decimal

class RegisterForm(FlaskForm):
    username = StringField('Nombre', validators=[DataRequired()])
    email = StringField('Correo Electrónico', validators=[Email(), DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Registrarse')


class LoginForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')


class ProductForm(FlaskForm):
    title = StringField(
        validators = [DataRequired()]
    )
    description = StringField(
        validators = [DataRequired()]
    )
    photo_file = FileField()
    price = DecimalField(
        places = 2, 
        rounding = decimal.ROUND_HALF_UP, 
        validators = [DataRequired(), NumberRange(min = 0)]
    )
    category_id = SelectField(
        validators = [InputRequired()]
    )
    submit = SubmitField()

# Formulari generic per esborrar i aprofitar la CSRF Protection
class DeleteForm(FlaskForm):
    submit = SubmitField()


class ResendVerificationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reenviar Enllaç de Verificació')

class EditProfileForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Actualitzar')