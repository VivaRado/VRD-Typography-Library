//
const request = require('request-promise');
//
var _python_path_ = '/usr/bin/python3';
//var _EFO = require(__root+'/assets/lib/efo_retrieve');
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
			source_efo: source_efo_filename,
			source_efo_dir: module_data["source_efo"]
			//
		};
		//
		res.render(__root+'/assets/views/home', data);
		//
	});
	//
	app.post('/thread', function(req,res){
		//
		/*if (req.body.tell == "get_classes") {
			//
			efo = new _EFO.EFO();
			efo.hello(module_data["source_efo"]);
			//*/
		//}
		//
		//  FLASK
		var send_data = {
			id: req.body.id,
			tell: req.body.tell,
			efo: module_data["source_efo"],
			data: req.body.data
		}
	 	//
		var options = {
			method: 'POST',
			uri: 'http://localhost:5000',
			body: send_data,
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
			res.status(err.statusCode).send( err.error )
			//
		});
		//
	});
	//
};
//