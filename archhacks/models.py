from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
	__tablename__ = 'users'
	uid = db.Column(db.Integer, primary_key=True)
	firstname = db.Column(db.String(100))
	lastname = db.Column(db.String(100))
	email = db.Column(db.String(120), unique=True)
	school = db.Column(db.String(512), nullable=True)
	pwdhash = db.Column(db.String(54))
	application_status = db.Column(db.Enum('Accepted', 'Rejected', 'Under Review', 'Wait Listed'), default="Under Review")
	attending = db.Column(db.Enum('Attending', 'Not Attending', 'No Response'), default="No Response")
	tourney_position = db.Column(db.Integer, nullable=True) # represents the position in the line for cornhole
	tourney_score = db.Column(db.Integer, nullable=True)
	twitter_handle = db.Column(db.String(120), nullable=True)
	won_round = db.Column(db.Boolean, nullable=True)
	is_admin = db.Column(db.Boolean)
	farthest_round = db.Column(db.Integer)

	def __init__(self, firstname, lastname, email, password, application_status="Under Review", attending="No Response", tourney_position=0, won_round=0, school="None Provided", is_admin=0, farthest_round=0, tourney_score=0, has_played=0, twitter_handle="", ):
		self.firstname = firstname.title()
		self.lastname = lastname.title()
		self.email = email.lower()
		self.school = school
		self.set_password(password)
		self.application_status = application_status
		self.tourney_position = tourney_position
		self.won_round = won_round
		self.attending = attending
		self.twitter_handle = twitter_handle
		self.is_admin = is_admin
		self.farthest_round = farthest_round
		self.tourney_score = tourney_score
		
	def name (self):
		return (" ".join([self.firstname, self.lastname]))

	def set_password(self, password):
		self.pwdhash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pwdhash, password)

class School(db.Model):
	__tablename__ = 'schools'
	uid = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(256))
	app_count = db.Column(db.Integer, default=0)
	dimension = db.Column(db.Integer, default=0)


	def __init__(self, name, app_count=0, dimension=0):
		self.name = name
		self.app_count = app_count
		self.dimension = dimension

class Event(db.Model):
	__tablename__ = 'events'
	uid = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(256))
	start_time = db.Column(db.String(256))
	end_time = db.Column(db.String(256))
	location = db.Column(db.String(256))
	description = db.Column(db.String(1024))
	category= db.Column(db.Enum('General', 'Food', 'Workshop', 'Fun'), default="General")

	def __init__(self, name, start_time, end_time, location, description, category):
		self.name = name
		self.start_time = start_time
		self.end_time = end_time
		self.location = location
		self.description = description
		self.category = category
