'use strict';
//
global.__root = __dirname
//
global.express = require('express');
global.exphbs  = require('express-handlebars');
global.py = require('python-shell');
var Handlebars = require('handlebars');
var fs = require('fs');
var path = require('path');
var favicon = require('serve-favicon');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var session = require('express-session');
var helpers = require(__root+'/assets/lib/helpers');
var argv = require('minimist')(process.argv.slice(2));
var _io = require('socket.io')(server)
var routes = require(__root+'/assets/routes');
global.io = _io;
//
if (argv.source) {
	//
	console.log(argv.source)
	//
	var app = express();
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
	app.use(cookieParser());
	var _app_limit = '100mb';
	//
	app.use(bodyParser.json({limit: _app_limit}));
	app.use(bodyParser.urlencoded({limit: _app_limit, extended: true}));
	//
	app.use(express.static(__root+'/assets/public/'));
	//
	var server = require('http').createServer(app);
	//
	var module_data = {
		"source_efo": argv.source
	};
	//
	require( __root+'/'+'assets'+'/'+'routes'+'/'+'index' )(app, module_data)
	//
	app.io = _io;
	//
	server.listen(port, function () {
		console.log('VRD TYPL Kerning Adjust Server Port: '+port);
	});
	//
	app.io.on('connection', function(socket){
		//
		console.log('SOCKET app.js');
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
} else {
	//
	console.log("Please Provide a Source EFO: --source '/font.EFO' ")
	//
}