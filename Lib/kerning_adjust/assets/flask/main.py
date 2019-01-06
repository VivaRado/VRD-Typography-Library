from app import app, socketio
#from classes import *

if __name__ == "__main__":
	app.debug = True
	socketio.run(app, host="localhost", debug=True, use_reloader=True)