
from flask import Flask, Blueprint,render_template,request,flash,redirect,url_for

from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user,login_required,logout_user,current_user


auth = Blueprint('auth', __name__)
@auth.route('/')
def home():
    return render_template('home.html')
@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email=request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first() #looking for a specific section
        if user:
            if check_password_hash(user.password, password):
                flash('login success',category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('login fail',category='error')
        else:
            flash('email does not exsit',category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up',methods=['GET','POST'])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("firstname","")
        password1 = request.form.get("password")
        password2 = request.form.get("password2")
        data = request.form
        print(data)

        user = User.query.filter_by(email=email).first()
        if user:
            flash('user already exists',category='error')
        elif len(email)<4:
            flash("Email must be at least 4 characters",category="error")
            pass
        elif len(first_name) <2:
            flash("First name must be at least 2 characters",category="error")
            pass
        elif password1 != password2:
            flash("Passwords must match",category="error")
            pass
        elif len(password1)<8:
            flash("Password must be at least 8 characters",category="error")
            pass
        else:
            new_user = User(email=email,first_name=first_name,password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash("Registered for Monoesports,Massive W",category="success")
            return redirect(url_for('views.home'))


    return render_template('sign_up.html',user=current_user)