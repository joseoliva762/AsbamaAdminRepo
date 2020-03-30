from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    correo = StringField('Correo: ', validators=[DataRequired()])
    nombre = StringField('Nombre: ', validators=[DataRequired()])
    role = StringField('Rol: ', validators=[DataRequired()])
    username = StringField('Username: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    submit = SubmitField('Resgitrar')

class ChangePassword(FlaskForm):
    currentPassword = PasswordField('Actual: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    confirmPassword = PasswordField('confirmar: ', validators=[DataRequired()])
    submit = SubmitField('Cambiar')