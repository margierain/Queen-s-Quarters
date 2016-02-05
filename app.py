import os
from flask import Flask, redirect, render_template, url_for, send_from_directory, request, session  
from flask.ext.bootstrap import Bootstrap
#this from the form
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, RadioField,IntegerField, SubmitField, FileField
from wtforms.validators import Required
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import model
from model import db
from config import config
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config.from_object(config['default'])
app.config['SQLALCHEMY_DATABASE_URI'] =\
'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# db = SQLAlchemy(app)
bootstrap =Bootstrap(app)
#declare for the photoes... upload_folder is where the pictures will be stored
UPLOAD_FOLDER = 'UPloads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# photos = UploadSet('photos', IMAGES)


class signin(Form):
	email = StringField('Enter email',validators=[Required()])
	password = PasswordField('Enter password', validators=[Required()])
	submit = SubmitField('submit')



class signup(Form):
	name = StringField('Enter your name', validators=[Required()]) 
	email = StringField('Enter email',validators=[Required()])
	password = PasswordField(' password', validators= [Required()])
	submit = SubmitField('submit')



class adhouse(Form):
	name = StringField('Store name:', validators=[Required()]) 
	house = StringField('Type of house,eg mansionette', validators=[Required()]) 
	location = StringField('Location', validators=[Required()]) 
	bedrooms = StringField('No. of bedrooms', validators=[Required()])
	price = StringField('Price', validators= [Required()])
	uploadPhotoes = FileField('Upload photoes ',validators=[Required])
	submit = SubmitField('Create property')


# for serving the photoes.
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



@app.route('/', methods=['GET','POST'])
def index():
	# from model import 


	return render_template("Index.html")
 

@app.route('/signup', methods=['GET', 'POST'])
def signUp():
	name = None
	form = signup()
	if form.validate_on_submit():
		name = form.name.data
		email = form.email.data
		password = form.password.data

		user = model.User.query.filter_by(name=form.name.data).first()
		if user:
			# user exists
			return "User exists"
		else:
			# sign up user
			newUser = model.User(email=email, password=password, name=name)
			db.session.add(newUser)
			db.session.commit()
			form.name.data = ''  
			return "Successfully signed up!"
	return render_template("/signup.html",form=form, name=session.get('name'))



@app.route('/signin', methods=['GET', 'POST'])
def signIn():
	form = signin()
	if form.validate_on_submit():
		email = form.email.data
		password = form.password.data

		user = model.User.query.filter_by(email=form.email.data).first()
		if user:
			# log in
			logout_user()
			return "User exists", render_template("/adhouse.html")
		else:
			# redirect to sign up
			
			return render_template("/signup.html", form=form)
	


@app.route('/adhouse', methods=['GET', 'POST'])
def adHouse():
	form = adhouse()
	
	if request.method == 'POST':
		name = form.name.data
		houseType = form.house.data
		location = form.location.data
		bedrooms = form.bedrooms.data
		price = form.price.data
		import ipdb; ipdb.set_trace()

		house = model.House(name=name, houseType=houseType, location=location, bedrooms=bedrooms, price=price)
		db.session.add(house)
		db.session.commit()

		uploadPhotoes = form.uploadPhotoes.data
		file = uploadPhotoes
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			# return redirect(url_for('uploaded_file',filename=filename))
			return "Successfully uploaded photo"


		
	return render_template('adhouse.html',form=form)





#run app
if __name__ == '__main__':
	app.run(debug=True)