from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy() #define/initialize database
DB_NAME = "database.db" #dabatase name

def create_app():
    app = Flask(__name__) # initialize flask app
    app.config['SECRET_KEY'] = 'key' # ENCRYPT/secure session and cookie data -dont share in production
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' #tell flask were using db and where it is sqllite
    #sql alchemy db is stored here
    db.init_app(app) # initialize db by giving it the flask app


    #register blueprint
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    #Create database - loads and runs before initialization
    from .models import User, Note #defines classes

    create_database(app)

    #loading users
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app): #Check if database exist; if not, will create, will not override existing
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app) #which app we create db for
        print('Created Database!')
