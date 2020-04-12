from . import auth
from App.forms import LoginForm, SignupForm, ChangePassword, UpdateData, UpdateExternalData
from flask_login import login_user, login_required, logout_user
from flask import render_template, redirect, url_for, flash, request, session, make_response
from App.firestoreService import getUser, getNewId, getUserById, putUser, updatePassword, updateUserData, updateExternalUserData
from App.model import UserData, UserModel
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
#from App import loadUser


@auth.route('/login', methods=['GET', 'POST'])
def login():
    userIp = session.get('userIp')
    login = LoginForm()
    context =  {
        'userIp': userIp,
        'login': login
    }
    if ( login.is_submitted() ):
        username = login.username.data
        #session['username'] =  login.username.data#request.form.get('username')
        password = login.password.data
        userDoc = getUser(username)
        if userDoc is not None:
            passwordFromDb = userDoc.to_dict()['password']
            if check_password_hash(pwhash=passwordFromDb, password=password):
                userData = UserData(
                    username=username,
                    password=password,
                    id=userDoc.id,
                    correo=userDoc.to_dict()['correo'],
                    nombre=userDoc.to_dict()['nombre'],
                    role=userDoc.to_dict()['role']
                )
                user = UserModel(userData)
                login_user(user)
                flash('Usario: {}, Ah iniciado sesion con exito'.format(user.username.title()))
                session['username'] = username
                return redirect(url_for('home'))
            else:
                flash("Contraseña incorrecta, vuelva a intentarlo.", 'error')
        else:
            flash("El usuario {}, No has sido encontrado.".format(username), 'error')
    return render_template('login.html', **context)



@auth.route('/signup', methods=['GET', 'POST'])
@login_required
def signup():
    userIp = session.get('userIp')
    signup = SignupForm()
    context =  {
        'userIp': userIp,
        'signup': signup
    }
    if ( signup.is_submitted() ):
        correo = signup.correo.data
        nombre = signup.nombre.data
        role = signup.role.data
        username = signup.username.data
        password = signup.password.data
        id = str(getNewId())
        if (getUser(username) is None):
            passwordHash = generate_password_hash(password)
            userData = UserData(username, passwordHash, id, correo, nombre, role)
            putUser(userData)
            user = UserModel(userData)
            if(getUser(user.username) is not None):
                flash('Usuario Creado con Exito!!')
            else:
                flash('Creacion de usuario Fallida', 'error')
        else:
            flash('El Usuario Ya Existe!!', 'error')
        return redirect(url_for('home'))
    else:
        flash('Registra un Usuario.')
    return render_template('signup.html', **context)


@auth.route('/changepassword', methods=['GET', 'POST'])
@login_required
def changePassword():
    flash('Actualizar Contraseña.')
    userIp = session.get('userIp')
    username = session.get('username')
    changePassword = ChangePassword()
    context =  {
        'userIp': userIp,
        'changepassword': changePassword
    }
    if(changePassword.is_submitted()):
        currentPassword = changePassword.currentPassword.data
        password = changePassword.password.data
        confirmPassword = changePassword.confirmPassword.data
        user = getUser(username)
        print(user.id)
        if(check_password_hash(user.to_dict()['password'], currentPassword)):
            if(password == confirmPassword):
                if(currentPassword != password):
                    updatePassword(user, generate_password_hash(password))
                    if(check_password_hash(getUser(username).to_dict()['password'], password)):
                        flash('Contraseña Actualizada con Exito!!')
                        return redirect(url_for('home'))
                    else:
                        flash('Ah ocurrido un error al actualizar la contraseña, por favor intente nuevamente.', 'error')
                else:
                    flash('No puede registrar la misma contraseña.', 'error')
            else:
                flash('La nueva contraseña, no coincide.','error')
        else:
            flash('la contraseña actual no coincide.', 'error')
    return render_template('changepassword.html', **context)

@auth.route('/updatedata', methods=['GET', 'POST'])
@login_required
def updateData():
    userIp = session.get('userIp')
    username = session.get('username')
    flash('Actualizar Informacion de {}.'.format(username.title()))
    updateData = UpdateData()
    context =  {
        'userIp': userIp,
        'updatedata': updateData
    }
    if(updateData.is_submitted()):
        user = getUser(username)
        password = updateData.password.data
        if(check_password_hash(user.to_dict()['password'], password)):
            correo = validarData(updateData.correo.data, user.to_dict()['correo'])
            nombre = validarData(updateData.nombre.data, user.to_dict()['nombre'])
            role = validarData(updateData.role.data, user.to_dict()['role'])
            newUsername = validarData(updateData.username.data, user.to_dict()['username'])
            updateUserData(user, correo,nombre,role,newUsername)
            flash('Actualizacion realizada con Exito.')
            return redirect(url_for('account'))
        else:
            flash('Contraseña Invalida.', 'error')

    return render_template('updatedata.html', **context)

def validarData(passData, CurrentData):
    if(passData == ''):
        return CurrentData
    return passData

@auth.route('/updateexternaldata/<string:username>', methods=['GET', 'POST'])
@login_required
def updateExternalData(username=None):
    userIp = session.get('userIp')
    flash('Actualizar Informacion de {}.'.format(username.title()))
    updateExternalData = UpdateExternalData()
    context =  {
        'userIp': userIp,
        'updateexternaldata': updateExternalData,
        'username': username
    }
    if(updateExternalData.is_submitted()):
        user = getUser(username)
        password = updateExternalData.password.data
        if(check_password_hash(user.to_dict()['password'], password)):
            role = validarData(updateExternalData.role.data, user.to_dict()['role'])
            updateExternalUserData(user, role)
            flash('Actualizacion realizada con Exito.')
            return redirect(url_for('userData'))
        else:
            flash('Contraseña Invalida.', 'error')
    return render_template('updateexternaldata.html', **context)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Sesion Cerrada.")
    return redirect( url_for('auth.login'))

# https://meet.jit.si/RevisionInterfazAdministrativa