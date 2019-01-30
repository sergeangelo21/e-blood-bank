from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, SelectField, DecimalField, DateField, RadioField
from wtforms.validators import DataRequired, EqualTo, ValidationError, NumberRange, Email

class ProposalForm(FlaskForm):
	title = StringField('Title of the Activity', validators=[DataRequired()])
	description = StringField('Description', validators=[DataRequired()])
	objective = StringField('Objective', validators=[DataRequired()])
	budget = StringField('Estimated Budget', validators=[DataRequired()])
	location = StringField('Venue', validators=[DataRequired()])
	event_date = StringField('Target Date', validators=[DataRequired()])
	thrust = SelectField('Thrust', choices = [("0","Please Choose One"),("1","Educational"),("2","Environmental"),("3","Health"),("4","Livelihood"),("5","Socio-Political"),("6","Spiritual")])
	submit = SubmitField('Submit')

class ProfileUpdateForm(FlaskForm):
    firstname = StringField('First Name')
    middlename = StringField('Middle Name')
    lastname = StringField('Last Name')
    gender = RadioField('Gender', choices=[("M","Male"),("F","Female")])
    birthday = DateField('Birthday')
    bio = StringField('Bio')
    company = StringField('Company Name')    
    address = StringField('Address')
    telephone = StringField('Telephone')
    mobile = StringField('Mobile Number')
    email = StringField('Email Address')
    username = StringField('Username')
    submit = SubmitField('Update')

class PasswordUpdateForm(FlaskForm):
    oldpassword = PasswordField('Old Password')
    password = PasswordField('Password')
    submit = SubmitField('Update')