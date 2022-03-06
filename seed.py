"""Seed file to make sample data for feedback db."""

from models import db, User, Feedback
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Make a bunch of users
u1 = User(username='LegoLover', password="b'$2b$12$p/GJk2FrX1zMjLXjUpwxo.Pz9IqPerVhAaMCzdH4NBJzKfO5qsv2a", email='ilovelegos@lego.com', first_name='Bob', last_name='Builder') #brickedUp1
u2 = User(username='iSteve', password="b'$2b$12$7b6j6nidPxLWcyxjXSPjZ.hU11P3Y4KwOFxGIoJYpjtiUrmvNkSdy", email='steve@apple.com', first_name='Steve', last_name='Jobs') #iamagenius

db.session.add_all([u1, u2])
db.session.commit()

p1 = Feedback(title='building blocks', content='great start for a solid foundation', user_id='LegoLover')
p2 = Feedback(title='awesome', content='learned a lot', user_id='iSteve')

db.session.add_all([p1, p2])
db.session.commit()
