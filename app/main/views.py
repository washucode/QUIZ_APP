from . import main
from flask import render_template,request,redirect,url_for,flash,abort,jsonify
from ..models import User,Player,Game,Question,Choices
from .. import db
from flask_login import login_required,current_user

@main.route('/',methods=['GET','POST'])
def index():
    if request.method == 'post':
        player_name = request.form.get('player_name')
        player = Player(player_name=player_name)
        db.session.add(player)
        db.session.commit()
        current_player = Player.query.filter_by(player_name=player_name).first()
        game_code = request.form.get('game_code')
        game = Game.query.filter_by(game_password=game_code).first()
        if game is not None:
            return redirect(url_for('.game',game_id=game.id,player_id=current_player.id))
        else:
            flash('That game does not exist')
            return render_template('index.html')
    return render_template('index.html')

@main.route('/game/<int:game_id>/<int:player_id>',methods=['GET','POST'])
def game(game_id,player_id):
    '''
    This method will query the database table games and render the game selected by the user

    Arg:
        game_id will allow query the database table games and query by id
    '''

    current_game = Game.query.get(game_id)
    player_id = player_id
    return render_template('game.html',current_game = current_game,player_id=player_id)

@main.route('/questions/<int:game_id>/<int:player_id>',methods=['GET','POST'])
def do_questions(game_id,player_id):
    '''
    This method will allow the player to view and answer the questions in the game

    Arg:
        the game id to allow it to query the table questions and query the questions related to the game
        player_id to allow capture of results and link them to the player
    '''

    player = Player.query.filter_by(id = player_id).first()
    # players = Player.query.
    questions = Question.query.filter_by(game_id = game_id).all()
    for question in questions:
        choices = Choice.query.filter_by(question_id = question).all()
    if request.method == 'post':
        counter = 0
        choice_answers = request.form.getlist('choices')
        for choice in choice_answers:
            if choice == True:
                counter += 1
                results = counter
            player.results = results
            db.session.commit()

    return render_template('doquestions.html',questions = questions,choices=choices,player=player)

@main.route('/creategame/<int:user_id>',methods=['GET','POST'])
@login_required
def create_game(user_id):
    '''
    This method takes in game data from the user and stores it in the database
    Arg:
        user_id in order to assighn the question the foreign key to the user who created it
    '''

    if request.method == 'post':
        gamename = request.form.get('gamename')
        description = request.form.get('description')
        award = request.form.get('award')
        status = request.form.get('status')
        game_password = request.form.get('game_password')

        new_game = Game(gamename=gamename,description=description,award=award,status=status,game_password=game_password,user_id=current_user)
        db.session.add(new_game)
        db.session.commit()
        game_id = Game.query.filter_by(gamename=gamename).first()
        return redirect(url_for('.add_questions',game_id=game_id.id))

    return render_template('create.html')

@main.route('/profile/<username>', methods = ['POST','GET'])
@login_required
def profile(username):
    '''
    This method displays user information and user games
    Arg:
        username in order to query the user by username in the db
    '''
    if current_user.username == username:
        user = User.query.filter_by(username=username).first()
        games = Game.query.filter_by(user_id=user.id).all()
        return render_template ( 'profile.html',user=user,games=games)
    else:
        abort(404)


@main.route('/questions/<int:game_id>',methods=['POST','GET'])
def add_questions(game_id):
    '''
    This method takes the questions from the Creator and stores it in the db
    Arg:
        game_id this will allow querying from the database for the game and store it as a foreign key in the questions object
    '''
    current_game = Game.query.filter_by(game_id=game_id).first()
    game_questions = Question.query.filter_by(game_id=game_id).all()
    if request.method == 'post':
        question = request.form.get('question')
        new_question = Question(question=question,game_id=current_game.id)
        db.session.add(new_question)
        db.session.commit()

        return redirect(url_for('.add_question',game_id=game_id))

    return render_template('addquestions.html',game_questions=game_questions)

@main.route('/choices/<int:question_id>')
def choices(question_id):
    '''
    This method will add the choices to the  database to the questions created
    Arg:
        question_id this will allow quering the db to access the question so as to store it as a foreign key in the choices table
    '''
    question = Question.query.get(question_id)
    if request.method == 'post':
        choice = request.form.get('choice')
        status = request.form.get('status')
        points = request.form.get('points')
        new_choice = Choices(question_id=question,choice=choice,status=status,points=points)
        db.session.add(new_choice)
        db.session.commit()
        return redirect(url_for('.choices',question_id=question_id))
    return render_template('choices.html',title='Add choices')

@main.route('/profile/bio/<uid>' , methods=['POST','GET'])
@login_required
def add_bio(uid):
    user = User.query.filter_by(id = uid).first()
    games = Game.query.filter_by(user_id=user.id).all()
    # if current_user.id == uid:
    if request.method == 'POST':
        bio = request.form.get('bio')
        if user == None:
            abort(404)
        else:
            user.bio = bio
            db.session.add(user)
            db.session.commit()
            return jsonify({'success':f'{bio}'})

    # else:
        # print('******4********')
        # return render_template ( 'profile.html',user=user,games=games)
    return render_template ( 'profile.html',user=user,games=games)


# @main.route('/preview')
# def preview():
#     questionspreview = Questions.query.get()
