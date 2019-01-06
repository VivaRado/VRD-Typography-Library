//
const request = require('request-promise');
//
var _python_path_ = '/usr/bin/python3';
var _script_path_ = __root+'/assets/pyt';
//
module.exports = function(app, module_data) {
	//
	const py = require('python-shell');
	//
	app.get('/', function (req, res) {
		//
		var source_efo_filename = module_data["source_efo"].substring(module_data["source_efo"].lastIndexOf('/')+1);
		//
		var data = {
			//
			layout: __root+'/assets/layouts/default',
			title: 'VRD TYPL Kerning Adjust',
			message: '',
			source_efo: source_efo_filename
			//
		};
		//
		res.render(__root+'/assets/views/home', data);
		//
	});
	//
	app.post('/gather', function(req,res){
		//
		//  FLASK
		var data = {
			id: req.body.id
		}
	 	//
		var options = {
			method: 'POST',
			uri: 'http://localhost:5000',
			body: data,
			json: true,
			resolveWithFullResponse: true
		};
		//
		var returndata;
		//
		request(options).then(function (response) {
			//
			returndata = response.body;
			//
			if (response.statusCode == 200) {
				//
				message = "success_"+returndata
				//
			} else {
				//
				message = "error_"+returndata
				//
			}
			//
			res.status(response.statusCode).send( message )
			//
		}).catch(function (err) {
			//
			console.log(err);
			//
		});
		//
	});
	//
};
//