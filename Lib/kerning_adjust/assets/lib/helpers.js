'use strict';

var Handlebars = require('handlebars');

exports.option_data = function(data_one, value, data_two, label, selectedValue) {
	var selectedProperty = label == selectedValue ? 'selected="selected"' : '';
	return new Handlebars.SafeString('<option '+data_one+'="'+value+'" '+data_two+'="'+label+'" value="' + label + '"' +  selectedProperty + '>' + label + "</option>");
};

exports.option = function(value, label, selectedValue) {
	var selectedProperty = value == selectedValue ? 'selected="selected"' : '';
	return new Handlebars.SafeString('<option value="' + value + '"' +  selectedProperty + '>' + label + "</option>");
};

exports.ifCond = function(v1, operator, v2, options) {

	switch (operator) {
		case '==':
			return (v1 == v2) ? options.fn(this) : options.inverse(this);
		case '!=':
			return (v1 != v2) ? options.fn(this) : options.inverse(this);
		case '===':
			return (v1 === v2) ? options.fn(this) : options.inverse(this);
		case '<':
			return (v1 < v2) ? options.fn(this) : options.inverse(this);
		case '<=':
			return (v1 <= v2) ? options.fn(this) : options.inverse(this);
		case '>':
			return (v1 > v2) ? options.fn(this) : options.inverse(this);
		case '>=':
			return (v1 >= v2) ? options.fn(this) : options.inverse(this);
		case 'and':
			return (v1 && v2) ? options.fn(this) : options.inverse(this);
		case '||':
			return (v1 || v2) ? options.fn(this) : options.inverse(this);
		default:
			return options.inverse(this);
	}
};

exports.tojson = function(context) {
	return JSON.stringify(context);
};

exports.commalist = function(items, options) {
	var out = '';

	for(var i=0, l=items.length; i<l; i++) {
		out = out + options.fn(items[i]) + (i!==(l-1) ? ",":"");
	}
	return out;

};
//
function insert(str, index, value) {
    return str.substr(0, index) + value + str.substr(index);
}

exports.commasep = function(items, elem, options) {
	var out = '';

	for (var i = 0; i < items.length; i++) {

		it_final = ''

		if ( (items[i]).toString().length >= 1){
			var it_final = items[i]
		} else {
			var it_final = '~'
		}
		out = out + elem +it_final+insert(elem, 1, "/")
		
	};
	return new Handlebars.SafeString( out );

};

exports.ifIn = function(elem, list, options) {
	
	var string = elem,
	substrings = list.split(',');

	for (var i = 0; i < substrings.length; i++) {

		if(string.indexOf(substrings[i]) > -1) {
			return options.fn(this);
		}

	};
	return options.inverse(this);
};

exports.dynamictemplate = function(_partial, context, opts) {

	var template = Handlebars.partials[_partial],
	    fnTemplate = null;

	if (typeof template === 'function') {
	  fnTemplate = template;
	} else {
	  // Compile the partial
	  fnTemplate = Handlebars.compile(template);
	  // Register the compiled partial
	  Handlebars.registerPartial('templatename', fnTemplate);  
	}

	return fnTemplate(context);
    
};

Handlebars.unregisterHelper('commalist');
Handlebars.unregisterHelper('commasep');
Handlebars.unregisterHelper('tojson');
Handlebars.unregisterHelper('option');
Handlebars.unregisterHelper('option_data');
Handlebars.unregisterHelper('ifCond');
Handlebars.unregisterHelper('ifIn');

