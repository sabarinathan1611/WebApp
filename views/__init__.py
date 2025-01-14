from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import json
from flask_migrate import Migrate



def config():
    with open('./config.json') as config_file:
        config = json.load(config_file)
        config_file.close
        return config
    
db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__,
                template_folder='../templates',
                static_folder='../static')
    app.config['SECRET_KEY'] = config().get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] =f"sqlite:///{DB_NAME}"

    app.config['UPLOAD_FOLDER'] = "static/images/"
    app.config['POST_FOLDER'] = "static/images/post/"
    

    app.config['RECAPTCHA_PUBLIC_KEY']=config().get('RECAPTCHA_PUBLIC_KEY')
    app.config['RECAPTCHA_PRIVATE_KEY'] =config().get('RECAPTCHA_PRIVATE_KEY')

    app.config['RECAPTCHA_PUBLIC_KEY']='recaptcha public key'
    app.config['RECAPTCHA_PRIVATE_KEY'] ='recaptcha private key'

    app.config['TESTING']=True
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Post

    create_database(app)
    # ckeditor = CKEditor(app)

    


    

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app




def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
        
