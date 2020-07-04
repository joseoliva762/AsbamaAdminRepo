import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import uuid
from datetime import datetime

class PhoneModel():
    def __init__(self, user,telefono, role, update, required):
        self.user = user
        self.telefono = telefono
        self.role = role
        self.update = update
        self.required = required

class Service:
    def __init__(self):
        if (not len(firebase_admin._apps)):
            credential = credentials.ApplicationDefault()
            firebase_admin.initialize_app(credential, {
                'projectId': 'asbama314',
            })
        self.db = firestore.client()

    def getConfiguration(self):
        return self.db.collection('configuracion').document('configuraciongeneral').get()

    def wiegandIdValidate(self, rfid):
        users = self.db.collection('users').where('access', '==', str(rfid)).get()
        users = [ user for user in users ]
        validate = True if (len(users) > 0) and (len(users) == 1) else False
        if( validate ):
            for user in users:
                return validate, user
        else:
            return validate, 'undefined'

    def createRegister(self, description, userId, date ):
        registerId = self.getNewId()
        accessRef = self.db.collection('users').document(userId).collection('registers').document(str(registerId))
        information = {
            'descripcion': description,
            'user': userId,
            'fechadecreacion': date
        }
        accessRef.set(information)
        accessGlobalRef = self.db.collection('register').document(str(registerId))
        accessGlobalRef.set(information)

    def undefinedRegister(self, description, undefinedId, date):
        registerId = self.getNewId()
        accessGlobalRef = self.db.collection('register').document(str(registerId))
        accessGlobalRef.set({
            'descripcion': description,
            'user': undefinedId,
            'fechadecreacion': date
        })

    def getUserById(self, userId):
        return self.db.collection('users').document(userId).get()

    def getPhones( self ):
        phones = self.db.collection('telefonos').get()
        phoneTemplateData = list()
        for phone in phones:
            user = self.getUserById(phone.to_dict()['user'])
            model = PhoneModel(user, phone.to_dict()['telefono'], user.to_dict()['role'], phone.to_dict()['fechadeactualizacion'], phone.to_dict()['requerido'])
            phoneTemplateData.append(model)
        return phoneTemplateData

    def getNewId(self):
        return uuid.uuid1()