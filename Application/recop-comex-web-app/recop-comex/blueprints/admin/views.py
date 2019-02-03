from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import current_user, login_required
from blueprints.admin.forms import *
from data_access.models import *
from data_access.queries import *
from static.email import generate, send_email

import os

admin = Blueprint('admin', __name__, template_folder="templates")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@admin.before_request
def before_request():

	if current_user.is_authenticated and not current_user.is_anonymous:

		if current_user.type == 2:
			return redirect(url_for('registered.index'))
		elif current_user.type == 3:
			return redirect(url_for('linkages.index'))
		elif current_user.type == 4:
			return redirect(url_for('communities.index'))

@admin.route('/admin')
@login_required
def index():

	return render_template('/admin/index.html', title="Home | Admin")

@admin.route('/admin/events/<status>/filter_<search>', methods=['GET', 'POST'])
@login_required
def events(status, search):

	if status=='scheduled':
		value='S'
	elif status=='new':
		value='N'
	elif status=='pending':
		value='P'
	elif status=='finished':
		value='F'
	else:
		value=status

	events = event_views.show_list(value, search)

	form = SearchForm()

	if form.validate_on_submit():

		return redirect(url_for('admin.events', status=status, search=form.search.data))

	return render_template('/admin/events/index.html', title="Events | Admin", form=form, events=events, status=status,search=search)

@admin.route('/admin/events/show/id=<id>')
@login_required
def event_show(id):

	event = event_views.show_info(id)

	return render_template('/admin/events/show.html', title= event.name.title() + " | Admin", event = event)

@admin.route('/admin/events/create')
@login_required
def events_create():

	return render_template('/admin/events/create.html' )

@admin.route('/admin/events/<action>/id=<id>')
@login_required
def event_action(id, action):

	event = event_information.retrieve_event(id)
	organizer = user_information.linkage_info(event.organizer_id)
	email = user_account.retrieve_user(organizer.id)

	if action=='approve':

		signatory = user_views.signatory_info(4)
		status = ['P','F']

		recipient = signatory.email_address
		user = 'Fr. ' + signatory.last_name
		token = generate(event.id)
		approve = url_for('unregistered.event_signing', token=token , action='approve', _external = True)
		decline = url_for('unregistered.event_signing', token=token , action='decline', _external = True)		
		html = render_template('admin/email/event.html', event=event , organizer=organizer.company_name, user=user, link = [approve, decline])
		subject = "NEW EVENT: " + event.name

		email_parts = [html, subject, current_user.email_address, recipient]

		send_email(email_parts)

		event_information.update_status(event.id,status[0])
		proposal_tracker.update_status(event.id,status[1])

		proposal = proposal_tracker.query.filter(proposal_tracker.event_id==event.id).first()

		audit_id = audit_trail.count()
		value = [audit_id,current_user.id,event.id,'event', 5]
		audit_trail.add(value)

		flash(event.name + ' was approved!', 'success')

	elif action=='decline':

		status='X'
		proposal_tracker.update_status(event.id, status)
		event_information.update_status(event.id, status)

		audit_id = audit_trail.count()
		value = [audit_id,user.id,event.id,'event', 6]
		audit_trail.add(value)

		flash(event.name + ' was declined.', 'info') 	


	return redirect(url_for('admin.events', status='all', search=' '))


@admin.route('/admin/linkages/<status>/filter_<search>', methods=['GET', 'POST'])
@login_required
def linkages(status, search):

	if status=='active':
		value='A'
	elif status=='new':
		value='N'
	elif status=='pending':
		value='P'
	elif status=='disabled':
		value='D'
	else:
		value=status

	linkages = linkage_views.show_list(value, 3, search=search)

	form = SearchForm()

	if form.validate_on_submit():

		return redirect(url_for('admin.linkages', status=status, search=form.search.data))

	return render_template('/admin/linkages/index.html', title="Linkages | Admin", form=form, linkages=linkages, status=status, search=search)

@admin.route('/admin/linkages/show/id=<id>')
@login_required
def linkage_show(id):

	linkage, mem_since = linkage_views.show_info(id)

	return render_template('/admin/linkages/show.html', title= linkage.company_name.title() + " | Admin", linkage=linkage, mem_since = mem_since)

@admin.route('/admin/linkages/action/id=<id>')
@login_required
def linkage_action(id):

	user = user_account.retrieve_user(id)
	linkage = user_information.linkage_info(user.info_id)

	if user.status == "A":
	
		status = "D"
		flash(linkage.company_name.title() + " was disabled!","success")

		audit_id = audit_trail.count()
		value = [audit_id,current_user.id,id,'linkage', 4]
		audit_trail.add(value)
	
	elif user.status== "D":
		
		status = "A"
		flash(linkage.company_name.title() + " was activated! ", "success")

		audit_id = audit_trail.count()
		value = [audit_id,current_user.id,id,'linkage', 3]
		audit_trail.add(value)

	else:
			
		token = generate(user.id)
		link = url_for('unregistered.confirm_linkage', token=token , _external = True)	
		html = render_template('admin/email/moa.html', user = user.username, link = link)
		subject = "MEMORANDUM OF AGREEMENT"

		email_parts = [html, subject, current_user.email_address, user.email_address]

		send_email(email_parts)
			
		flash('MOA was sent to ' + linkage.company_name.title(), 'success')

		status = "P"
			
		audit_id = audit_trail.count()
		value = [audit_id,current_user.id,id,'linkage', 1]
		audit_trail.add(value)

	user_account.update_status(id, status)

	return redirect(url_for('admin.linkages', status='all', search=' '))

@admin.route('/admin/linkages/create')
@login_required
def linkages_create():

	return render_template('/admin/linkages/create.html')

@admin.route('/admin/communities/<status>/filter_<search>')
@login_required
def communities(status, search):

	if status=='active':
		value='A'
	elif status=='new':
		value='N'
	elif status=='pending':
		value='P'
	elif status=='disabled':
		value='D'
	else:
		value=status

	communities = linkage_views.show_list(value, 4, search)


	return render_template('/admin/communities/index.html', title="Communities | Admin", communities=communities)

@admin.route('/admin/donations')
@login_required
def donations():

	return render_template('/admin/donations/index.html', title="Donations | Admin")

@admin.route('/admin/reports')
@login_required
def reports():

	return render_template('/admin/reports/index.html', title="Reports | Admin")

@admin.route('/admin/feedbacks')
@login_required
def feedbacks():

	return render_template('/admin/feedbacks/index.html', title="Feedbacks | Admin")

@admin.route('/admin/profile/about/<user>')
@login_required
def profile_about(user):

	admin = user_views.profile_info(current_user.info_id)

	return render_template('/admin/profile/about.html', title="Admin", admin=admin)

@admin.route('/admin/profile/eventsattended')
@login_required
def profile_eventsattended():

	return render_template('/admin/profile/eventsattended.html', title="Admin")	

@admin.route('/admin/profile/settings/personal', methods=['GET', 'POST'])
@login_required
def profile_settings_personal():

	user_information_update = user_information.profile_info_update(current_user.info_id)

	form = ProfilePersonalUpdateForm()

	if form.validate_on_submit():

		user_information_update.first_name = form.firstname.data
		user_information_update.middle_name = form.middlename.data
		user_information_update.last_name = form.lastname.data
		user_information_update.gender = form.gender.data
		user_information_update.birthday = form.birthday.data
		user_information_update.bio = form.bio.data

		db.session.commit()

		flash('Profile was successfully updated!', 'success')

		return redirect(url_for('admin.profile_settings_personal'))

	else:

		form.firstname.data = user_information_update.first_name
		form.middlename.data = user_information_update.middle_name
		form.lastname.data = user_information_update.last_name
		form.gender.data = user_information_update.gender
		form.birthday.data = user_information_update.birthday
		form.bio.data = user_information_update.bio

	return render_template('/admin/profile/settings/personal.html', title="Admin", form=form)

@admin.route('/admin/profile/settings/contact', methods=['GET', 'POST'])
@login_required
def profile_settings_contact():

	user_information_update = user_information.profile_info_update(current_user.info_id)
	user_account_update = user_account.profile_acc_update(current_user.info_id)

	form = ProfileContactUpdateForm()

	if form.validate_on_submit():

		user_information_update.address = form.address.data
		user_information_update.telephone = form.telephone.data
		user_information_update.mobile_number = form.mobile.data

		db.session.commit()

		user_account_update.email_address = form.email.data

		db.session.commit()

		flash('Profile was successfully updated!', 'success')

		return redirect(url_for('admin.profile_settings_contact'))

	else:

		form.address.data = user_information_update.address
		form.telephone.data = user_information_update.telephone
		form.mobile.data = user_information_update.mobile_number
		form.email.data = user_account_update.email_address

	return render_template('/admin/profile/settings/contact.html', title="Admin", form=form)	

@admin.route('/admin/profile/settings/username', methods=['GET', 'POST'])
@login_required
def profile_settings_username():

	user_account_update = user_account.profile_acc_update(current_user.info_id)

	form = ProfileUsernameUpdateForm()

	if form.validate_on_submit():

		user = user_account.login([current_user.username, form.oldpassword.data])

		if user:

			user_account_update.username = form.username.data

			db.session.commit()

			flash('Username was successfully updated!', 'success')

			return redirect(url_for('admin.profile_settings_username'))

		else:

			flash('Wrong password.', 'error')

	else:

		form.username.data = user_account_update.username

	return render_template('/admin/profile/settings/username.html', title="Admin", form=form)

@admin.route('/admin/profile/update/password', methods=['GET', 'POST'])
@login_required
def profile_settings_password():

	user_account_update = user_account.profile_acc_update(current_user.info_id)

	form = PasswordUpdateForm()

	if form.validate_on_submit():

		user = user_account.login([current_user.username, form.oldpassword.data])

		if user:

			user_account_update.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

			db.session.commit()

			flash('Password was successfully updated!', 'success')

			return redirect(url_for('admin.profile_settings_password'))

		else:

			flash('Wrong password.', 'error')

	return render_template('/admin/profile/settings/password.html', form=form)