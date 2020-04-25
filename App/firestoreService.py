import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import uuid
from datetime import datetime
# from App.model import PhoneModel

class PhoneModel():
    def __init__(self, user,telefono, role, update):
        self.user = user
        self.telefono = telefono
        self.role = role
        self.update = update

class RegitrosModel():
    def __init__(self, user, telefono, fecha, descripcion):
        self.user = user
        self.telefono = telefono
        self. fecha = fecha
        self.descripcion = descripcion


if (not len(firebase_admin._apps)):
    credential = credentials.ApplicationDefault()
    firebase_admin.initialize_app(credential, {
        'projectId': 'asbama314',
    })

db= firestore.client()

def getUsers():
    return db.collection('users').get()

def getUserRegisters(userId):
    return db.collection('users').document(userId).collection('registers').get()

def getUser(username):
    users = db.collection('users').where('username', '==', username).get()
    for user in users:
        return user

def getUserById(userId):
    return db.collection('users').document(userId).get()

def deleteUserFromDb(userId):
    userRef = db.collection('users').document(userId)
    userRef.delete()

def getPhoneByUserId(userId):
    phones = db.collection('telefonos').where('user', '==', userId).get()
    for phone in phones:
        return phone

def deleteFromPhones(phoneId):
    phoneRef = db.collection('telefonos').document(str(phoneId))
    phoneRef.delete()

def putUser(userData):
    userRef = db.collection('users').document(userData.id)
    userRef.set({
        'username': userData.username,
        'password': userData.password,
        'correo': userData.correo,
        'nombre': userData.nombre,
        'role': userData.role,
        'imagen': userData.imagen,
        'telefono': userData.telefono,
        'access': 'undefined',
        'fechadecreacion': datetime.now(),
        'fechadeactualizacion': datetime.now(),
        'status': True
        })
    telefonosRef = db.collection('telefonos').document(str(getNewId()))
    telefonosRef.set({
        'telefono': userData.telefono,
        'user': userData.id,
        'fechadeactualizacion': datetime.now()
    })

def getNewId():
    return uuid.uuid1()

def updatePassword(user, password):
    userRef = db.collection('users').document(user.id)
    userRef.update({
        'password': password,
    })

def updateUserData(user, correo, nombre, role, username, imagen, telefono, lastPhone ):
    userRef = db.collection('users').document(user.id)
    userRef.update({
        'correo': correo,
        'nombre': nombre,
        'role': role,
        'username': username,
        'telefono': telefono,
        'imagen': imagen,
        'fechadeactualizacion': datetime.now()
    })
    if(telefono != lastPhone):
        phoneRef = db.collection('telefonos').document(str(updatePhonesByUserId(user.id).id))
        phoneRef.update({
            'telefono': telefono
        })
def updateExternalUserData(user, role):
    userRef = db.collection('users').document(user.id)
    userRef.update({
        'role': role
    })

def updatePhonesByUserId(userId):
    telefonos = db.collection('telefonos').where('user', '==', userId).get()
    for telefono in telefonos:
        return telefono

def getPhones():
    return db.collection('telefonos').get()

def getPhonesByAdmin(phones):
    phoneTemplateData = list()
    for phone in phones:
        user = getUserById(phone.to_dict()['user'])
        model = PhoneModel(user, phone.to_dict()['telefono'], user.to_dict()['role'], phone.to_dict()['fechadeactualizacion'])
        phoneTemplateData.append(model) 
    return phoneTemplateData

def setCurrentRegister(registerId, userId, fechadecreacion, descripcion):
    accessRef = db.collection('users').document(str(userId)).collection('registers').document(registerId)
    accessRef.set({
        'descripcion': descripcion,
        'user': userId,
        'fechadecreacion': fechadecreacion
    })

def getCurrentRegister(userId):
    registros = db.collection('users').document(userId).collection('registers').get()
    registerTemplateData = list()
    for registro in registros:
        user = getUserById(str(registro.to_dict()['user']))
        model = RegitrosModel(user.to_dict()['username'], user.to_dict()['telefono'], registro.to_dict()['fechadecreacion'], registro.to_dict()['descripcion'])
        registerTemplateData.append(model) 
    return registerTemplateData


def setRegister(userId,descripcion):
    registerId = str(getNewId())
    accessRef = db.collection('register').document(registerId)
    fechadecreacion = datetime.now()
    accessRef.set({
        'descripcion': descripcion,
        'user': userId,
        'fechadecreacion': fechadecreacion
    })
    setCurrentRegister(registerId, userId, fechadecreacion, descripcion)

def getRegister():
    registros = db.collection('register').get()
    registerTemplateData = list()
    for registro in registros:
        user = getUserById(str(registro.to_dict()['user']))
        model = RegitrosModel(user.to_dict()['username'], user.to_dict()['telefono'], registro.to_dict()['fechadecreacion'], registro.to_dict()['descripcion'])
        registerTemplateData.append(model) 
    return registerTemplateData

def deleteRegister(userId):
    registersQuery = db.collection('register').where('user', '==', userId).get()
    for registerQuery in registersQuery:
        registerRef = db.collection('register').document(str(registerQuery.id))
        registerRef.delete()
        registerRef = db.collection('users').document(userId).collection('registers').document(registerQuery.id)
        registerRef.delete()