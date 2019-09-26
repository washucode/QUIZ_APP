from . import auth
from flask import render_template,jsonify,request,redirect,url_for
from app.models import User
from flask_login import login_user,logout_user,login_required,current_user
from werkzeug.security import generate_password_hash,check_password_hash
from app import db
@auth.route('/login', methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    else:
        if request.method == 'POST':
            form = request.form
            email = form.get('email')
            password = form.get('password')
            user = User.query.filter_by(email = email).first()
            if user is not None:
                if check_password_hash(user.password_hash,password):
                    login_user(user)
                    print('Passed********************************************')
                    return jsonify({'awesome':True})
                else:
                    return jsonify({'imeanguka':True})
            else:
                return jsonify({'imeanguka':True})

        return render_template('auth/login.html')

@auth.route('/signup', methods=['POST','GET'])
def signup():
    if  current_user.is_authenticated:
        return redirect(url_for('main.index'))
    else:
        if request.method == "POST":
            form = request.form
            username = form.get('username')
            email = form.get('email')
            password = form.get('password')
            confirm_password = form.get('confirm_password')
            print(username,email,password)
            if password != confirm_password:
                return jsonify({'pwd_err':'passwords Dont match'})
            user = User.query.filter_by(username = username).first()
            if user != None:
                print('****************************usr err')
                return jsonify({'username_err':'Username already taken'})
            user = User.query.filter_by(email = email).first()
            if user != None:
                print('****************************email err')
                return jsonify({'email_err':'Email already taken'})
            new_user =User(email = email , username=  username, password_hash = generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'awesome':True})
        return render_template('auth/signup.html')

@auth.route('/profile/change/pwd/<uid>', methods=['POST','GET'])
@login_required
def change_password(uid):
    if current_user.is_authenticated:
        if request.method == 'POST':
            form = request.form
            former_password = form.get('former_password')
            new_password = form.get('new_password')
            confirm_new_password = form.get('confirm_new_password')
            user = User.query.filter_by(id = uid).first()
            if user == None:
                abort(404)
            else:
                if check_password_hash(user.password_hash,former_password) == False:
                    return jsonify({'invalid':'Invalid password'})
                else:
                    if new_password != confirm_new_password:
                        return jsonify({'notmatch':'Passwords dont match'})
                    if former_password == new_password:
                        return jsonify({'equalToOld':'The new password should be different from the old password'})

                    else:
                        user.password_hash = generate_password_hash(new_password)
                        db.session.add(user)
                        db.session.commit()
                        return jsonify({'changed':'Your password has ben successfuly changed'})
    else:
        abort(404)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')
