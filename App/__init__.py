from flask import Flask
from flask_bootstrap import Bootstrap
from .config import Config
from .auth import auth
from flask_login import  LoginManager
from .model import UserModel

loginManager = LoginManager()
loginManager.login_view = 'auth.login'


@loginManager.user_loader
def loadUser(userId):
    return UserModel.query(userId=userId)

def createApp():
    app = Flask(__name__)
    bootstrap = Bootstrap(app)
    app.config.from_object(Config)
    loginManager.init_app(app)
    app.register_blueprint(auth)
    return app