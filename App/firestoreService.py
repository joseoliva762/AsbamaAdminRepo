import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import uuid

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

def putUser(userData):
    userRef = db.collection('users').document(userData.id)
    userRef.set({
        'username': userData.username,
        'password': userData.password,
        'correo': userData.correo,
        'nombre': userData.nombre,
        'role': userData.role
        })

def getNewId():
    return uuid.uuid1()

def updatePassword(user, password):
    userRef = db.collection('users').document(user.id)
    userRef.update({
        'password': password,
    })

def updateUserData(user, correo, nombre, role, username):
    userRef = db.collection('users').document(user.id)
    userRef.update({
        'correo': correo,
        'nombre': nombre,
        'role': role,
        'username': username
    })

def updateExternalUserData(user, role):
    userRef = db.collection('users').document(user.id)
    userRef.update({
        'role': role
    })