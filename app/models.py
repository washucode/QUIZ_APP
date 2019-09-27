from . import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    '''
    This is a class that contains the database schema for users
    '''
    __tablename__= 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(255),unique=True,nullable=False)
    email = db.Column(db.String(255),unique=True,nullable=False)
    password_hash = db.Column(db.String,nullable=False)
    profile_photo = db.Column(db.String, nullable = True)
    bio = db.Column(db.Text,nullable = True)
    game = db.relationship('Game',backref='user',lazy='dynamic')


    def generate_password(self,password):
        '''
        Generates password hash
        '''
        password_gen = generate_password_hash(password)
        self.password_hash = password_gen

    def verify_password(self,password):
        '''
        confirms password equal to the password hash during login
        '''
        check_password_hash(self.password_hash,password)


class Player(db.Model):
    '''
    This class will create the database schema for players
    '''
    __tablename__='players'
    id = db.Column(db.Integer,primary_key=True)
    game_id = db.Column(db.Integer,db.ForeignKey('games.id'))
    player_name = db.Column(db.String,nullable=False)
    results = db.Column(db.Integer)

class Game(db.Model):
    '''
    This is a class that contains the database schema for the game
    '''
    __tablename__='games'
    id = db.Column(db.Integer,primary_key=True)
    gamename = db.Column(db.String(255),nullable=False,unique=True)
    description = db.Column(db.String)
    award = db.Column(db.String)
    status = db.Column(db.Boolean)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    game_password = db.Column(db.String,nullable=False)
    questions = db.relationship('Question',backref='game',lazy='dynamic')

    player = db.relationship('Player',backref='game',lazy='dynamic')


class Question(db.Model):
    '''
    This class will create the database schema for the questions
    '''
    __tablename__='questions'
    id = db.Column(db.Integer,primary_key=True)
    question = db.Column(db.Text,nullable=False)
    game_id = db.Column(db.Integer,db.ForeignKey('games.id'))
    choices = db.relationship('Choices',backref='question',lazy='dynamic')

class Choices(db.Model):
    '''
    This class will create the database schema for the choices
    '''
    __tablename__='choices'
    id = db.Column(db.Integer,primary_key=True)
    question_id = db.Column(db.Integer,db.ForeignKey('questions.id'))
    choice = db.Column(db.String,nullable=False)
    status = db.Column(db.Boolean)
    points = db.Column(db.Integer)
