from flask_login import UserMixin
from App.firestoreService import getUser, getUserById

class UserData():
    def __init__(self, username, password, id = '', correo = '', nombre= ''):
        self.username = username
        self.password = password
        self.id = id
        self.correo = correo
        self.nombre = nombre


class UserModel(UserMixin):
    def __init__(self, userData):
        self.username = userData.username
        self.password = userData.password
        self.id = userData.id
        self.correo = userData.correo
        self.nombre = userData.nombre

    @staticmethod
    def query(userId):
        userDoc = getUserById(userId)
        userData = UserData(
            username=userDoc.to_dict()['username'],
            password=userDoc.to_dict()['password'],
            id=userDoc.id,
            correo=userDoc.to_dict()['correo'],
            nombre=userDoc.to_dict()['nombre']
        )
        return UserModel(userData)