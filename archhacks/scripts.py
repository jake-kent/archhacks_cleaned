import sys
import json
import requests
import math

from flask import Flask
from flask_sqlalchemy  import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug import generate_password_hash, check_password_hash

from models import User, School

app = Flask(__name__)
app.secret_key = "********************************"
app.config['SQLALCHEMY_DATABASE_URI'] = '********************************'

db = SQLAlchemy()
db.init_app(app)

def populateusersfromtypeform():
	used_emails = []
	with app.app_context():
		typeformdata = requests.get('https://api.typeform.com/v1/form/rak9AE?key=***************************************&completed=true&order_by=date_submit&limit=3000').json()
		responses = typeformdata['responses']
		for user in responses:
			try:
				first_name = user['answers']['textfield_18072312']
				last_name = user['answers']['textfield_18072313']
				email = user['answers']['email_18074955']
				if first_name is not None and len(first_name) > 0 and last_name is not None and len(last_name) > 0 and email is not None and len(email) > 0:
					if user['answers']['dropdown_20497446'] == "Other":
						school = (user['answers']['textfield_20513659'])
					else:
						school = (user['answers']['dropdown_20497446'])
					db_user = User.query.filter_by(email=email).first()
					try:
						if db_user is None and email not in used_emails:
							tempuser = User(firstname=first_name, lastname=last_name, email=email, password="dev1234", school=school)
							used_emails.append(email)
							db.session.merge(tempuser)
							db.session.commit()
						elif db_user is not None and db_user.school == "None Provided":
							db_user.school = school
							db.session.commit()
					except IntegrityError:
						continue

			except KeyError:
				continue

def popupdateschools():
	schools = {}
	with app.app_context():
		typeformdata = requests.get('https://api.typeform.com/v1/form/rak9AE?key=***************************************&completed=true&order_by=date_submit&limit=3000').json()
		responses = typeformdata['responses']
		for user in responses:
			school = user['answers']['dropdown_20497446']
			if school == 'Other':
				if 'textfield_20513659' in user['answers']:
					school = user['answers']['textfield_20513659']
				else:
					continue
			if school is not None:
				if school in schools:
					schools[school] += 1
				else:
					schools[school] = 1
		try:
			schools['Illinois Institute of Technology'] += 7
			schools['Case Western Reserve University'] += 4
			schools['University of Illinois at Chicago'] += 2
		except KeyError:
			pass
		for school in schools:
			try:
				db_school = School.query.filter_by(name=school).first()
				if db_school is not None:
					db_school.app_count = schools[school]
					db_school.dimension = int(min(70, 70 * pow(float(float(schools[school])/50), 0.333333333333)))
					db.session.commit()
				else:
					dimension = int(min(70, 70 * pow(float(float(schools[school])/50), 0.333333333333)))
					db_school = School(name=school, app_count=schools[school], dimension=dimension)
					db.session.add(db_school)
					db.session.commit()
			except IntegrityError:
				continue
			
def resetuser(email):
	with app.app_context():
		user = User.query.filter_by(email=email).first()
		if user is not None:
			print("are you sure you want to reset " +  email + "'s password? This cannot be undone!!")
			user.pwdhash = generate_password_hash("dev1234")
			db.session.merge(user)
			db.session.commit()


if __name__ == "__main__":
	if ("populateusersfromtypeform" in sys.argv[1]):
		populateusersfromtypeform()
	if ("popupdateschools" in sys.argv[1]):
		popupdateschools()
	if ("resetuser" in sys.argv[1]):
		if sys.argv[2]:
			resetuser(sys.argv[2])
