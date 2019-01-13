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
	sleep(1)
	if len(self._func):
		
		method_to_call = getattr(kern_adjust, self._func, self._data)
		result = method_to_call(self)
		clients[self._id]["thread_state"] = "null"
		yield str(result)
	#
	sleep(1)
	n = "done"
	# En_Value = clients[self._id]
	# clients.clear() 
	# clients[self._id] = En_Value
	yield n
	#
#
class FlaskThread(Thread):
	#
	def __init__(self, _id, _efo, _func, _data):
		self.delay = 1
		self._id = _id
		self._efo = _efo
		self._func = _func
		self._data = _data
		super(FlaskThread, self).__init__(name=_id)
	#
	def run_function_thread(self):
		#
		if clients[self._id]["thread_state"] not in ["ended", "aborted"]:
			#
			#number = round(random()*10, 3)
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
						socketio.emit('flask_message', {"text": "success_flask_thread_"+func_info+"_"+self._func, "thread_state": "active", "thread_id": self._id , "thread_data":x} , namespace='/test', room=self._id)
						socketio.emit('flask_message_log', {"text": "success_flask_thread_"+func_info+"_"+self._func+"_for_"+self._id, "thread_state": "active", "thread_id": self._id, "thread_data":x } , namespace='/test')
						#
					#
				else:
					#
					socketio.emit('flask_message', {"text": "success_flask_thread_finished", "thread_state": "ended", "thread_id": self._id }, namespace='/test', room=self._id)
					socketio.emit('flask_message_log', {"text": "success_flask_thread_finished_for_"+self._id, "thread_state": "null", "thread_id": self._id } , namespace='/test')
					#
					
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
	_data = dataDict["data"]
	_source_efo = dataDict["efo"]
	#
	message = ""
	_func = ""
	#
	#
	session['id'] = _id
	#
	#
	if _id in clients:
		#
		#

		if _tell == "abort":
			#
			status = 400
			thread_available = False
			#
			if clients[_id]["thread_state"] == "active":
				#
				clients[_id]["thread_state"] = "aborted" # abort! abort!
				#
				message = "warning_flask_thread_aborted"
				#
			else:
				#
				clients[_id]["thread_state"] = "null"
				#
				message = "warning_flask_thread_not_active"
				#
			#
		elif _tell in ["get_classes", "get_glif_width", "update_adjustments_json"]:
				
			#
			if clients[_id]["thread_state"] == "active":
				#
				status = 400
				message = "warning_flask_thread_exists"
				#
				thread_available = False
				#
			else:
				#
				#
				clients[_id]["thread_state"] = "active"
				#
				status = 200
				message = "activating_"+_tell
				#print(_source_efo)
				#
				thread_available = True
				#
				_func = _tell
				#
			#
			
		#
		if thread_available:
			#
			thread = FlaskThread(_id, _source_efo, _func, _data)
			thread.start()
			#

			#
		#
		response = app.response_class(response=message, status=status, mimetype='application/json')
		#
		return response
		#