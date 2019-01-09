//
var py = require('python-shell');
var _python_path_ = '/usr/bin/python3';
var _script_path_ = __root+'/assets/flask';
//
exports.Flask = function(){
	//
	var options = {
		//
		//mode: 'json',
		pythonPath: _python_path_,
		//pythonOptions: ['-u'],
		scriptPath: _script_path_,
		//
	};
	//
	function start(argument) {
		//
		py.PythonShell.run('main.py', options, function (err, results) {
			//
			if(err){
				//
				console.log(['error_'+err]);
				//
			}
			//
		});
		//
	}
	this.start = start;
	//
}
