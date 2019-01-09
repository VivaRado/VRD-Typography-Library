from flask import Flask, Response, render_template, redirect, url_for, request, session, send_from_directory, jsonify, copy_current_request_context
from flask_session import Session
from flask_cors import CORS
from flask_socketio import SocketIO, join_room, leave_room
from threading import Thread, Event
from random import random
import json
import os
import sys
from time import sleep
from classes import kern_adjust
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
clients = {}
#
thread = Thread()
thread_stop_event = Event()
#
def generator(self):
	#
	n = "starting"
	yield n
	#
	if len(self._func):
		
		method_to_call = getattr(kern_adjust, self._func)
		result = method_to_call(self)
		yield str(result)
	#
	sleep(1)
	n = "done"
	yield n
	#
#
class FlaskThread(Thread):
	#
	def __init__(self, _id, _efo, _func):
		self.delay = 1
		self._id = _id
		self._efo = _efo
		self._func = _func
		super(FlaskThread, self).__init__(name=_id)
	#
	def run_function_thread(self):
		#
		if clients[self._id]["thread_state"] not in ["ended", "aborted"]:
			#
			number = round(random()*10, 3)
			res = generator(self)
			#
			for x in res:
				#
				if x != "done":
					#
					func_info = "starting"
					#
					if x != "starting":
						#
						socketio.emit('flask_message', {'number': number, "text": "success_flask_thread_"+func_info+"_"+self._func, "thread_state": "active", "thread_id": self._id , "thread_data":x} , namespace='/test', room=self._id)
						socketio.emit('flask_message_log', {'number': number, "text": "success_flask_thread_"+func_info+"_"+self._func+"_for_"+self._id, "thread_state": "active", "thread_id": self._id, "thread_data":x } , namespace='/test')
						#
					#
				else:
					#
					socketio.emit('flask_message', {'number': 0, "text": "success_flask_thread_finished", "thread_state": "ended", "thread_id": self._id }, namespace='/test', room=self._id)
					socketio.emit('flask_message_log', {'number': number, "text": "success_flask_thread_finished_for_"+self._id, "thread_state": "ended", "thread_id": self._id } , namespace='/test')
					#
					clients[self._id]["thread_state"] = "ended"
					#
				#
			#
		#
	def run(self):
		self.run_function_thread()
#
@app.route('/')
def index():
	#
	return render_template('flask_log.html')
#
@socketio.on('join', namespace='/test')
def on_join(data):
	#
	if data["room"] not in clients.keys():
		#
		clients[data["room"]] = {"thread_state":"null"}
		#
	#
	socketio.emit('flask_message_log', {"text":"success_flask_joined_"+data["room"], "thread_state": "standby", "thread_id": "null"}, namespace='/test')
	#
	join_room(data["room"], namespace='/test')
	#
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
	thread_available = False
	status = 400
	delay = 1
	data = request.data
	dataDict = json.loads(data)
	#
	_id = dataDict["id"]
	_tell = dataDict["tell"]
	_source_efo = ""
	message = ""
	_func = ""
	#
	session['id'] = _id
	#
	if _id in clients:
		#
		if _tell == "abort":
			#
			if clients[_id]["thread_state"] == "active":
				#
				clients[_id]["thread_state"] = "aborted" # abort! abort!
				#
				status = 200
				message = "warning_flask_thread_aborted"
				thread_available = False
				#
			else:
				#
				status = 400
				message = "warning_flask_thread_not_active"
				thread_available = False
				#
			#
		elif _tell == "get_classes":
			#
			_source_efo = dataDict["efo"]
			status = 200
			message = "getting_classes"
			#print(_source_efo)
			#
			thread_available = True
			#
			_func = _tell
			#
		elif _tell == "get_glif_width":
			#
			_source_efo = dataDict["efo"]
			status = 200
			message = "getting_glif_width"
			#print(_source_efo)
			#
			thread_available = True
			#
			_func = _tell
			#
		else:
			#
			if clients[_id]["thread_state"] == "active":
				#
				status = 400
				message = "error_flask_thread_exists"
				#
				thread_available = False
				#
			else:
				#
				clients[_id]["thread_state"] = "active"
				#
				request.sid = _id
				#
				status = 200
				message = "flask_thread_started"
				#
				thread_available = True
				#
			#
		#
		if thread_available:
			#
			thread = FlaskThread(_id, _source_efo, _func)
			thread.start()
			#
		#
		response = app.response_class(response=message, status=status, mimetype='application/json')
		#
		return response
		#