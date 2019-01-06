from flask import Flask, Response, render_template, redirect, url_for, request, session, send_from_directory, jsonify, copy_current_request_context
from flask_session import Session
from flask_cors import CORS
from flask_socketio import SocketIO, join_room, leave_room
from threading import Thread, Event
from random import random
import json
import os
from time import sleep
#
f_dir = os.path.dirname( __file__ )
template_dir = os.path.abspath(os.path.join(f_dir, '..', 'views'))
static_file_dir = os.path.abspath(os.path.join(f_dir, '..', 'public'))
print(static_file_dir)
app = Flask(__name__, static_folder=static_file_dir, template_folder=template_dir)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
cors = CORS(app, resources={r"localhost*": {"origins": "*"}})
Session(app)
socketio = SocketIO(app)
#
clients = []
#
thread = Thread()
thread_stop_event = Event()
#
def some_function(__id):
	#
	sleep(1)
	#
	return __id
	#
#
class FlaskThread(Thread):
	#
	def __init__(self, _id):
		self.delay = 1
		self._id = _id
		super(FlaskThread, self).__init__(name=_id)

	def interrupt(self):
		global thread
		thread.cancel()

	def randomNumberGenerator(self):
		#
		x = 0
		#
		while not thread_stop_event.isSet():
			#
			if x < 5:
				#
				number = round(random()*10, 3)
				#
				res = some_function(self._id)
				#
				socketio.emit('flask_message', {'number': number, "text": "success_flask_thread_counting", "thread_state": "active", "thread_id": self._id } , namespace='/test', room=self._id)
				socketio.emit('flask_message_log', {'number': number, "text": "success_flask_thread_counting_for_"+self._id, "thread_state": "active", "thread_id": self._id } , namespace='/test')
				#
			#
			if x == 5:
				#
				socketio.emit('flask_message', {'number': 0, "text": "success_flask_thread_finished", "thread_state": "ended", "thread_id": self._id }, namespace='/test', room=self._id)
				socketio.emit('flask_message_log', {'number': number, "text": "success_flask_thread_finished_for_"+self._id, "thread_state": "active", "thread_id": self._id } , namespace='/test')
				sleep(1)
				socketio.emit('flask_message', {'number': 0, "text": "error_flask_threading_interrupted", "thread_state": "ended", "thread_id": self._id }, namespace='/test', room=self._id)
				socketio.emit('flask_message_log', {'number': number, "text": "error_flask_threading_interrupted_for_"+self._id, "thread_state": "active", "thread_id": self._id } , namespace='/test')
				#
				#
				self.interrupt()
				#
			#
			x = x + 1
			#
		#
	def run(self):
		self.randomNumberGenerator()
#
@app.route('/')
def index():
	#
	return render_template('flask_log.html')
#
@socketio.on('join', namespace='/test')
def on_join(data):

	socketio.emit('flask_message_log', {"text":"success_flask_joined_"+data["room"], "thread_state": "standby", "thread_id": "null"}, namespace='/test')

	join_room(data["room"], namespace='/test')

@socketio.on('connect', namespace='/test')
def test_connect():
	#
	socketio.emit('flask_message_log', {"text":"success_flask_server_standby", "thread_state": "standby", "thread_id": "null"}, namespace='/test')
	#
#
@app.route('/', methods = ['POST'])
def postdata():
	global thread
	#
	data = []
	#
	print("CLIENTS",clients)
	#
	#
	status = 400
	delay = 1
	data = request.data
	dataDict = json.loads(data)
	#
	
	_id = dataDict["id"]
	session['id'] = _id
	#
	clients.append(session['id'])
	#
	request.sid = _id
	#
	thread = FlaskThread(_id)
	thread.start()
	status = 200
	message = "success_flask_thread_started"
	#
	response = app.response_class(response=message+'_'+session['id'], status=status, mimetype='application/json')
	#
	return response
	#