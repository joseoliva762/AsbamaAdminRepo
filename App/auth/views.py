from . import auth
from App.forms import ChangePassword, LoginForm, SignupForm, UpdateData, UpdateExternalData, UpdatePhoneRequired, UpdateConfiguration, UpdateStateSystem
from flask_login import login_user, login_required, logout_user
from flask import render_template, redirect, url_for, flash, request, session, make_response
from App.firestoreService import getUser, getNewId, getUserById, putUser, updatePassword, updateUserData, updateExternalUserData
from App.firestoreService import getConfigurationInfo, getPhoneRequiredCallback, getPhones, getPhonesByAdmin, updateConfigInfoDB
from App.firestoreService import setStateSystem
from App.model import UserData, UserModel
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import random
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
        username = (login.username.data).lower()
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
                    role=userDoc.to_dict()['role'],
                    imagen=userDoc.to_dict()['imagen'],
                    telefono=userDoc.to_dict()['telefono'],
                    access=userDoc.to_dict()['access'],
                    fechadeactualizacion=userDoc.to_dict()['fechadeactualizacion']
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
        imagen = imageValidator(signup.imagen.data)
        telefono = signup.telefono.data
        correo = signup.correo.data
        nombre = signup.nombre.data
        role = signup.role.data
        username = signup.username.data
        password = signup.password.data
        id = str(getNewId())
        if (getUser(username) is None):
            passwordHash = generate_password_hash(password)
            userData = UserData(username, passwordHash, id, correo, nombre, role, imagen, telefono)
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

def imageValidator(imgUrl):
    return imgUrl if imgUrl != '' else url_for('static', filename='images/profile.jpg')

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
            imagen = validarData(updateData.imagen.data, user.to_dict()['imagen'])
            telefono = validarData(updateData.telefono.data, user.to_dict()['telefono'])
            updateUserData(user, correo,nombre,role,newUsername, imagen, telefono, user.to_dict()['telefono'])
            flash('Actualizacion realizada con Exito.')
            return redirect(url_for('account'))
        else:
            flash('Contraseña Invalida.', 'error')
    else:
        flash('Actualizar Informacion de {}.'.format(username.title()))


    return render_template('updatedata.html', **context)

def validarData(passData, CurrentData):
    if(passData == ''):
        return CurrentData
    return passData

@auth.route('/updateexternaldata/<string:username>', methods=['GET', 'POST'])
@login_required
def updateExternalData(username=None):
    userIp = session.get('userIp')
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
            return redirect(url_for('users.userData'))
        else:
            flash('Contraseña Invalida.', 'error')
    else:
        flash('Actualizar Informacion de {}.'.format(username.title()))
    return render_template('updateexternaldata.html', **context)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Sesion Cerrada.")
    return redirect( url_for('auth.login'))

@auth.route('/configuracion', methods=['GET', 'POST'])
@login_required
def configuration():
    userIp = session.get('userIp')
    configuracion = getConfigurationInfo()
    telefonos = getPhones()
    phonesByAdmins = getPhoneRequiredCallback(telefonos)
    updatePhones = UpdatePhoneRequired()
    updatePhones.submit.id = "updateForm"
    stateSytem = UpdateStateSystem()
    stateSytem.submit.id = "updateForm"

    context =  {
        'userIp': userIp,
        'configuracion': configuracion,
        'phones': phonesByAdmins,
        'updatephones': updatePhones,
        'background': chargeBackgruound(),
        'statesystem': stateSytem
    }
    return render_template('configuracion.html', **context)

def chargeBackgruound():
    selector = round(random.random() * 5)
    return url_for('static', filename='images/background{}.jpg'.format(selector))

@auth.route('/configuracion/update', methods=['GET', 'POST'])
@login_required
def configurationUpdate():
    userIp = session.get('userIp')
    configuracion = getConfigurationInfo()
    telefonos = getPhones()
    phonesByAdmins = getPhoneRequiredCallback(telefonos)
    updatePhones = UpdatePhoneRequired()
    updatePhones.submit.id = "updateForm"
    configuracionUpdate = UpdateConfiguration()
    configuracionUpdate.resolucioncamara.render_kw['placeholder'] = configuracion.to_dict()['resolucioncamara']
    configuracionUpdate.resolucioncamara.id = 'update__data'
    configuracionUpdate.tiempodeespera.render_kw['placeholder'] = configuracion.to_dict()['tiempodeespera']
    configuracionUpdate.tiempodeespera.id = 'update__data'
    configuracionUpdate.submit.id = 'boton__actualizar'
    context =  {
        'userIp': userIp,
        'configuracion': configuracion,
        'phones': phonesByAdmins,
        'updatephones': updatePhones,
        'background': chargeBackgruound(),
        'configuracionUpdate': configuracionUpdate
    }
    if(configuracionUpdate.is_submitted()):
        resolucion = validarData(configuracionUpdate.resolucioncamara.data, configuracionUpdate.resolucioncamara.render_kw['placeholder']) 
        espera = validarData(configuracionUpdate.tiempodeespera.data, configuracionUpdate.tiempodeespera.render_kw['placeholder']) 
        updateConfigInfoDB(resolucion, espera)
        flash('Actualizacion de la configuracion realizada con exito.')
        return redirect(url_for('auth.configuration'))

    return render_template('configuracionupdate.html', **context)

# https://meet.jit.si/RevisionInterfazAdministrativa

@auth.route('/configuracion/update/statesystem/<int:required>', methods=['GET', 'POST'])
@login_required
def configurationUpdateStateSytem(required=0):
    userIp = session.get('userIp')
    context = {
        'userIp': userIp,
    }
    setStateSystem(required)
    return redirect( url_for('auth.configuration') )