from . import auth
from flask import render_template,jsonify,request,redirect,url_for
from app.models import User
from flask_login import login_user,logout_user,login_required,current_user,is_authenticated
@auth.route('/login', methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
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
