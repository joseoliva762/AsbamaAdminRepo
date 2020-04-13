from . import users
from App.forms import LoginForm, SignupForm, ChangePassword, UpdateData, UpdateExternalData
from flask_login import login_user, login_required, logout_user
from flask import render_template, redirect, url_for, flash, request, session, make_response
from App.firestoreService import getUsers, getUser, getNewId, getUserById, putUser, updatePassword, updateUserData, updateExternalUserData
from App.model import UserData, UserModel
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

@users.route('/all')
@login_required
def userData():
    users =getUsers()
    userIp = session.get('userIp')
    context = {
        'userIp': userIp,
        'users': users
    }
    return render_template('userdata.html', **context)

@users.route('/<string:username>', methods=['GET'])
@login_required
def externalUserData(username=None):
    userIp = session.get('userIp')
    user = getUser(username)
    context = {
        'userIp': userIp,
        'user': user,
        'update': 2
    }
    return render_template('externaluserdata.html', **context)
