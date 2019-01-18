'use strict';
//
global.__root = __dirname
//
global.express = require('express');
global.exphbs  = require('express-handlebars');
//
var Handlebars = require('handlebars');
var fs = require('fs');
var path = require('path');
var bodyParser = require('body-parser');
//var session = require('express-session');
var helpers = require(__root+'/assets/lib/helpers');
var argv = require('minimist')(process.argv.slice(2));

var routes = require(__root+'/assets/routes');
//
var cors = require('cors');
//
var Flask = require(__root+"/assets/lib/start_flask");
//
if (argv.source) {
	//
	global.efo_source = argv.source
	//
	var app = express();
	//
	app.use(cors());
	//
	var port = 8008;
	//
	global.hbs = exphbs.create({
		defaultLayout: __root+'/app_modules/default/views/layouts/main',
		extname      : '.hbs',
		handlebars : Handlebars,
		helpers      : helpers,
		partialsDir: __root+'/assets/partials'
	});
	//
	app.engine('.hbs', hbs.engine);
	app.set('view engine', '.hbs');
	//
	app.disable('x-powered-by');
	//
	var _app_limit = '100mb';
	//
	app.use(bodyParser.json({limit: _app_limit}));
	app.use(bodyParser.urlencoded({limit: _app_limit, extended: true}));
	//
	app.use(express.static(__root+'/assets/public/'));
	//
	var server = require('http').createServer(app);
	var _io = require('socket.io')(server)
	_io.origins('*:*')
	//
	global.io = _io;
	//
	var module_data = {
		"source_efo": argv.source
	};
	//
	//
	app.io = _io;
	//
	server.listen(port, function () {
		console.log('VRD TYPL Kerning Adjust Server Port: '+port);
	});
	//
	app.io.on('connection', function(socket){
		//
		global.socket_id = socket.id;
		//
		socket.on('connect_error', function(e) {
			//
			console.log('connect_error')
			socket.reconnection(false);
			//
		});
		//
		socket.on('reconnect_error', function(e) {
			//
			console.log('reconnect_error')
			socket.reconnection(false);
			//
		});
		//
	});
	//
	//
	require( __root+'/'+'assets'+'/'+'routes'+'/'+'index' )(app, module_data)
	//
	console.log("STARTING FLASK")
	//
	var _flask = new Flask.Flask();
	_flask.start();
	//
} else {
	//
	console.log("Please Provide a Source EFO: --source '/font.EFO' ")
	//
}