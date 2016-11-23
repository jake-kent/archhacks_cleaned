import re
from flask import session
from flask_wtf import Form
from wtforms.fields import TextField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import Required, Email, ValidationError
from models import db, User
from sqlalchemy import func

# test
class SignupForm(Form):
	firstname = TextField("First name", [Required("Please enter your first name.")])
	lastname = TextField("Last name", [Required("Please enter your last name.")])
	email = TextField("Email", [Required("Please enter your email address."),
						Email("Please enter your email address.")])
	school = TextField("School", [Required("Please enter your school.")])
	password = PasswordField('Password', [Required("Please enter a password.")])
	submit = SubmitField("Create account")

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def validate(self):
		if not Form.validate(self):
			return False

		user = User.query.filter_by(email=self.email.data.lower()).first()
		if user:
			self.email.errors.append("That email is already taken")
			return False
		else:
			return True


class SigninForm(Form):
	email = TextField("Email", [Required("Please enter your email address."), 
						Email("Please enter your email address.")])
	password = PasswordField('Password', [Required("Please enter a password.")])
	submit = SubmitField("Sign In")

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def validate(self):
		if not Form.validate(self):
			return False

		user = User.query.filter_by(email = self.email.data.lower()).first()
		if user and user.check_password(self.password.data):
			return True
		else:
			self.email.errors.append("Invalid e-mail or password")
			return False


class TourneyForm(Form):
	register = SubmitField("Register")
	unregister = SubmitField("Unregister")

	def reg_validate(self, user):
		if self.register.data:
			user = User.query.filter_by(email=user.email).first()
			if user.tourney_position:
				self.register.errors += "You are already registered.",
				return False
			else:
				# update database to register user
				last = db.session.query(func.max(User.tourney_position)).scalar()
				user.tourney_position = last + 1
				db.session.commit()
				return True
		return False

	def unreg_validate(self, user):
		if self.unregister.data:
			user = User.query.filter_by(email=user.email).first()
			if user.tourney_position:
				return True
			else:
				self.unregister.errors += "You are not registered.",
				return False
		return False

class ChangePassForm(Form):
	old_pass = PasswordField('Old Password', [Required("Please enter your old password.")])
	new_pass = PasswordField('New Password', [Required("Please enter your new password.")])

	submit = SubmitField("Change Password")

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def validate(self):
		if not Form.validate(self):
			return False
		user = User.query.filter_by(email = session['email']).first()
		if user and user.check_password(self.old_pass.data):
			return True
		else:
			self.old_pass.errors.append("Please check that you've entered your old password correctly.")
			return False


class ForgotPasswordForm(Form):
	email = TextField("Email", [Required("Please enter your email address."),
						Email("Please enter your email address.")])
	submit = SubmitField("Reset Password")

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def validate(self):
		if not Form.validate(self):
			return False
		return True

class ConfirmAttendanceForm(Form):
	attending = SubmitField("Mark Me as Attending")
	not_attending = SubmitField("Mark Me as Not Attending")

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def validate(self):
		if not Form.validate(self):
			return False
		return True

class TwitterHandleForm(Form):
	add = SubmitField("Add")
	edit = SubmitField("Edit")
	twitter_handle_field = TextField("Twitter Handle", [Required("Please enter your Twitter handle.")])

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def validate(self):
		twitter_regex = re.compile(r'@([A-Za-z0-9_]+)')
		if Form.validate(self) and twitter_regex.match(str(self.twitter_handle_field.data)):
			return True
		self.twitter_handle_field.errors.append("Please ensure that your Twitter handle is of the form @username")
		return False
