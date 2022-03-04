from flask import Flask, redirect, render_template
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
        new_user = User.register(first_name, last_name, email, username, password)

        db.session.add(new_user)
        db.session.commit()
        flash('Welcome! Your account was created (-:')
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
            return redirect('/secret')
        else:
            form.username.errors = ['Invlaid username/password.']            

    return render_template('login.html', form=form)


@app.route('/secret', methods=["GET", "POST"])
def user_found():
    """Return the text “You made it!”"""
    return ('You made it!')