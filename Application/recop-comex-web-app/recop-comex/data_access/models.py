#Table specifications and simple queries goes here

from extensions import db

class audit_trail(db.Model):

	id = db.Column(db.INT, primary_key=True)
	user_id = db.Column(db.INT)
	affected_id = db.Column(db.INT, nullable=False)
	target_table = db.Column(db.VARCHAR(25), nullable=False)
	date_created = db.Column(db.DATETIME, nullable=False)
	type = db.Column(db.INT, nullable=False)

class beneficiary(db.Model):

	id = db.Column(db.INT, primary_key=True)
	donor_id = db.Column(db.INT)
	beneficiary_id = db.Column(db.INT)
	budget = db.Column(db.NUMERIC(10,2))
	status = db.Column(db.CHAR(1), nullable=False)

class donation(db.Model):

	id = db.Column(db.INT, primary_key=True)
	sponsee_id = db.Column(db.INT)
	sponsor_id = db.Column(db.INT)
	amount = db.Column(db.NUMERIC(10,2), nullable=False)
	date_given = db.Column(db.DATETIME, nullable=False)
	transaction_slip = db.Column(db.VARCHAR(200), nullable=False)
	is_event = db.Column(db.CHAR(1), nullable=False)
	status = db.Column(db.CHAR(1), nullable=False)

class event_attachment(db.Model):

	id = db.Column(db.INT, primary_key=True)
	event_id = db.Column(db.INT)
	path = db.Column(db.VARCHAR(200), nullable=False)
	type = db.Column(db.INT, nullable=False)

class event_category(db.Model):

	id = db.Column(db.INT, primary_key=True)
	name = db.Column(db.VARCHAR(20), nullable=False)
	description = db.Column(db.VARCHAR(30), nullable=False)

	def select():

		result = event_category.query.all()
		choice = ((row.id, row.name) for row in result)

		return choice

class event_information(db.Model):

	id = db.Column(db.INT, primary_key=True)
	organizer_id = db.Column(db.INT)
	category_id = db.Column(db.INT)
	name = db.Column(db.VARCHAR(30),nullable=False)
	description = db.Column(db.VARCHAR(140),nullable=False)
	objective = db.Column(db.VARCHAR(140),nullable=False)
	budget = db.Column(db.NUMERIC(10,2), nullable=False)
	location = db.Column(db.VARCHAR(50),nullable=False)
	event_date = db.Column(db.DATETIME, nullable=False)
	type = db.Column(db.INT, nullable=False)
	status = db.Column(db.CHAR(1), nullable=False)

	def count():

		rows = db.session.query(event_information).count()
		rows+=1
		return rows

	def add(value):

		record = event_information(
			id=value[0], 
			organizer_id=value[1], 
			category_id=value[2], 
			name=value[3], 
			description='event ko to',
			objective=value[4],
			budget = '1000.00',
			location=value[5],
			event_date=value[6],
			type=value[7],
			status=value[8]
			)
			 
		db.session.add(record)
		db.session.commit()

	def show(status):

		result = event_information.query.filter(event_information.status==status).first()

		return result.name

class event_participation(db.Model):

	id = db.Column(db.INT, primary_key=True)
	event_id = db.Column(db.INT)
	participant_id = db.Column(db.INT)
	rating = db.Column(db.INT, nullable=False)
	comment = db.Column(db.VARCHAR(140),nullable=False)
	is_target = db.Column(db.CHAR(1), nullable=False)
	status = db.Column(db.CHAR(1), nullable=False)

class event_resource(db.Model):

	id = db.Column(db.INT, primary_key=True)
	event_id = db.Column(db.INT)
	name = db.Column(db.VARCHAR(30), nullable=False)
	type = db.Column(db.INT, nullable=False)

class event_signatory(db.Model):

	id = db.Column(db.INT, primary_key=True)
	signatory_id = db.Column(db.INT)
	description = db.Column(db.VARCHAR(20),nullable=False)
	order = db.Column(db.INT, nullable=False)

class proposal_tracker(db.Model):

	id = db.Column(db.INT, primary_key=True)
	event_id = db.Column(db.INT)
	proposed_on = db.Column	(db.DATETIME, nullable=False)
	recop_accepted = db.Column(db.DATETIME)
	fmi_signed = db.Column(db.DATETIME)
	acad_signed = db.Column(db.DATETIME)
	approved_on = db.Column(db.DATETIME)
	comment = db.Column(db.VARCHAR(20))
	status = db.Column(db.CHAR(1), nullable=False)	

class referral(db.Model):

	id = db.Column(db.INT, primary_key=True)
	referrer_id = db.Column(db.INT)
	name = db.Column(db.VARCHAR(50),nullable=False)
	email_address = db.Column(db.VARCHAR(30),nullable=False)
	type = db.Column(db.INT, nullable=False)
	status = db.Column(db.CHAR(1), nullable=False)

class user_account(db.Model):

	id = db.Column(db.INT, primary_key=True)
	info_id = db.Column(db.INT)
	username = db.Column(db.VARCHAR(20),nullable=False)
	password = db.Column(db.VARCHAR(20),nullable=False)
	email_address = db.Column(db.VARCHAR(30),nullable=False)
	type = db.Column(db.INT, nullable=False)
	last_active = db.Column(db.DATETIME, nullable=False)
	status = db.Column(db.CHAR(1), nullable=False)

	def count():

		rows = db.session.query(user_account).count()
		rows+=1
		return rows

	def add(value_user_account):

		record = user_account(
			id=value_user_account[0], 
			info_id=value_user_account[1],
			username=value_user_account[2],
			password=value_user_account[3],
			email_address=value_user_account[4],
			type=value_user_account[5],
			last_active=value_user_account[6],
			status=value_user_account[7]
			)
			 
		db.session.add(record)
		db.session.commit()

class user_information(db.Model):

	id = db.Column(db.INT, primary_key=True)
	first_name = db.Column(db.VARCHAR(30),nullable=False)
	middle_name = db.Column(db.VARCHAR(20),nullable=False)
	last_name = db.Column(db.VARCHAR(20),nullable=False)
	company_name = db.Column(db.VARCHAR(50),nullable=False)
	gender = db.Column(db.CHAR(1), nullable=False)
	address = db.Column(db.VARCHAR(50),nullable=False)
	telephone = db.Column(db.VARCHAR(15))
	mobile_number = db.Column(db.VARCHAR(15))
	type = db.Column(db.INT, nullable=False)
	is_active = db.Column(db.CHAR(1), nullable=False)

	def count():

		rows = db.session.query(user_information).count()
		rows+=1
		return rows

	def add(value_user_information):

		record = user_information(
			id=value_user_information[0], 
			first_name=value_user_information[1],
			middle_name=value_user_information[2],
			last_name=value_user_information[3],
			company_name=value_user_information[4],
			gender=value_user_information[5],
			address=value_user_information[6],
			telephone=value_user_information[7],
			mobile_number=value_user_information[8],
			type=value_user_information[9],
			is_active=value_user_information[10]
			)
			 
		db.session.add(record)
		db.session.commit()