"""Seed file to make sample data for feedback db."""

from models import db, User, Feedback
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Make a bunch of users
u1 = User(username='LegoLover', password="$2b$12$p/GJk2FrX1zMjLXjUpwxo.Pz9IqPerVhAaMCzdH4NBJzKfO5qsv2a", email='ilovelegos@lego.com', first_name='Bob', last_name='Builder') #brickedUp1
u2 = User(username='iSteve', password="$2b$12$7b6j6nidPxLWcyxjXSPjZ.hU11P3Y4KwOFxGIoJYpjtiUrmvNkSdy", email='steve@apple.com', first_name='Steve', last_name='Jobs') #iamagenius
u3 = User(username='vhristien', password="$2b$12$swq8xRzKGC9KGalEZxux9.v6JlYEP6.CPhb3yombejki/dEruLnbW'", email='christien@christien.com', first_name='Christien', last_name='Ng') #123456

db.session.add_all([u1, u2, u3])
db.session.commit()

p1 = Feedback(title='building blocks', content='great start for a solid foundation', user_id='LegoLover')
p2 = Feedback(title='awesome', content='learned a lot', user_id='iSteve')
p3 = Feedback(title='sick', content='this is a sick app', user_id='vhristien')
p4 = Feedback(title='Lorem', content='Lorem ipsum dolor, sit amet consectetur adipisicing elit. Consequuntur autem quae sapiente quasi, corrupti omnis fugit accusamus est enim eveniet id architecto reiciendis sit excepturi aperiam ea error iusto repellendus.', user_id='vhristien')

db.session.add_all([p1, p2, p3, p4])
db.session.commit()
