import flask

app=flask.Flask(__name__)

@app.route("/")
def hello():
	return "Hello World"

@app.route("/say/<something>")
def say(something):
	return "say:"+str(something)

@app.route("/display")
def displayPage():
	try:
		f=open("index.html","rb")
		data=f.read()
		f.close()
		return data
	except Exception as e:
		return str(e)



if __name__=="__main__":
	app.run()