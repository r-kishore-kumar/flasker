from flask import Flask,render_template,flash
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
import mysql.connector
from datetime import datetime

conn=mysql.connector.connect(
	host='localhost',
	user='root',
	password='root',
	database='adduser'
	)


#create an instance
app=Flask(__name__)
app.config['SECRET_KEY']="This is my secret key that is something"

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
	cursor=conn.cursor()
	query="SELECT * FROM user_list"
	cursor.execute(query)
	return render_template('create_user.html',user=cursor,form=form)



if __name__=="__main__":
	app.run(debug=True)
