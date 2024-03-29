from . import main
from flask import render_template,request,redirect,url_for,flash,abort,jsonify
from ..models import User,Player,Game,Question,Choices
from .. import db,photos
from flask_login import login_required,current_user

@main.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        player_name = request.form.get('player_name')
        game_code = request.form.get('game_code')
        game = Game.query.filter_by(game_password=game_code).first()
        if game is not None:
            player = Player(player_name=player_name, game_id=game.id)
            db.session.add(player)
            db.session.commit()
            return redirect(url_for('main.game',game_id=game.id,player_id=player.id))
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
    game = Game.query.filter_by(id = game_id).first()
    player = Player.query.filter_by(id = player_id).first()
    players = game.player

    questions = Question.query.filter_by(game_id = game_id).all()

    if request.method == 'POST':
        counter = 0
        q_id=[]
        for que in questions:
            q_id.append(que.id)
        selected = []
        for id in q_id:
            selected.append(int(request.form.get(str(id))))
        player.results = sum(selected)
        db.session.commit()


    return render_template('do_questions.html',game=game,questions = questions,player=player)

@main.route('/creategame/<int:user_id>',methods = ['POST','GET'])
@login_required
def create_game(user_id):
    '''
    This method takes in game data from the user and stores it in the database
    Arg:
        user_id in order to assighn the question the foreign key to the user who created it
    '''

    if request.method == "POST":

        gamename = request.form.get('gamename')
        description = request.form.get('description')
        award = request.form.get('award')
        status = request.form.get('status')
        if status.lower() == "true" or status.lower() == "t":
            status_real = True
        elif status.lower() == 'false ' or status.lower() == "f":
            status_real = False
        else:
            flash("Please enter valid input")
        game_password = request.form.get('game_password')

        new_game = Game(gamename=gamename,description=description,award=award,status=status_real,game_password=game_password,user_id=current_user.id)
        db.session.add(new_game)
        db.session.commit()
        game_id = Game.query.filter_by(gamename=gamename).first()
        return redirect(url_for('.add_questions',game_id=game_id.id))
        print(gamename)
    return render_template('create_game.html')

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
    current_game = Game.query.filter_by(id=game_id).first()
    current_player = Player.query.get(game_id)
    print("====",current_player)
    game_questions = Question.query.filter_by(game_id=game_id).all()

    if request.method == 'POST':
        question = request.form.get('question')
        print("-----",question)
        new_question = Question(question=question,game_id=current_game.id)
        db.session.add(new_question)
        db.session.commit()
        print("----",new_question)

        return redirect(url_for('.add_questions',game_id=current_game.id))

    return render_template('add_questions.html',game_questions=game_questions,game_id=current_game.id)

@main.route('/choices/<int:question_id>',methods=['POST','GET'])
def choices(question_id):
    '''
    This method will add the choices to the  database to the questions created
    Arg:
        question_id this will allow quering the db to access the question so as to store it as a foreign key in the choices table
    '''
    question = Question.query.get(question_id)
    if request.method == 'POST':
        choice = request.form.get('choice')
        status = request.form.get('status')
        points = request.form.get('points')
        status_real = True
        if status.lower() == "true" or status.lower() == "t":
            status_real = True
        elif status.lower() == 'false ' or status.lower() == "f":
            status_real = False
        else:
            flash("Please enter valid input")
        new_choice = Choices(question_id=question.id,choice=choice,status=status_real,points=points)
        db.session.add(new_choice)
        db.session.commit()

        return redirect(url_for('.choices',question_id=question.id, game_id= question.game_id))
    return render_template('choices.html',question_id=question.id, game_id= question.game_id)

@main.route('/profile/bio/<uid>' , methods=['POST','GET'])
@login_required
def add_bio(uid):
    user = User.query.filter_by(id = uid).first()
    games = Game.query.filter_by(user_id=user.id).all()
    if request.method == 'POST':
        bio = request.form.get('bio')
        if user == None:
            abort(404)
        else:
            user.bio = bio
            db.session.add(user)
            db.session.commit()
            return jsonify({'success':f'{bio}'})

    return render_template ( 'profile.html',user=user,games=games)

@main.route('/profile/edit/bio/<uid>', methods=['POST','GET'])
@login_required
def update_bio(uid):
    user = User.query.filter_by(id = uid).first()
    games = Game.query.filter_by(user_id=user.id).all()
    if request.method == 'POST':
        changeBio = request.form.get("changeBio")
        if user == None:
            abort(404)
        else:
            print(changeBio)
            user.bio = changeBio
            db.session.add(user)
            db.session.commit()
            return jsonify({'passed':'Bio has been successfuly saved','success':f'{changeBio}'})
    return render_template ( 'profile.html',user=user,games=games)


@main.route('/profile/add_photo/<uid>', methods=['POST','GET'])
@login_required
def profile_photo(uid):
    user = User.query.filter_by(id = uid).first()
    games = Game.query.filter_by(user_id=user.id).all()
    if request.method == 'POST':
        if 'profilePic'  in request.files:
            print('********1*')
            filename = photos.save(request.files.get('profilePic'))
            path = f'photos/{filename}'
            print('*********',path)
            if user == None:
                abort(404)
            else:
                user.profile_photo = path
                db.session.add(user)
                db.session.commit()

    return render_template ( 'profile.html',user=user,games=games)

@main.route('/profile/update_photo/<uid>', methods=['POST','GET'])
@login_required
def update_profile_photo(uid):
    user = User.query.filter_by(id = uid).first()
    games = Game.query.filter_by(user_id=user.id).all()
    if request.method == 'POST':
        if 'UpdatePic'  in request.files:
            print('********1*')
            filename = photos.save(request.files.get('UpdatePic'))
            path = f'photos/{filename}'
            print('*********',path)
            if user == None:
                abort(404)
            else:
                user.profile_photo = path
                db.session.add(user)
                db.session.commit()

    return render_template ( 'profile.html',user=user,games=games)
