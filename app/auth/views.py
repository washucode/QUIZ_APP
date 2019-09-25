from . import auth
from flask import render_template,jsonify,request,redirect,url_for
from app.models import User
from flask_login import login_user,logout_user,login_required,current_user
from werkzeug.security import generate_password_hash,check_password_hash

@auth.route('/login', methods=['POST','GET'])
def login():
    if current_user != None:
        return redirect('main.index')
    else:
        if request.method == 'POST':
            form = request.form
            email = form.get('email')
            password = form.get('password')
        user = User.query.filter_by(email = email).first()
        if user is not None and user.verify_password(password):
            login_user(user)
            return jsonify({'success':True})
        else:
            return jsonify({'success':False})

        return render_template('auth/login.html')

@auth.route('/signup', methods=['POST','GET'])
def signup():
    if current_user != None:
        return redirect('main.index')
    else:
        if request.method == "POST":
            form = request.form
            username = form.get('username')
            email = form.get('email')
            password = form.get('password')

            user = User.query.filter_by(email = email).first()
            if user != None:
                return jsonify({'email_err':'Email already taken'})
            user = User.query.filter_by(username = username).first()
            if user != None:
                return jsonify({'username_err':'Username already taken'})
            new_user =User(email = email , username=  username, password_hash = generate_password_hash(password))
            return jsonify({'success':True})

        return render_template('auth/signup.html')
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')
