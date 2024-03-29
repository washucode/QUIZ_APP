from flask import Flask
from config import config_options
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_uploads import UploadSet, IMAGES, configure_uploads
app=Flask(__name__)
db = SQLAlchemy()
login_manager = LoginManager()
photos = UploadSet('photos',IMAGES)
def create_app(configname):
    '''
    methods runs the flask app

    Arg:
        config name thats the configuration option
    '''
    #import configurations
    app.config.from_object(config_options[configname])

    #import and initialise blueprint
    from .auth import auth as auth_blueprint
    from .main import main as main_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    #initialising the extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.session_protection = 'strong'
    configure_uploads(app,photos)

    return app
