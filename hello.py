from flask import Flask,render_template

#create an instance
app=Flask(__name__)
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



if __name__=="__main__":
	app.run(debug=True)
