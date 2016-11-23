import json
import requests
import string
import random
import schedule
import time
from flask import Flask
from flask import render_template, session, request, url_for, redirect, send_file, jsonify
from models import db, User, School, Event
from forms import SignupForm, SigninForm, TourneyForm, ChangePassForm, ConfirmAttendanceForm, ForgotPasswordForm, TwitterHandleForm
from werkzeug import generate_password_hash, check_password_hash
from flask.ext.mail import Mail, Message
from scripts import popupdateschools
from dateutil import parser


app = Flask(__name__)


app.secret_key = "********************************"

app.config['SQLALCHEMY_DATABASE_URI'] = '********************************'
app.config.update(
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.zoho.com',
	MAIL_PORT=465,
	MAIL_USE_TLS = False,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = '********************************',
	MAIL_PASSWORD = '********************************'
)

mail = Mail(app)

from models import db
db.init_app(app)

tourney_started = False
tourney_round = 0

def parse_params(params):
	params_string = ""
	first = True
	for param in params:
		if not first:
			params_string += "&"
		params_string += str(param[0])
		params_string += "="
		params_string += str(param[1])
		if first: first = False;
	return params_string

#homepage
@app.route('/')
def static_homepage():
	schedule = Event.query.all()
	novfourevents = []
	novfiveevents = []
	novsixevents = []
	for event in schedule:
		event.start_time = parser.parse(event.start_time)
		event.end_time = parser.parse(event.end_time)
		if event.start_time.day == 4:
			novfourevents.append(event)
		if event.start_time.day == 5 or event.end_time.day == 5:
			novfiveevents.append(event)
		if event.start_time.day == 6 or event.end_time.day == 6:
			novsixevents.append(event)
	novfourevents.sort(key=lambda x: x.start_time)
	novfiveevents.sort(key=lambda x: x.start_time)
	novsixevents.sort(key=lambda x: x.start_time)
	
	return render_template('index.html', novfourevents=novfourevents, novfiveevents=novfiveevents, novsixevents=novsixevents)

#favicon
@app.route('/favicon.ico')
def favicon():
	return send_file("static/images/favicon.ico", mimetype='image/ico')

#volunteer
@app.route('/volunteer')
def volunteer():
	return render_template('volunteer.html')

#sponsor feedback
@app.route('/sponsor/feedback')
def sponsor_feedback():
	params = request.args.items()
	if params:
		params_string = parse_params(params)
	else:
		params_string = None
	return render_template('sponsor_feedback.html', params_string=params_string)

#rubric
@app.route('/rubric')
def rubric():
	return send_file("static/files/Rubric.pdf", mimetype='application/pdf')

#driving - directions
@app.route('/driving')
def driving_destination():
	return send_file("static/files/Driving_Info.pdf", mimetype='application/pdf')

#packing list
@app.route('/remember')
@app.route('/packing_list')
def packing_list():
	return send_file("static/files/Packing_List.pdf", mimetype='application/pdf')

#judging criteria/format
@app.route('/judging')
def judging_criteria():
	return send_file("static/files/Judging_Handout.pdf", mimetype='application/pdf')

#schedule
@app.route('/schedule')
def schedule_handout():
	return send_file("static/files/schedule.pdf", mimetype='application/pdf')

#map
@app.route('/map')
def indoor_outdoor_map():
	return send_file("static/images/indoor_outdoor_map.png", mimetype='image/png')

#directions
@app.route('/to')
def archhacks_directions_redirect():
	return redirect('https://www.google.com/maps/dir//38.6504722,-90.3106389/@38.6504703,-90.3281485,14z/data=!4m8!1m7!3m6!1s0x0:0x0!2zMzjCsDM5JzAxLjciTiA5MMKwMTgnMzguMyJX!3b1!8m2!3d38.650475!4d-90.310643', code=301)

#carpool
@app.route('/carpool')
def carpool():
	return redirect(url_for('carpool_redirect'))

#carpool redirect
@app.route('/ArchHacks - Gas Reimbursement Guide')
def carpool_redirect():
	return send_file("static/files/ArchHacks_Gas_Reimbursement_Guide.pdf", mimetype='application/pdf')

#bus route forms
@app.route('/bus/<bus_route>')
def bus_forms(bus_route):
	params = request.args.items()
	if params:
		bus_params = parse_params(params)
	else:
		bus_params = None
	if bus_route:
		bus_route = bus_route.lower()
		if bus_route == "purdue":
			return render_template("bus.html", bus_route="Purdue", bus_params=bus_params, bus_form_id="1FAIpQLSc4AFmoXdK_rd-BYwoGQCeXXyY-rQ-dLXy09R22QwCpgc3nYA")
		elif bus_route == "chicago":
			return render_template("bus.html", bus_route="UChicago", bus_params=bus_params, bus_form_id="1FAIpQLScVf4Ilof9ldpxkEn3XdSjWm8P8vAS2E9s4o0r4ghQPMHEk6A")
		elif bus_route == "cmu" or bus_route == "osu":
			return render_template("bus.html", bus_route=bus_route, bus_params=bus_params, bus_form_id="1FAIpQLSddumY3-WALGfE_MeZ6oUMCpUYBkpUFAaEHQQ-AqRkybpmtIg")
		elif bus_route == "florida":
			return render_template("bus.html", bus_route="UFlorida", bus_params=bus_params, bus_form_id="1FAIpQLSeEM3rfW-GcKljS0VVa9ECCxXoeAi8FDw_ligRMa8pX5Mbk8Q")
		elif bus_route == "gt":
			return render_template("bus.html", bus_route="Georgia Tech", bus_params=bus_params, bus_form_id="1FAIpQLScBLhN0igeuisXIEVxhW6rs9EPZE_RcM7DARbjuNy7r6aBEaw")
		elif bus_route == "uiuc":
			return render_template("bus.html", bus_route="UIUC", bus_params=bus_params, bus_form_id="1FAIpQLSdV4wES76OCHcLFaTLLCBFkvwyR06nTqrcvPx3fx60WR3TL3g")
		elif bus_route == "uwaterloo":
			return render_template("bus.html", bus_route="UWaterloo", bus_params=bus_params, bus_form_id="1FAIpQLSf9OiIJ5swEPGMZOvjD5d7I_eITBytG7xEE70On88zrybqanQ")
		else:
			return "Please enter archhacks.io/bus/ followed by purdue, chicago, cmu, osu, florida, gt, UIUC or uwaterloo to find your bus waitlist form."
	else:
		return "Please enter archhacks.io/bus/ followed by purdue, chicago, cmu, osu, florida, gt, UIUC or uwaterloo to find your bus waitlist form."

#driver form
@app.route('/carpool/driver')
def carpool_driver():
	params = request.args.items()
	if params:
		params_string = parse_params(params)
	else:
		params_string = None
	return render_template('driver.html', params_string=params_string)

#driver confirm form
@app.route('/carpool/driver/confirm')
def carpool_driver_confirm():
	params = request.args.items()
	if params:
		params_string = parse_params(params)
	else:
		params_string = None
	return render_template('driver_confirm.html', params_string=params_string)

@app.route('/carpool/passenger')
def carpool_passenger():
	params = request.args.items()
	if params:
		params_string = parse_params(params)
	else:
		params_string = None
	return render_template('passenger.html', params_string=params_string)

@app.route('/meditation')
def meditation():
	params = request.args.items()
	if params:
		params_string = parse_params(params)
	else:
		params_string = None
	return render_template('meditation.html', params_string=params_string)

@app.route('/application-stats')
def applications_data_vis():
	ignore_schools = ['Washington University in St. Louis', 'University of Southern California', 'UC Berkeley']
	schools = School.query.all()
	schools.sort(key=lambda x: x.app_count, reverse=True)
	schools = [school for school in schools if school.app_count >= 5 and school.name not in ignore_schools]
	return render_template('application-stats.html', schools=schools)

@app.route('/application-stats.html')
def applications_data_vis_old():
	return redirect(url_for('applications_data_vis'))

@app.route('/app_home')
def app_homepage():
	return render_template('app_home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = SignupForm()
	if request.method == 'POST':
		if not form.validate():
			return render_template('signup.html', form=form)
		else:
			newuser = User(firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data, school=form.school.data, password=form.password.data)
			db.session.add(newuser)
			db.session.commit()

			session['email'] = newuser.email
			return redirect(url_for('profile'))

	elif request.method == 'GET':
		return render_template('signup.html', form=form)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
	form = ConfirmAttendanceForm()
	twitter_handle_form = TwitterHandleForm()
	if 'email' not in session:
		return redirect(url_for('signin'))
	user = User.query.filter_by(email = session['email']).first()
	if user is None:
			return redirect(url_for('signin'))
	if request.method == 'POST':
		if not twitter_handle_form.validate():
			return render_template('profile.html', user=user, form=form, twitter_handle=twitter_handle_form)
		else:
			user.twitter_handle = twitter_handle_form.twitter_handle_field.data
			db.session.commit()
			return render_template('profile.html', user=user, form=form, twitter_handle=twitter_handle_form)
	elif request.method == 'GET':
		return render_template('profile.html', user = user, form=form, twitter_handle=twitter_handle_form)

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
	if 'email' not in session:
		return redirect(url_for('signin'))
	form = ChangePassForm()
	if request.method == 'POST':
		if not form.validate():
			return render_template('change_password.html', form=form)
		else:
			user = User.query.filter_by(email = session['email']).first()
			if user is None:
				return redirect(url_for('signin'))
			else:
				user.pwdhash = generate_password_hash(form.new_pass.data)
				db.session.commit()
				return redirect(url_for('profile'))
			

	elif request.method == 'GET':
		return render_template('change_password.html', form=form)

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
	form = ForgotPasswordForm()
	if request.method == 'GET':
		return render_template('forgot_password.html', form=form)
	if request.method == 'POST':
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None:
			temppass = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(24))
			user.pwdhash = generate_password_hash(temppass)
			db.session.commit()
			msg = Message(
					'ArchHacks - Password Reset',
					sender='admin@archhacks.io',
					recipients=[form.email.data])
			msg.body = "Your temporary ArchHacks password is: archhacksrulez."
			msg.html = "<p>Your temporary ArchHacks password is: "+temppass+"</p><p>Go to <a href='http://archhacks.io/signin'>ArchHacks App Signin</a> to log in.</p>"
			mail.send(msg)
		return render_template('forgot_password.html', email=form.email.data)

@app.route('/confirm_attendance', methods=['POST'])
def confirm_attendance():
	form = ConfirmAttendanceForm()
	if 'email' not in session:
		return redirect(url_for('signin'))
	if request.method == 'POST':
		user = User.query.filter_by(email = session['email']).first()
		if user is None:
			return redirect(url_for('signin'))
		if 'not_attending' in request.form:
			user.attending = "Not Attending"
			db.session.commit()
			return redirect(url_for('profile'))
		elif 'attending' in request.form:
			user.attending = "Attending"
			db.session.commit()
			return redirect(url_for('profile'))
		return redirect(url_for('profile'))


@app.route('/signin', methods=['GET', 'POST'])
def signin():
	form = SigninForm()
	if request.method == 'POST':
		if not form.validate():
			return render_template('signin.html', form=form)
		else:
			session['email'] = form.email.data
			return redirect(url_for('profile'))

	elif request.method == 'GET':
			return render_template('signin.html', form=form)

@app.route('/signout')
def signout():
	if 'email' not in session:
		return redirect(url_for('signin'))

	session.pop('email', None)
	return redirect(url_for('app_homepage'))

@app.route('/tourney', methods=['GET', 'POST'])
def tourney():
	if 'email' not in session:
		return redirect(url_for('signin'))

	# people who are still waiting to play
	reg_users = [user for user in User.query.order_by(User.tourney_position).all() if user.tourney_position > 0 and not user.won_round]

	# people in first round who have played and have a score, ordered by highest score
	scored_users = [user for user in User.query.order_by(User.tourney_score.desc()).all() if user.won_round]

	# people who have played and won
	won_users = [user for user in User.query.order_by(User.tourney_position).all() if user.won_round]

	tourney_form = TourneyForm()

	user = User.query.filter_by(email=session['email']).first()
	message = ""
	if request.method == 'POST':
		if tourney_form.reg_validate(user):
			# update database to register user
			last = db.session.query(db.func.max(User.tourney_position)).scalar()
			user.tourney_position = last + 1
			db.session.commit()

			reg_users.append(user)
			message = "You have successfully registered"
		elif tourney_form.unreg_validate(user):
			user.tourney_position = 0
			db.session.commit()

			reg_users.remove(user)
			message = "You have successfully unregistered"

	if not 'error' in locals() and not 'error' in globals():
		error = None;

	if tourney_round == 0:
		return render_template('tourney_round0.html',
							   user=user,
							   tourney_form=tourney_form,
							   message=message,
							   error=error,
							   reg_users=reg_users,
							   tourney_started=tourney_started,
							   scored_users=scored_users,
							   round=tourney_round)

	return render_template(
							'tourney.html',
							user=user,
							won_users=won_users,
							tourney_form=tourney_form,
							reg_users=reg_users,
							message=message,
							error=error,
							round=tourney_round,
							tourney_started=tourney_started)


@app.route('/start_tourney', methods=['GET'])
def start_tourney():
	if 'email' not in session:
		return redirect(url_for('signin'))

	user = User.query.filter_by(email=session['email']).first()

	if not user.is_admin:
		return redirect(url_for('profile'))

	global tourney_started
	tourney_started = True

	return redirect(url_for('tourney'))


@app.route('/tourney_next_round', methods=['GET'])
def tourney_next_round():
	if 'email' not in session:
		return redirect(url_for('signin'))

	user = User.query.filter_by(email=session['email']).first()

	if not user.is_admin:
		return redirect(url_for('profile'))

	global tourney_round
	tourney_round += 1

	# get all users who have won and put them back in line
	won_users = [user for user in User.query.order_by(User.tourney_position) if user.tourney_position != 0]

	for i, user in enumerate(won_users, start=2):
		if not user.won_round:
			# if there was an odd number of players, put the person that got the bye at the beginning
			user.tourney_position = 1
		else:
			user.won_round = 0
			user.tourney_position = i

		user.farthest_round = tourney_round
	db.session.commit()

	return redirect(url_for('tourney'))


@app.route('/set_tourney_winner', methods=['GET', 'POST'])
def set_tourney_winner():
	if 'email' not in session:
		return redirect(url_for('signin'))

	user = User.query.filter_by(email=session['email']).first()

	if not user.is_admin:
		return redirect(url_for('profile'))

	user0_email = request.form.get('user0_email').strip()
	user1_email = request.form.get('user1_email').strip()
	entered_email = request.form.get('email_entry').strip()

	if entered_email == user0_email and user0_email != "":
		winner_email = user0_email
		loser_email = user1_email
	elif entered_email == user1_email and user1_email != "":
		winner_email = user1_email
		loser_email = user0_email
	else:
		# entered email did not match either competitor
		return redirect(url_for('tourney'))

	winner = User.query.filter_by(email=winner_email).first()
	winner.won_round = 1

	loser = User.query.filter_by(email=loser_email).first()
	if loser is not None:
		loser.tourney_position = 0

	db.session.commit()

	return redirect(url_for('tourney'))


@app.route('/set_tourney_score', methods=['POST'])
def set_tourney_score():
	if 'email' not in session:
		return redirect(url_for('signin'))

	user = User.query.filter_by(email=session['email']).first()

	if not user.is_admin:
		return redirect(url_for('profile'))

	user_email = request.form.get('email_entry').strip()
	score = request.form.get('score')

	found_user = User.query.filter_by(email=user_email).first()
	if found_user is not None:
		found_user.won_round = 1
		found_user.tourney_score = int(score)

	db.session.commit()
	return redirect(url_for('tourney'))



@app.route('/begin_bracket_style', methods=['GET'])
def begin_bracket_style():
	if 'email' not in session:
		return redirect(url_for('signin'))

	user = User.query.filter_by(email=session['email']).first()

	if not user.is_admin:
		return redirect(url_for('profile'))

	# select top 64 users, put them back in the pool
	played_users = [user for user in User.query.order_by(User.tourney_score.desc()) if user.won_round]

	# deal with ties at the bottom
	if len(played_users) > 64 and played_users[64].tourney_score == played_users[65].tourney_score:
		tied_for_last = [user for user in played_users if user.tourney_score == played_users[64].tourney_score]

		# remove players whose score is lower than last place's
		advancing_users = [user for user in played_users if user.tourney_score > played_users[64].tourney_score]
		num_spots = 64 - len(played_users)

		advancing_users += random.sample(tied_for_last, num_spots)
	else:
		advancing_users = played_users[:64]

	# reset won_round and remove players from line that did not make it
	for user in played_users:
		user.won_round = 0

	# reset all tourney_positions
	User.query.update({"tourney_position": 0})

	# randomize tourney_position for advancing players
	positions = list(range(1, 65))
	for user in advancing_users:
		pos = random.choice(positions)
		user.tourney_position = pos
		positions.remove(pos)

	global tourney_round
	tourney_round += 1

	db.session.commit()

	return redirect(url_for('tourney'))


if __name__ == "__main__":
	app.run()
