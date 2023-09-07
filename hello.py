from flask import Flask,render_template,flash,request
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy 
import mysql.connector
from datetime import datetime



#create an instance
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'
# app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@localhost/our_users'
app.config['SECRET_KEY']="This is my secret key that is something"

db=SQLAlchemy(app)
#Update Data
@app.route('/update/<int:id>',methods=['POST','GET'])

def update(id):
	form=UserForm()
	name_to_update=Users.query.get_or_404(id)
	if request.method=="POST":
		name_to_update.name=request.form['name']
		name_to_update.email=request.form['email']
		try:
			db.session.commit()
			flash("User Updated Successfully!")
			return render_template("update.html",form=form,name_to_update=name_to_update)
		except:
			db.session.commit()
			flash("Error! Looks like there was a problem.... try again!")
			return render_template("update.html",form=form,name_to_update=name_to_update)
	else:
		return render_template("update.html",form=form,name_to_update=name_to_update)

#Create Model
class Users(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String(200),nullable=False)
	email=db.Column(db.String(120),nullable=False,unique=True)
	date_added=db.Column(db.DateTime,default=datetime.utcnow)

	def __repr__(self):
		return'<Name %r>' % self.name
	

#Create a Form Class
class NamerForm(FlaskForm):
	name=StringField("What's Your Name?",validators=[DataRequired()])
	submit=SubmitField("Submit")

class UserForm(FlaskForm):
	name=StringField("Name",validators=[DataRequired()])
	email=StringField("Email",validators=[DataRequired()])
	submit=SubmitField("Submit")


#create an route
@app.route('/home/<name>')

def index(name):
	return '<h1>Hello {}!</h1>'.format(name)

@app.route('/index')
def homepage():
	name='Kishore Kumar'
	Languages=['HTML','CSS','Python','C Programming','C++','MySQL','Flask']
	return render_template('index.html',name=name,Languages=Languages)

#Create Custom Error pages

@app.errorhandler(500)

def page_not_found(e):
	return render_template('500.html'),500

@app.errorhandler(404)

def page_not_found(e):
	return render_template('404.html'),404

@app.route('/name',methods=['GET','POST'])
def name():
	name=None
	form=NamerForm()
	#Validate Form
	if form.validate_on_submit():
		name=form.name.data
		form.name.data=''
		flash("Form Submitted Successfully !!")
	return render_template('name.html',name=name,form=form)

@app.route('/user/add',methods=['GET','POST'])
def add_user():
	name=None
	form=UserForm()
	if form.validate_on_submit():
		user=Users.query.filter_by(email=form.email.data).first()
		if user is None:
			user=Users(name=form.name.data,email=form.email.data)
			db.session.add(user)
			db.session.commit()
		name=form.name.data
		form.name.data=''
		form.email.data=''
		flash('User Added Successfully!!!')
	our_users=Users.query.order_by(Users.date_added)
	return render_template('create_user.html',form=form,name=name,our_users=our_users)



if __name__=="__main__":
	app.run(debug=True)
