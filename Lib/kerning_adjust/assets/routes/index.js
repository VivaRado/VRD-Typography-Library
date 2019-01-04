//
module.exports = function(app, module_data) {
	//
	app.get('/', function (req, res) {
		//
		var data = {
			//
			layout: __root+'/assets/layouts/default',
			title: 'VRD TYPL Kerning Adjust',
			message: '',
			source_efo: module_data["source_efo"]
			//
		};
		//
		res.render(__root+'/assets/views/home', data);
		//
	});
	//
};
//