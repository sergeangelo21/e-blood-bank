from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import login_user, logout_user, current_user, login_required
from blueprints.unregistered.forms import LoginForm, SignupForm
from data_access.models import user_account, user_information

from datetime import datetime

import os

unregistered = Blueprint('unregistered', __name__, template_folder="templates")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@unregistered.route('/')
def index():

	return render_template('/unregistered/index.html')

@unregistered.route('/events')
def events():

	return render_template('/unregistered/events.html')

@unregistered.route('/partners')
def partners():

	return render_template('/unregistered/partners.html')

@unregistered.route('/contactus')
def contactus():

	return render_template('/unregistered/contactus.html')

@unregistered.route('/signup', methods=['GET', 'POST'])
def signup():

	form = SignupForm()

	if form.validate_on_submit():
		id_user_account = user_account.count()
		id_user_information = user_information.count()

		value_user_information = [
			id_user_information,form.firstname.data,form.middlename.data,
			form.lastname.data,form.company.data,form.gender.data,
			form.address.data,form.telephone.data,form.mobile.data,form.type.data
			]
		user_information.add(value_user_information)

		if int(form.type.data) > 0:
			status = "D"
		else:
			status = "A"

		value_user_account = [
			id_user_account,id_user_information,form.username.data,
			form.password.data,form.email.data,1,datetime.utcnow(),status
			]
		user_account.add(value_user_account)


	return render_template('/unregistered/signup.html', form=form)

@unregistered.route('/login', methods=['GET', 'POST'])
def login():

	if current_user.is_authenticated and not current_user.is_anonymous:
		return redirect(url_for(''))

	form = LoginForm()

	if form.validate_on_submit():
        
		user = user_account.query.filter(user_account.username==form.username.data).first()

		if user is None or user.password!=form.password.data:

			flash('Invalid username or password')
			return redirect(url_for('unregistered.login'))

		login_user(user, remember=form.remember_me.data)

		if current_user.type == "1":
			return redirect(url_for(''))

		return redirect(url_for('registered.index'))

	return render_template('/unregistered/login.html', form=form)

@unregistered.route('/logout')
def logout():

	user_account.logout()

	logout_user()

	return redirect('/')