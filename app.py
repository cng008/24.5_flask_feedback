from flask import Flask, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import UserForm, LoginForm, FeedbackForm

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
    feed = Feedback.query.all()
    return render_template('feedback/list.html', feed=feed)


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
        new_user = User.register(username, password, email, first_name, last_name)

        db.session.add(new_user)
        db.session.commit()
        session['username'] = new_user.username
        flash("Welcome! Your account was created (-:", "success")
        return redirect(f'/users/{new_user.username}')

    return render_template('/user/signup.html', form=form)


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
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ['Invlaid username/password.']            

    return render_template('user/login.html', form=form)


@app.route('/logout')
def logout():
    """Clear any information from the session and redirect to /"""
    session.pop('username')
    flash("You've been logged out.", "success")
    return redirect('/')


@app.route('/users/<username>')
def user_found(username):
    """Show information about the given user.
    Show all of the feedback that the user has given.
    For each piece of feedback, display with a link to a form to edit the feedback and a button to delete the feedback.
    Have a link that sends you to a form to add more feedback and a button to delete the user.
    """
    if "username" not in session:
        flash("Please login first!", "secondary")
        return redirect('/')

    user = User.query.get_or_404(username)
    feedback = Feedback.query.filter(Feedback.user_id == username)
    return render_template('user/profile.html', user=user, feed=feedback)


@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    """Delete user and all of their feedback from database."""
    if "username" not in session:
        flash("Your account has been deleted.", "secondary")
        return redirect('/')

    user = User.query.get_or_404(username)
    if user.username == session['username']:
        db.session.delete(user)
        db.session.commit()

    flash("You don't have permission to do that!", "danger")
    return redirect('/')


@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
def add_feedback(username):
    """Display a form to add feedback
    Add a new piece of feedback and redirect to /users/<username>
    """
    if "username" not in session:
        flash("You must be logged in to do that.", "danger")
        return redirect('/')

    form = FeedbackForm()
    user = User.query.get_or_404(username)
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        new_feedback = Feedback(title=title, content=content, user_id=session['username'])

        db.session.add(new_feedback)
        db.session.commit()
        flash('Your feedback was successfully submitted!', "success")
        return redirect(f'/users/{ user.username }')

    return render_template('feedback/add.html', form=form, user=user)


@app.route('/feedback/<int:feedback_id>/update', methods=["GET", "POST"])
def edit_feedback(feedback_id):
    """Display a form to edit feedback
    Update a specific piece of feedback and redirect to /users/<username> 
    """
    if "username" not in session:
        flash("Please login first!", "secondary")
        return redirect('/login')
        
    feedback = Feedback.query.get_or_404(feedback_id)
    form = FeedbackForm(obj=feedback)
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()
        flash('Your feedback was successfully edited!', "success")
        return redirect(f'/users/{ feedback.username }')

    return render_template('feedback/edit.html', form=form, feedback=feedback)


@app.route('/feedback/<int:feedback_id>/delete', methods=["GET", "POST"])
def delete_feedback(feedback_id):
    """Delete a specific piece of feedback and redirect to /users/<username>"""
    if "username" not in session:
        flash("Please login first!", "secondary")
        return redirect('/login')

    feedback = Feedback.query.get_or_404(feedback_id)
    user = session['username']
    if feedback.user_id == user:
        db.session.delete(feedback)
        db.session.commit()
        return redirect(f'/users/{ user }')

    flash("You don't have permission to do that!", "danger")
    return redirect('/')

