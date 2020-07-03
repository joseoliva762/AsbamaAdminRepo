from flask import request, make_response, redirect, render_template, session, url_for, flash
from flask_bootstrap import Bootstrap
from flask_login import login_required
from App.forms import LoginForm, RegisterAccess, UpdatePhoneRequired
from App.firestoreService import getUsers, getUserRegisters, getUser, getPhones, getPhonesByAdmin, getRegister, setRegister, getCurrentRegister, getUserById, getPhoneId, updateRequired
import unittest, random

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
    registros = getRegister()
    context = {
        'userIp': userIp,
        'registros': registros,
        'registroCode': 314,
        'background': chargeBackgruound()
    }
    return render_template('home.html', **context)

def chargeBackgruound():
    selector = round(random.random() * 5)
    return url_for('static', filename='images/background{}.jpg'.format(selector))

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
    updatePhones = UpdatePhoneRequired()
    updatePhones.submit.id = "updateForm"
    context = {
        'userIp': userIp,
        'phones': phonesByAdmins,
        'updatephones': updatePhones
    }
    return render_template('telefonos.html', **context)

@app.route('/users/undefined')
@login_required
def undefined():
    userIp = request.remote_addr
    response = make_response(redirect('/home'))
    session['userIp'] = userIp
    return response

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

@app.route('/telefonos/update/<string:telefono>/<int:required>', methods=['GET', 'POST'])
@login_required
def updatePhoneRequired(telefono=None, required=0):
    userIp = session.get('userIp')
    context = {
        'userIp': userIp,
        'registros': registros
    }
    phone = getPhoneId(telefono)
    updateRequired(phone.id, required)
    return redirect( url_for('telefonos') )

@app.route('/telefonos/update/config/<string:telefono>/<int:required>', methods=['GET', 'POST'])
@login_required
def updatePhoneRequiredFromConfig(telefono=None, required=0):
    userIp = session.get('userIp')
    context = {
        'userIp': userIp,
        'registros': registros
    }
    phone = getPhoneId(telefono)
    updateRequired(phone.id, required)
    return redirect( url_for('auth.configuration') )

@app.route('/evidence/<string:date>', methods=['GET', 'POST'])
@login_required
def getEvidence(date=None):
    userIp = session.get('userIp')
    path = getPath(date, 'h264')
    video = url_for('static', filename='{}'.format(path))
    # video = url_for('static', filename='demo.mp4')
    context = {
        'userIp': userIp,
        'background': chargeBackgruound(),
        'date': date,
        'path': path,
        'video': video
    }
    return render_template('evidence.html', **context)

def getPath( date, extension, root='Security/Evidencias/'):
   path = '{}\'{}\'/\'{}\'.{}'.format(
       root,
       date,
       date,
       extension
   )
   return path