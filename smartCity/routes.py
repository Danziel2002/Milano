# ---------------------------------------------------------
#
# Page for the milano contest by Iasmina Martinovici, Alex Tanase and Gruescu Daniel
# Designer : Iasmina Martinovici
# FrontEnd developer : Alex Tanase
# BackEnd developer : Gruescu Daniel
#
# ---------------------------------------------------------


#Imports
from flask import render_template, url_for, flash, redirect, request, jsonify
from smartCity import app, db, bcrypt
from smartCity.forms import RegistrationForm, LoginForm, AccountForm, PostForm, AddToCart
from smartCity.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required, mixins


#Function for leveling up
def levelUp():
    if not(current_user.is_anonymous):
        editUser = User.query.filter_by(username=current_user.username).first()
        editUser.experience -= 100
        editUser.level += 1
        db.session.commit()
    else:
        print("no user")

#Function that gives the user some exp for a completed task
def giveExp(expGot):
    if not(current_user.is_anonymous):
        editUser = User.query.filter_by(username=current_user.username).first()
        db.session.commit()
        if editUser.experience >= 100:
            levelUp()
    else:
        print("no user")


#The routes for the home page
@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    if not(current_user.is_anonymous):
        return render_template('home.html', posts=posts, level = current_user.level)
    else:
        return render_template('home.html', posts=posts, level = 'not user')


#The route for the about page
@app.route("/about")
def about():
    return render_template('about.html', title='About')


#The route for the register page
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,experience=0, level=0, email=form.email.data, password=hashed_password, cart="Empty", ItemsInCart = 0)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    else:
        print("OOOO")
    return render_template('register.html', title='Register', form=form)



#The route for the login page
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


#The logout function
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


#The route to modify an account
@app.route("/account",methods=['GET', 'POST'])
@login_required
def account():
    form = AccountForm()
    if form.validate_on_submit():
        if form.username.data != '':
            editUser = User.query.filter_by(username=current_user.username).first()
            editUser.username = form.username.data
            db.session.commit()
        if form.email.data != '':
            editUser = User.query.filter_by(email=current_user.email).first()
            editUser.email = form.email.data
            db.session.commit()
        if form.password.data != '':
            editUser = User.query.filter_by(password=current_user.password).first()
            editUser.password = hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            db.session.commit()
    return render_template('account.html', title='Account', form = form)

#The route for the option page
@app.route('/actions')
@login_required
def actions():
    return render_template('actions.html')

@app.route('/dummy')
def dummy():
    return render_template('dummy.html')
