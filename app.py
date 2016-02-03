from flask import Flask, redirect, render_template  
from flask.ext.bootstrap import Bootstrap
#this from the form
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, RadioField,IntegerField, SubmitField
from wtforms.validators import Required


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
	name = StringField('Store name', validators=[Required()]) 
	name = StringField('Type of house eg.massonate', validators=[Required()]) 
	name = StringField('', validators=[Required()]) 


	

app = Flask(__name__)

app.config['SECRET_KEY'] = 'ERTRYU76798'
bootstrap = Bootstrap(app)

@app.route('/')
def index():
	return render_template("Index.html")

@app.route('/signup')
def signUp():
	name = None
	form = signup()
	if form.validate_on_submit():
		name = form.name.data
		form.name.data = ''  
	return render_template("signup.html", form=form)

@app.route('/signin')
def signIn():
	name = None
	form = signin()
	if form.validate_on_submit():
		name = form.name.data
		form.name.data = ''
	return render_template('signin.html',form=form)




#run app
if __name__ == '__main__':
	app.run(debug=True)