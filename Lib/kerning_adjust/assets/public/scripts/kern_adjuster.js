// kern_adjust: 0.001
(function ($, window) {
	//"use strict";

	var $window = $(window);

	var namespace = "kern_adjust",
		$body = null,
		classes = {
			base: "kern_adjust",
			content: "kern_adjust-content",
			glyph: "char",
			glyph_base: "glyph",
			handle: "kern_adjust-handle",
			isSetup: "kern_adjust-setup",
			isActive: "kern_adjust-active"
		},
		events = {
			start: "touchstart." + namespace + " mousedown." + namespace,
			move: "touchmove." + namespace + " mousemove." + namespace,
			end: "touchend." + namespace + " mouseup." + namespace
		};
	//
	var options = {
		customClass: "",
		class_kern_elem: "",
		kern_classes: "",
		glyphlib: "",
		glif_width: "",
		efo_name: "",
		masters:"",
		axes:"",
		kerning_obj: {}
	};
	//
	var rep_container = '<strong data-report="" class="report_container"></strong>';
	//
	var reports = {
		"kerning_none": {"class":"r_kerning_none", "title":"No Kerning Value", "initial":"🆚"},
		"class_none": {"class":"r_class_none", "title":"No Class Value", "initial":"🆑"}
	}
	//
	var pub = {
		//
		defaults: function(opts) {
			options = $.extend(options, opts || {});
			return (typeof this === 'object') ? $(this) : true;
		},
		//
		destroy: function() {
			return $(this).each(function(i, el) {
				var data = $(el).data(namespace);

				if (data) {
					data.$kern_adjust.removeClass( [data.customClass, classes.base, classes.isActive].join(" ") );

					data.$kern_adjust.off( classify(namespace) ).removeData(namespace);
				}
			});
		},
		//
		reset: function()  {
			//
			return $(this).each(function(i) {
				//
				var data = $(this).data(namespace);
				//
				if (data) {
					//
					data.$kern_adjust.addClass(classes.isSetup);
					//
					data.$kern_adjust.removeClass(classes.isSetup);
					//
				}
			});
		}
	};
	//
	function init(opts) {
		//
		// Local options
		opts = $.extend({}, options, opts || {});
		
		// Check for Body
		if ($body === null) {
			$body = $("body");
		}

		// Apply to each element
		var $items = $(this);
		for (var i = 0, count = $items.length; i < count; i++) {
			build($items.eq(i), opts);
		}
		//
		return $items;
	}
	//
	function classify(text) {
		return "." + text;
	}
	//
	function update_info_tags(el, add_t) {
		//
		el_t = el.attr("title");
		el_r = el.find("strong").attr("data-report");
		//
		t_parts = []
		r_parts = []
		//
		if (el_t.length > 0) {
			//
			t_parts = el_t.split(', ');
			//
		}
		//
		if (el_r.length > 0) {
			//
			r_parts = el_r.split(' ');
			//
		}
		//
		t_add = add_t["initial"]+' '+add_t["title"];
		r_add = add_t["initial"]
		//	
		if (t_parts.indexOf(t_add) == -1) {
			//
			t_parts.push(t_add);
			//
		}
		//
		if (r_parts.indexOf(r_add) == -1) {
			//
			r_parts.push(r_add);
			//
		}
		//
		f_t = t_parts.join(", ");
		f_r = r_parts.join(" ");
		//
		el.attr("title",f_t);
		el.find("strong").attr("data-report",f_r);
		//
	}
	//
	var _ommit_reports = ["	", "\n", "space", "sigma1"];
	//
	function make_reports(data) {
		//
		for (var i = 0; i < data.$fragment_map.length; i++) {
			//
			has_error = false;
			//
			t_class = '.'+classes.glyph+data.$fragment_map[i][0]
			//
			_elem = $(t_class);
			//
			_elem.removeClass("r_*")
			//
			_elem_glyph = _elem.attr("data-glyph")
			//
			if ( _ommit_reports.indexOf(_elem_glyph) == -1 ) {
				//
				el_kerning_val = _elem.find('i').width();
				el_class_val = _elem.attr("data-class");
				//
				if( (data.$fragment_map.length - 1) != i) { // dont show kerning fault on last element
					//
					if (el_kerning_val == 0) {
						//
						has_error = true;
						//
						_elem.addClass(reports["kerning_none"]["class"])
						//
						update_info_tags(_elem, reports["kerning_none"])
						//
						//
					}
					//
				}
				//
				if (el_class_val == "undefined") {
					//
					has_error = true;
					//
					_elem.addClass(reports["class_none"]["class"])
					//
					update_info_tags(_elem, reports["class_none"])
					//
				}

				//
				if (has_error == false) {

					_elem.addClass("r_clear")
					
				}
				//
			} 
			//
		}
		//
	}
	//
	function determine_pair_kerning( _a, _b) {
		//
		itm = $('.'+classes.glyph+_a);
		//
		if (itm.attr("data-glyph") == "space") {
			return
		}
		//
		a_width = parseInt($('.'+classes.glyph+_a).width());
		a_init_width = parseInt($('.'+classes.glyph+_a).attr("data-init-width"));
		//b_width = $('.'+classes.glyph+_b).width()
		//
		kerning_value = Math.abs(a_init_width - a_width);
		//
		elem = $('.'+classes.glyph+_a)
		elem.find('i').css({"width":kerning_value, "right":-(Math.abs(a_init_width - a_width))});
		//
	}
	//
	function set_pair_kern_diff(data, R_glyph, L_glyph, val){
		//
		//
		g_left = parseCeilInt(R_glyph.css("left"));
		//
		if (g_left == 0) {
			//
			g_left = parseCeilInt(R_glyph.css("margin-left"));
			//
		}
		//
		_neg = "diff_neg";
		_pos = "diff_pos";
		_b = R_glyph.find('b');
		_i = R_glyph.find('i');
		//
		if (L_glyph) {

			_i_prev = L_glyph.find('i');

		} else {

			_i_prev = R_glyph.prev().find('i');
			
		}
		//
		a_left = Math.abs(g_left);
		a_init_width = Math.abs(R_glyph.attr("data-init-width"));
		//
		if (g_left < 0) {
			//
			diff_class = _neg;
			//
			a_init_width = Math.abs(R_glyph.width() - Math.abs(a_left))
			//
		} else {
			//
			diff_class = _pos;
			//
			a_init_width = Math.abs(R_glyph.width()) - Math.abs( parseInt( _i_prev.width() ) );
			//
		}
		//
		//
		_b.removeClass(_pos);
		_b.removeClass(_neg);
		_b.addClass(diff_class);
		_b.css({"width":a_left, "right": a_init_width });
		//
	
		//
	}
	//
	function is_master(data){ // is master, current master
		//
		for (var key in data.masters) {
			//
			var obj = data.masters[key];
			//
			if ( parseInt(data.axes["wght"]) == obj[0]) {
				//
				if ( parseInt(data.axes["ital"]) == obj[1]) {
					//
					return [key, obj[0], obj[1]];
					//
				}
				//
			}
			//
		}
		//
		//
	}
	//
	function show_class_kerning_effect(data,_L, _L_sc, _R, _R_sc, _val){
		//
		var current_master = is_master(data)
		//
		_L_c = _L.attr(_L_sc);
		_R_c = _R.attr(_R_sc);
		//

		did_show = [];

		for (var i = 0; i < data.$fragment_map.length; i++) {
			//
			_R_elem = $(".kern span."+classes.glyph_base+'.'+classes.glyph+i)
			_L_elem = _R_elem.prev();
			//
			_L_is = _L_elem.attr(_L_sc);
			_R_is = _R_elem.attr(_R_sc);
			//
			if (_L_is == _L_c && _R_is == _R_c) {
				//
				run_kerning_adjustment(data, _L_elem, _R_elem, _val)
				//
			}
			//
		}
		//
	}
	//
	// maybe combine get_defined_sides with find_with_class
	//
	var find_with_class = function(_c){
			//
			_itm_G = $('[data-glyph="'+_c+'"]');
			//
			if ( _c.indexOf("@") != -1 ) {
				//
				c_L = _c.split("@_")[1];
				//
				_itm = $('[data-class="'+c_L+'"]');
				//
				_itm_L = $('[data-class-l="'+c_L+'"]');
				_itm_C = $('[data-class="'+c_L+'"]');
				_itm_R = $('[data-class-r="'+c_L+'"]');
				//
				if (_itm_C.length == 0) {

					if (_itm_L.length == 0) {
						//
						if (_itm_R.length == 0) {
							//
							_itm_c = [_itm_G, "data-glyph", "G"];
							//
						} else {
							//
							_itm_c = [_itm_R, "data-class-r", "R"];
							//
						}
						//
					} else {
						//
						_itm_c = [_itm_L, "data-class-l", "L"];
						//
					}
					//
				} else {
					//
					_itm_c = [_itm_C, "data-class", "C"];
					//
				}

			} else {

				_itm_c = [_itm_G, "data-glyph", "G"];

			}
			//
			//
			return _itm_c;
			//
		}
	//
	function get_defined_sides(data, _itm){
		//
		_itm_L = _itm.attr("data-class-l");
		_itm_C = _itm.attr("data-class");
		_itm_R = _itm.attr("data-class-r");
		//
		//
		if( data.class_kern_elem.is(':checked')){
			//
			if (_itm_C == "undefined") {

				if (_itm_L == "undefined") {
					//
					if (_itm_R == "undefined") {
						//
						_itm_c = [_itm.attr("data-glyph"), "data-glyph", "G"];
						//
					} else {
						//
						_itm_c = ["@_"+_itm_R, "data-class-r", "R"];
						//
					}
					//
				} else {
					//
					_itm_c = ["@_"+_itm_L, "data-class-l", "L"];
					//
				}
				//
			} else {
				//
				_itm_c = ["@_"+_itm_C, "data-class", "C"];
				//
			}
			//
		} else {
			//
			_itm_c = [_itm.attr("data-glyph"), "data-glyph", "G"];
			//
		}
		//
		return _itm_c;
		//
	}
	//
	function update_class_kerning(data, _L, _R){
		//
		data.kerning_obj = JSON.parse(localStorage.getItem(data.efo_name+'_kerning'))
		//
		//
		var current_master = is_master(data)
		//
		s_L_c = get_defined_sides(data, _L)
		s_R_c = get_defined_sides(data, _R)
		//
		//
		if (current_master) {
			//
			k_val = parseInt(_R.css("margin-left"))
			//
			R_name = s_R_c[0];
			R_attr = s_R_c[1];
			L_name = s_L_c[0];
			L_attr = s_L_c[1];
			//
			if (s_R_c[2] == "L") { // if Left Class Defined in Right Side Kerning Attempt
				//
				R_attr = "data-glyph";
				R_name = get_let(_R.attr(R_attr));
				//
			}
			//
			if (s_L_c[2] == "R") { // if Right Class Defined in Left Side Kerning Attempt
				//
				L_attr = "data-glyph";
				L_name = get_let(_L.attr(L_attr));
				//
			}
			//
			if( data.class_kern_elem.is(':checked')){
				//
				show_class_kerning_effect(data, _L, L_attr, _R, R_attr, k_val);
				//
			}
			//
			k_pair_name = L_name+' '+R_name;
			//
			if (k_val == 0) {
				//
				delete data.kerning_obj[current_master[0]][k_pair_name]
				//
			} else {
				//
				data.kerning_obj[current_master[0]][k_pair_name] = k_val * 10
				//
			}

		}
		//
		p(pprint( JSON.stringify(data.kerning_obj, undefined, 4) ),$('.serialize'));
		//
		localStorage.setItem( data.efo_name+'_kerning', JSON.stringify(data.kerning_obj))
		//
		data.kerning_obj = JSON.stringify(data.kerning_obj)
		//
	}
	//
	function fragmentFromString(strHTML) {
		//
		return document.createRange().createContextualFragment(strHTML);
		//
	}
	//
	function arrayColumn(arr, n) {
		return arr.map(x=> x[n]);
	}
	//
	function px2em(_px) {
		//
		var W = window,
			calc_ = $(".calc");
		//
		calc_.append('<span style="font-size:unset; width:auto; display:inline;">A</span>');
		elem = calc_[0]
		//
		var parentFontSize = parseInt(W.getComputedStyle(elem.parentNode, null).fontSize),
			elemFontSize = _px / 10;
		//
		var rem = parseFloat((elemFontSize / parseInt(parentFontSize, 10)) ).toPrecision(4) * 2
		//
		return rem
	}
	//
	function get_let(l){
		return l.substring(l.lastIndexOf("_") + 1);
	}
	//
	function get_class(data, letter){
		//
		found = [];
		cls = [];
		//	
		_cls_L = undefined;
		_cls_R = undefined;
		_cls_C = undefined;
		//
		for (var key in data.kern_classes) {
			//
			_obj = data.kern_classes[key];
			//
			if (arrayColumn(_obj, 2).indexOf(letter) != -1) {
				//
				found.push(key)
				//
			}
			//
		}
		//
		for (var i = 0; i < found.length; i++) {
			//
			dir = found[i].split('@MMK_').pop().split('_')[0];
			//
			//
			if (dir == "L") {
				//
				_cls_L = get_let(found[i])
				//
			}
			//
			if (dir == "R") {
				//
				_cls_R = get_let(found[i])
				//
			}
			//
		}
		//
		if (_cls_R == _cls_L) {
			//
			_cls_C = _cls_R
			//
		}
		//
		return [_cls_L, _cls_C, _cls_R]
		//
	}
	//
	function get_name(data, letter){
		//
		for (var key in data.glyphlib) {
			_obj = data.glyphlib[key];
			//
			for (var i = 0; i < _obj.length; i++) {
				//
				if (_obj[i][0] == letter) {
					//
					return key
					//
				}
				//
			}
		}
		//
	}
	//
	function get_initial_letter(data){
		//
		data.$kern_adjust.css({"font-size":px2em(data.glif_width)-0.6+'rem'}) // minus 0.6 because it is closer to the glif width value ?
		$(".calc").css({"font-size":px2em(data.glif_width)-0.6+'rem'})
		//
		initial_letter = "A"; // initial letter is set to "A" here and in flask
		//
		f_string = '<span class="calculator" data-glyph="'+initial_letter+'">'+initial_letter+'</span>'
		//
		$(f_string).hide().appendTo('.calc');
		f_w = parseInt($('.calc span').width());
		//
		return f_w
		//
	}
	//
	function isNumeric(value) {
		return /^-{0,1}\d+$/.test(value);
	}
	//
	function arranger(data, t, splitter) {
		//
		var kern_tag_now = '<i></i>';
		var kern_tag_alt = '<b></b>';
		//
		var a = data.$initial_text.split(splitter);
		//
		if (a.length) {
			//
			if (data.$fragment_map.length == 0) { // if we have a fragment_map dont place the elements again.
				//
				t.empty()
				//
				get_px_fontsize = undefined;
				//
				get_initial_letter(data);
				//
				for (var i = 0; i < a.length; i++) {
					//
					d_class = get_class(data, a[i]);
					//
					d_glyph = get_name(data, a[i]);
					//
					//
					f_string = '<span '+
									'title="" '+
									'class="'+classes.glyph_base+' '+classes.glyph+(i+1)+'" '+
									'data-init-width="0" '+
									'data-glyph="'+d_glyph+'" '+
									'data-class="'+d_class[1]+'"'+
									'data-class-l="'+d_class[0]+'"'+
									'data-class-r="'+d_class[2]+'">'+
										a[i]+
										kern_tag_now+
										kern_tag_alt+
										rep_container+
								'</span>'
					//
					frag = fragmentFromString(f_string);
					//
					var f_w = $('.calc').children().eq(i).width();
					//
					frag.firstChild.setAttribute("data-init-width", f_w)
					//
					data.$fragment_temp.appendChild(frag)
					//
					data.$fragment_map.push([i+1,f_w,0,0])
					//
				}
				//
				$('.calc').empty()
				//
				t.append(data.$fragment_temp)
				//
			} else { // just re render without kerning and get their widths
				//
				for (var i = 0; i < data.$fragment_map.length; i++) {
					//
					elem = $(".kern span."+classes.glyph_base+'.'+classes.glyph+i)
					var e_w = elem.clone().hide().appendTo('.calc').width();
					//
					elem.attr("data-init-width", e_w)
					//
					data.$fragment_map[i][1] = e_w
					//
				}
				//
				$('.calc').empty()
				//
			}
			//
			for (var i = 0; i < data.$fragment_map.length; i++) {
				//
				//
				if (data.$fragment_map[i+1]) {
					//
					t_class = '.'+classes.glyph+data.$fragment_map[i][0]
					//
					_elem = $(t_class);
					//
					_L = data.$fragment_map[i][0]
					_R = data.$fragment_map[i+1][0]
					//
					determine_pair_kerning(_L,_R)
					//
					set_pair_kern_diff(data, elem);
					//
				}
				//
			}
			//
		}
		//
	}
	//
	function variable_axes(data) {
		//
		inputs = data.$inputs
		outputs = data.$outputs
		//
		var i, l, axes = {}, ffs = [];
		for (i=0, l=inputs.length; i<l; i++) {
			//
			axes[inputs[i].name] = inputs[i].value;
			//
		}
		for (i in axes) {
			if (i.length === 4) {
				ffs.push('"' + i + '" ' + axes[i]);
			}
		}
		//
		ffs = ffs.join(', ') || 'normal';
		//
		data.axes = axes;
		//
		for (i=0, l=outputs.length; i<l; i++) {
			outputs[i].style.fontVariationSettings = ffs;
		}
	}
	//
	function transfer_to_left(_t){
		//
		var _t_l = parseCeilInt(_t.css("margin-left"))
		//
		_t.css({"left":_t_l, "margin-left": 0 })
		//
	}
	//
	function transfer_to_margin(_t){
		//
		var _t_l = parseCeilInt(_t.css("left"))
		//
		_t.css({"left":0, "margin-left": _t_l })
		//
	}
	//
	function parseCeilInt(num){
		//
		return Math.floor(parseFloat(num))
		//
	}
	//
	function check_bounds(data,_pos){
		//
		var has_bound = false;
		//
		var new_pos = _pos;
		//
		if (data.d_left > _pos) {
			//
			has_bound = true;
			new_pos = data.d_left
			//
		} else if ( _pos > data.d_right ) {
			//
			has_bound = true;
			new_pos = data.d_right
			//
		}
		//
		return new_pos;
		//
	};
	//
	function make_empty_kerning_master(data){
		//
		_masters = data.masters
		//
		var kern_master =JSON.parse(JSON.stringify(_masters))
		//
		for (var key in kern_master) {
			//
			kern_master[key] = {};
			//
		}
		//
		data.kern_master = kern_master;
		//
		return kern_master
		//
	}
	//	
	function build($kern_adjust, opts) {
		//
		var dims = [];
		//
		this.onSlideEnd = opts.onSlideEnd;
		//
		if (!$kern_adjust.hasClass(classes.base)) {
			// EXTEND OPTIONS
			opts = $.extend({}, opts, $kern_adjust.data(namespace + "-options"));
			//
			var html = '';
			//
			//
			var data = $.extend({
				$kern_adjust: $kern_adjust,
				$initial_text: $kern_adjust.text(),
				$inputs:'',
				$outputs:'',
				$fragment_temp: document.createDocumentFragment(),
				$fragment_map: [],
				$glyph: ''
			}, opts);
			//
			k_object = localStorage.getItem(data.efo_name+'_kerning');
			//
			data.kerning_obj = k_object
			//
			if (!k_object) {
				//
				localStorage.setItem( data.efo_name+'_kerning', JSON.stringify(make_empty_kerning_master(data)))
				//
			}
			//
			p(pprint( JSON.stringify(JSON.parse(localStorage.getItem(data.efo_name+'_kerning')), undefined, 4) ),$('.serialize'));
			//
			data.handleBounds = {};
			data.glyph_left = 0;
			//
			$kern_adjust.data(namespace, data)
			//
			document.querySelectorAll('.typeface:not(.loaded_kern)').forEach(function(li) {
				//
				li.className += ' loaded_kern';
				var sliders = '#' + li.id + ' input[data-typeface]';
				var samples = '#' + li.id + ' .sample';
				//
				var inputs = document.querySelectorAll(sliders);
				var outputs = document.querySelectorAll(samples);
				//
				data.$inputs = inputs;
				data.$outputs = outputs;
				//
			});
			//
			arranger(data,$kern_adjust, '');
			//
			pub.reset.apply($kern_adjust);
			//
		}
		//
		variable_axes(data);
		arranger(data,data.$kern_adjust, '');
		//
		interact(data);
		//
		assign_kerning_acord(data);
		//
		make_reports(data);
		//
	}
	//
	function isEmptyObject(obj) {
		for(var prop in obj) {
			if (Object.prototype.hasOwnProperty.call(obj, prop)) {
				return false;
			}
		}
		return true;
	}
	//
	function assign_kerning_acord(data){
		//
		data.kerning_obj = JSON.parse(localStorage.getItem(data.efo_name+'_kerning'))
		//
		

		var reset_kern_view_guides = function() {
			//
			for (var i = 0; i < data.$fragment_map.length; i++) {
				//
				_R_elem = $(".kern span."+classes.glyph_base+'.'+classes.glyph+i)
				_L_elem = _R_elem.prev();
				//
				_L_elem.find("b").removeAttr("style");
				//
				run_kerning_adjustment(data, _L_elem, _R_elem, 0)
				//
			}
		}
		//

		//
		//
		var current_master = is_master(data);
		//
		reset_kern_view_guides();
		//
		if (current_master) {
			//
			k_current = data.kerning_obj[current_master[0]];
			//
			if (isEmptyObject(k_current) == false) {
				//
				//
				for (k in k_current){
					//
					c_split = k.split(" ");
					//
					//
					ac_L = c_split[0]
					ac_R = c_split[1]
					//
					t_L = find_with_class(ac_L);
					t_R = find_with_class(ac_R);
					//
					L_attr = t_L[1];
					R_attr = t_R[1];
					//
					/*if (t_R[2] == "L") { // if Left Class Defined in Right Side Kerning Attempt
						//
						R_attr = "data-glyph";
						//R_name = get_let(_R.attr(R_attr));
						//
					}
					//
					if (t_L[2] == "R") { // if Right Class Defined in Left Side Kerning Attempt
						//
						L_attr = "data-glyph";
						//L_name = get_let(_L.attr(L_attr));
						//
					}*/
					//console.log(t_L[0], L_attr,t_R[0], R_attr)
					//
					show_class_kerning_effect(data,t_L[0], L_attr,t_R[0], R_attr, k_current[k] / 10);
					//
				}
				//
			} else {
				reset_kern_view_guides();
			}
			//
		}
		//
	}
	//
	function interact(data){
		//
		function var_sliders(data){
			//
			var i, l;
			for (i=0, l=data.$inputs.length; i<l; i++) {
				//
				$(data.$inputs[i]).on('change', function(){
					//
					variable_axes(data);
					//
					arranger(data,data.$kern_adjust, '');
					//
					assign_kerning_acord(data);
					//
					make_reports(data);
					//
				});
				//
			}
			//
		};
		//
		var_sliders(data);
		//
		for (var i = 0; i < data.$fragment_map.length; i++) {
			//
			elem_glyph = $('.'+classes.glyph+data.$fragment_map[i][0]);
			//
			elem_glyph.bind(events.start, classify(classes.handle+'-h'), function(e){
				//
				data.$glyph = $(this);
				//
				onHandleDown(e,data)
				//
			});
			//
		};
		//
	}
	//
	function onStart(data) {
		//
		$(".kern").unbind(events.move);
		$(".kern").unbind(events.end);
		//
		$('.kern').bind(events.move, function(e){
			//
			onMouseMove(data, e)
			//
		}).bind(events.end, function(e){
			//
			onMouseUp(data, e)
			//
		});
		//
		$('.fonts').mouseleave(function() {
			//
			$(".kern").unbind(events.move);
			//
		});
		//
		$("html").mouseleave(function() {
			//
			$(".kern").unbind(events.move);
			//
		});
		//
	}
	//
	function onHandleDown(e, data) {
		//
		e.preventDefault();
		e.stopPropagation();
		//
		has_prev = data.$glyph.prev().length
		has_next = data.$glyph.next().length
		//
		var this_pos_top = data.$glyph.position().top;
		var prev_pos_top = data.$glyph.prev().position().top;
		var next_pos_top = prev_pos_top;
		//
		if (has_prev > 0) {
			//
			if (has_next > 0) {
				//
				var next_pos_top = data.$glyph.next().position().top;
				//
			}
			//
			if (this_pos_top != next_pos_top) { return; } // avoid last letter in each line miscalculation
			if (this_pos_top != prev_pos_top) { return; } // avoid first letter in each line miscalculation
			if (data.$glyph.prev().length == 0 ) { return; } // avoid first letter miscalculation // sorry you will have to resize the window.
			//
			var oe = e.originalEvent,
				touch = (typeof oe.targetTouches !== "undefined") ? oe.targetTouches[0] : null,
				pageX = (touch) ? touch.pageX : e.clientX;
			//
			var the_class = $(e.target).attr('class');
			var is_dim = the_class.substring(the_class.lastIndexOf("-") + 1);
			//
			data.$glyph.next().attr("data-original-margin", parseCeilInt(data.$glyph.next().css("margin-left")))
			data.$glyph.next().css({"margin-left": parseCeilInt(data.$glyph.css("margin-left")) + parseCeilInt(data.$glyph.next().attr("data-original-margin")) })
			//
			transfer_to_left(data.$glyph)
			//
			data.$glyph.addClass('active_handle');
			//
			// calculate bounds before moving
			if (has_next > 0) {
				data.d_right = parseCeilInt(data.$glyph.next().position().left) + parseCeilInt(data.$glyph.next().css("left")) - parseCeilInt(data.$glyph.position().left );
			}
			data.d_left = parseCeilInt(data.$glyph.prev().position().left) - parseCeilInt(data.$glyph.prev().css("left")) - parseCeilInt(data.$glyph.position().left );
			//
			pos = parseCeilInt(pageX) - parseCeilInt(data.$glyph.position().left)
			//
			data.glyph_left = pos;
			//
			onStart(data, elem_glyph);
			//
		}
		
	}
	//
	var _ratio = 0.5;
	//
	function onMouseMove(data, e) {
		//
		e.preventDefault();
		e.stopPropagation();
		//
		var oe = e.originalEvent,
			touch = (typeof oe.targetTouches !== "undefined") ? oe.targetTouches[0] : null,
			pageX = (touch) ? touch.pageX : e.clientX;
		//
		data.mouseStart = e.clientX;
		//
		var pos = parseCeilInt(pageX) - parseCeilInt(data.glyph_left) - parseCeilInt(data.$glyph.position().left) + parseCeilInt(data.$glyph.css("left") )
		//
		var _pos = check_bounds(data, pos);
		//
		position(data, _pos);
		//
		set_pair_kern_diff(data,data.$glyph);
		//
	}
	//
	function run_kerning_adjustment(data, _L,_R, val) {
		//
		if (val) {
			//
			_R.css({"margin-left": val })
			_R.find("b").css({"width": Math.abs(val) })
			//
			set_pair_kern_diff(data,_R);
			//
		} else {
			//
			_R.css({"margin-left": parseCeilInt( _R.attr("data-original-margin")) })
			//
			transfer_to_margin(_L)
			//
		}
		//
	}
	//
	function onMouseUp(data, e) {
		//
		e.preventDefault();
		e.stopPropagation();
		//
		data.$glyph.removeClass('active_handle');
		//
		$(".kern").unbind(events.move);
		$(".kern").unbind(events.end);
		//
		run_kerning_adjustment(data, data.$glyph, data.$glyph.next())
		//
		data.mouseStart = 0;
		//
		update_class_kerning(data, data.$glyph.prev(),data.$glyph)
		//
		if (this.onSlideEnd && typeof this.onSlideEnd === 'function') {
			//
			k_object = JSON.parse(localStorage.getItem(data.efo_name+'_kerning'));
			data.kerning_obj = k_object
			//
            this.onSlideEnd(k_object);
            //
        }
	}
	//
	function position(data, pos) {
		//
		var _direct = 'left';
		//
		var style_handle  = {};
		style_handle[_direct] = pos;
		//
		data.$glyph.css(style_handle);
		//
	}
	//
	$.fn[namespace] = function(method, callback) {
		//
		if (pub[method]) {
			//
			pub[method].apply(this, Array.prototype.slice.call(arguments, 1));
			//
		} else if (typeof method === 'object' || !method) {
			//
			init.apply(this, arguments);
			//
		}
		//
		if (typeof callback == 'function') {
			//
			return callback('ok');
			//
		} 
		//
	};
	//
})( jQuery, window, document );

$(window).resize(function(){
	
	$(".kern_adjust").kern_adjust("reset");

});
