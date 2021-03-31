from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
# standard routes - homepage, etc - creates a blueprint for views, urls

auth = Blueprint('auth', __name__)

#Login, logout signup - add to url to get to view/page - defining pages and location
#pass values to templates from backend to display on front page - beside .html template


@auth.route('/login', methods=['GET', 'POST'])  # GET AND POST can accept get and posts requests at route
def login():
    #data = request.form #get information sent in form
    #print(data)
    #login users
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        #check if valid
        # check if user dosent exist/have email when signing up

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True) #login user - remembers in session
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user) # , text="Testing", user="Daryl") # "<p>Login</p>"

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))#"<p>Logout</p>"

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    #differentiate between get and post request
    if request.method == 'POST': #getting request/infor from form
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')


        #check if valid - if not do not create new user account
        # check if user dosent exist/have email when signing up
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exist.', category='error')

        elif len(email) < 4:
            #flash message on validity check - can use any category - just know what they mean - uses different color
            flash('Email must be greater than 3 characters.', category='error')

        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')

        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')

        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            #create new user
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256')) #method is hashing algorithm
            #add new user
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)  # login user - remembers in session
            flash('Account Created!', category='success')
            return redirect(url_for('views.home')) #after account created, redirects user to homepage -blueprint.function

    return render_template("sign_up.html", user=current_user) # "<p>Sign Up</p>"

