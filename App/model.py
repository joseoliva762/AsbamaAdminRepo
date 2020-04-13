from flask_login import UserMixin
from App.firestoreService import getUserById

class UserData():
    def __init__(self, username, password, id = '', correo = '', nombre= '', role='', imagen='', telefono='', access='', fechadeactualizacion=''):
        self.username = username
        self.password = password
        self.id = id
        self.correo = correo
        self.nombre = nombre
        self.role = role
        self.imagen = imagen
        self.telefono = telefono
        self.access = access
        self.fechadeactualizacion=fechadeactualizacion


class UserModel(UserMixin):
    def __init__(self, userData):
        self.username = userData.username
        self.password = userData.password
        self.id = userData.id
        self.correo = userData.correo
        self.nombre = userData.nombre
        self.role = userData.role
        self.imagen = userData.imagen
        self.telefono = userData.telefono
        self.access = userData.access
        self.fechadeactualizacion=userData.fechadeactualizacion

    @staticmethod
    def query(userId):
        userDoc = getUserById(userId)
        userData = UserData(
            username=userDoc.to_dict()['username'],
            password=userDoc.to_dict()['password'],
            id=userDoc.id,
            correo=userDoc.to_dict()['correo'],
            nombre=userDoc.to_dict()['nombre'],
            role=userDoc.to_dict()['role'],
            access=userDoc.to_dict()['access'],
            imagen=userDoc.to_dict()['imagen'],
            telefono=userDoc.to_dict()['telefono'],
            fechadeactualizacion=userDoc.to_dict()['fechadeactualizacion']
        )
        return UserModel(userData)
