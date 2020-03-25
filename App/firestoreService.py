import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

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
