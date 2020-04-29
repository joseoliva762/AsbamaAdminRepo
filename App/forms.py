from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    submit = SubmitField('Login')

class SearchUser(FlaskForm):
    name = StringField('Nombre: ', render_kw={"placeholder": "Nombre.."}) #, placeholder="Nombre...")
    submit = SubmitField('Buscar')

class RegisterAccess(FlaskForm):
    descripcion = StringField('Descripcion: ', validators=[DataRequired()])
    submit = SubmitField('Registrar')

class SignupForm(FlaskForm):
    imagen = StringField('Imagen URL: ')
    telefono = StringField('Telefono: ', validators=[DataRequired()])
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

class UpdateData(FlaskForm):
    imagen = StringField('Imagen URL: ')
    telefono = StringField('Telefono: ')
    correo = StringField('Correo: ')
    nombre = StringField('Nombre: ')
    role = StringField('Rol: ')
    username = StringField('Username: ')
    password = PasswordField('Confirmar Password: ', validators=[DataRequired()])
    submit = SubmitField('Actualizar')

class UpdateExternalData(FlaskForm):
    imagen = StringField('Imagen URL: ')
    telefono = StringField('Telefono: ')
    correo = StringField('Correo: ')
    nombre = StringField('Nombre: ')
    role = StringField('Rol: ', validators=[DataRequired()])
    username = StringField('Username: ')
    password = PasswordField('Confirmar Password: ', validators=[DataRequired()])
    submit = SubmitField('Actualizar')

class DeleteUser(FlaskForm):
    password = PasswordField('Confirmar Password: ', validators=[DataRequired()])
    submit = SubmitField('Eliminar')

class UpdatePhoneRequired(FlaskForm):
    submit = SubmitField('Update')