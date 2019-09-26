from . import main
from flask import render_template

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/game')
def game():    
    return render_template('game.html')

@main.route('/questions')
def question():
    return render_template('questions.html')
