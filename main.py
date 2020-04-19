from flask import request, make_response, redirect, render_template, session, url_for, flash
from flask_bootstrap import Bootstrap
from flask_login import login_required
from App.forms import LoginForm, RegisterAccess
from App.firestoreService import getUsers, getUserRegisters, getUser, getPhones, getPhonesByAdmin, getRegister, setRegister, getCurrentRegister, getUserById
import unittest

from App import createApp

app = createApp()

users = ['Comprar cafe', 'Enviar solicitud de compra', 'Entregar video a productor ']

@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.errorhandler(404)
def notFound(error):
    context = {
        "error": error,
        "number": "404",
        "title": "Not Found",
        "msg": "Lo Siento No Encontramos Lo Que Buscabas."
    }
    return render_template('error.html', **context)

@app.errorhandler(500)
def internalError(error):
    context = {
        "error": error,
        "number": "500",
        "title": "Internal Server Error",
        "msg": "Lo Siento Ocurrio un problema en el Servidor, Intenta más Tarde."
    }
    return render_template('error.html', **context)

@app.route('/')
def index():
    userIp = request.remote_addr
    response = make_response(redirect('/auth/login'))
    session['userIp'] = userIp
    return response


@app.route('/home', methods=['GET'])
@login_required
def home():
    userIp = session.get('userIp')
    #username = current_user.to_dict().username
    # username = session.get('username')
    #response = make_response(redirect('/home'))
    print('Llegoooo aquiiiiii......')
    registros = getRegister()
    context = {
        'userIp': userIp,
        'registros': registros,
        'registroCode': 314
    }
    return render_template('home.html', **context)

@app.route('/account', methods=['GET'])
@login_required
def account():
    userIp = session.get('userIp')
    user = getUser(str(session.get('username')))
    registros = getCurrentRegister(user.id)
    context = {
        'userIp': userIp,
        'update': 1,
        'registros': registros
    }
    return render_template('account.html', **context)

@app.route('/telefonos')
@login_required
def telefonos():
    userIp = session.get('userIp')
    telefonos = getPhones()
    phonesByAdmins = getPhonesByAdmin(telefonos)
    context = {
        'userIp': userIp,
        'phones': phonesByAdmins
    }
    return render_template('telefonos.html', **context)


@app.route('/registros', methods=['GET', 'POST'])
@login_required
def registros():
    userIp = session.get('userIp')
    registros = RegisterAccess()
    context = {
        'userIp': userIp,
        'registros': registros
    }
    if( registros.is_submitted() ):
        descripcion = registros.descripcion.data
        username = session.get('username')
        user = getUser(username)
        flash(' Registro del usuario {} creado exitosamente!'.format(username))
        setRegister(user.id, descripcion)

        return redirect(url_for('home'))
    return render_template('registros.html', **context)

