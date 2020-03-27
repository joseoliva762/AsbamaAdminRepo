from . import auth
from App.forms import LoginForm
from flask_login import login_user, login_required, logout_user
from flask import render_template, redirect, url_for, flash, request, session, make_response
from App.firestoreService import getUser
from App.model import UserData, UserModel
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
            if password == passwordFromDb:
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
                return redirect(url_for('home'))
            else:
                flash("Contraseña incorrecta, vuelva a intentarlo.")
        else:
            flash("El usuario {}, No has sido encontrado.".format(username))
    return render_template('login.html', **context)

@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash("Sesion Cerrada.")
    return redirect( url_for('auth.login'))