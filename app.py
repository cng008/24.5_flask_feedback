from flask import Flask, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User
from forms import UserForm, LoginForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']  =  False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "shhhhhh"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def home_page():
    """Homepage."""
    return redirect('/register')


@app.route('/register', methods=["GET", "POST"])
def create_user():
    """GET: Show a form that when submitted will register/create a user.
        POST: Process the registration form by adding a new user. Then redirect to /secret.
    """
    form = UserForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        new_user = User.register(username, password, first_name, last_name, email)

        db.session.add(new_user)
        db.session.commit()
        session['username'] = new_user.username
        flash("Welcome! Your account was created (-:", "success")
        return redirect('/secret')

    return render_template('signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def auth_user():
    """GET: Show a form that when submitted will login a user.
        POST: Process the login form, ensuring the user is authenticated and going to /secret if so.
    """
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome back, {user.username}!", "success")
            session['username'] = user.username
            return redirect('/secret')
        else:
            form.username.errors = ['Invlaid username/password.']            

    return render_template('login.html', form=form)


@app.route('/secret', methods=["GET"])
def user_found():
    """Return the text “You made it!”"""
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/')
    return render_template('list.html')


@app.route('/logout')
def logout():
    """Clear any information from the session and redirect to /”"""
    session.pop('username')
    flash("You've been logged out.", "success")
    return redirect('/')