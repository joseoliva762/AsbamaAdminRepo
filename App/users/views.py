from . import users
from App.forms import LoginForm, SignupForm, ChangePassword, UpdateData, UpdateExternalData, DeleteUser, SearchUser
from flask_login import login_user, login_required, logout_user
from flask import render_template, redirect, url_for, flash, request, session, make_response
from App.firestoreService import getUsers, getUser, getNewId, getUserById, putUser, updatePassword, updateUserData, updateExternalUserData, deleteUserFromDb, deleteFromPhones,getPhoneByUserId, getCurrentRegister
from App.model import UserData, UserModel
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

@users.route('/all', methods=['GET',  'POST'])
@login_required
def userData():
    users =getUsers()
    userIp = session.get('userIp')
    search = SearchUser()
    if(search.is_submitted()):
        if(search.name.data != ''):
            users_ph = list()
            for user in users:
                if( (search.name.data).lower() in user.to_dict()['nombre'].lower()):
                    users_ph.append(user)
            users = users_ph
        # return redirect(url_for('users.userData'))
    context = {
        'userIp': userIp,
        'users': users,
        'search': search
    }
    print('\t\t\t', users)
    return render_template('userdata.html', **context)

@users.route('/<string:username>', methods=['GET'])
@login_required
def externalUserData(username=None):
    userIp = session.get('userIp')
    user = getUser(username)
    registros = getCurrentRegister(user.id)
    context = {
        'userIp': userIp,
        'user': user,
        'update': 2,
        'name': user.to_dict()['nombre'],
        'registros': registros
    }
    return render_template('externaluserdata.html', **context)

@users.route('/delete/<string:username>', methods=['GET',  'POST'])
@login_required
def deleteUser(username=None):
    userIp = session.get('userIp')
    user = getUser(username)
    delete = DeleteUser()
    context = {
        'userIp': userIp,
        'user': user,
        'update': 2,
        'delete': delete
    }
    if(delete.is_submitted()):
        user = getUser(username)
        currentPassword = delete.password.data
        if(check_password_hash(user.to_dict()['password'], currentPassword)):
            flash('El usuario {} fue borrado Exitosamente.'.format(username))
            phoneDb = getPhoneByUserId(user.id)
            deleteFromPhones(phoneDb.id)
            #print('>>>', phoneDb.to_dict()['telefono'])
            deleteUserFromDb(user.id)
            return redirect(url_for('home'))
        else:
            flash('la contraseña actual no coincide.', 'error')
    else:
        flash('Seguro que desea eliminar al usuario {}'.format(username))
    return render_template('deleteUser.html', **context)
    #return redirect(url_for('home'))
