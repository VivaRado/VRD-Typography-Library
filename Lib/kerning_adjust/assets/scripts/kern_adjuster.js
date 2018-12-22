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
			//bar: "kern_adjust-bar",
			//track: "kern_adjust-track",
			handle: "kern_adjust-handle",
			//isHorizontal: "kern_adjust-horizontal",
			//isVertical: "kern_adjust-vertical",
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
		customClass: ""
	};
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

					data.$kern_adjust.off( classify(namespace) )
								  .removeData(namespace);
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
					//data.$kern_adjust.empty()
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
		console.log("kern_adjuster")
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
	//////
	function classify(text) {
		return "." + text;
	}
	//
	function determine_pair_kerning( _a, _b) {
		//
		itm = $('.'+classes.glyph+_a)
		//
		a_width = $('.'+classes.glyph+_a).width()
		a_init_width = $('.'+classes.glyph+_a).attr("data-init-width")
		b_width = $('.'+classes.glyph+_b).width()
		//
		$('.'+classes.glyph+_a).find('i').css({"width":a_init_width - a_width, "right":-(a_init_width - a_width)})
		//
	}
	//
	function fragmentFromString(strHTML) {
		//
		return document.createRange().createContextualFragment(strHTML);
		//
	}
	//
	function arranger(data, t, splitter) {
		//
		var a = data.$initial_text.split(splitter);
		//
		if (a.length) {
			//
			if (data.$fragment_map.length == 0) { // if we have a fragment_map dont render the elements again.
				//
				t.empty()
				//
				for (var i = 0; i < a.length; i++) {
					//
					f_string = '<span class="'+classes.glyph_base+' '+classes.glyph+(i+1)+'" data-init-width="0">'+a[i]+'<i></i></span>'
					//
					frag = fragmentFromString(f_string);
					//
					f_w = $(f_string).hide().appendTo('.calc').width() // render width
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
					elem = $('.'+classes.glyph+data.$fragment_map[i][0]);
					//
					e_w = elem.clone().hide().appendTo('.calc').width() // re render width
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
				if (data.$fragment_map[i+1]) {
					//
					determine_pair_kerning(data.$fragment_map[i][0],data.$fragment_map[i+1][0])
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
			axes[inputs[i].name] = inputs[i].value;
		}
		for (i in axes) {
			if (i.length === 4) {
				ffs.push('"' + i + '" ' + axes[i]);
			}
		}
		ffs = ffs.join(', ') || 'normal';
		
		for (i=0, l=outputs.length; i<l; i++) {
			outputs[i].style.fontVariationSettings = ffs;
		}
	}
	//
	function build($kern_adjust, opts) {
		//
		var dims = [];
		//
		//
		if (!$kern_adjust.hasClass(classes.base)) {
			// EXTEND OPTIONS
			opts = $.extend({}, opts, $kern_adjust.data(namespace + "-options"));
			//
			var html = '';
			//
			var data = $.extend({
				$kern_adjust: $kern_adjust,
				$initial_text: $kern_adjust.text(),
				$inputs:'',
				$outputs:'',
				$fragment_temp: document.createDocumentFragment(),
				$fragment_map: [],
				$handle: ''
			}, opts);
			//
			data.handleBounds = {};
			data.handleTop = 0;
			data.handleLeft = 0;
			//
			$kern_adjust.data(namespace, data)
			//
			document.querySelectorAll('.typeface:not(.loaded_kern)').forEach(function(li) {
				//
				console.log('#' + li.id + ' input', '#' + li.id + ' .sample')
				//
				li.className += ' loaded_kern';
				var sliders = '#' + li.id + ' input';
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
			console.log(data.$initial_text)
			//
			pub.reset.apply($kern_adjust);
			//
		}
		//
		variable_axes(data)
		arranger(data,data.$kern_adjust, '');
		//
		interact(data)
		//
	}
	//
	function interact(data){
		//
		function var_sliders(data){
			//
			var i, l;
			for (i=0, l=data.$inputs.length; i<l; i++) {
				$(data.$inputs[i]).on('input', function(){
					variable_axes(data)
				});
				$(data.$inputs[i]).on('change', function(){
					variable_axes(data) // dont do on input
					arranger(data,data.$kern_adjust, ''); // could on input, but would be laggy because it takes time to get new widths
				}); // .on 'input' 
			}
			//
		};
		//
		var_sliders(data);
		//
		for (var i = 0; i < data.$fragment_map.length; i++) {
			
			elem_glyph = $('.'+classes.glyph+data.$fragment_map[i][0]);

			elem_glyph.bind(events.start, classify(classes.handle+'-h'), function(e){
				//
				data.$handle = $(this);
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
		console.log('start')
		//
		//data.$content.off( classify(namespace) );
		//
		$('.kern').bind(events.move, function(e){
			//
			console.log("moving")
			//
			onMouseMove(data, e)
			//
		}).bind(events.end, function(e){
			//
			onMouseUp(data, e)
			//
		});
		//
	}
	//
	function findPos(obj) {
		var curleft = curtop = 0;
		if (obj.offsetParent) {
			do {
				curleft += obj.offsetLeft;
				curtop += obj.offsetTop;
			} while (obj = obj.offsetParent);
			return { x: curleft, y: curtop };
		}
	}
	//
	function onHandleDown(e, data) {
		//
		//elem_glyph = $(e.target)
		//
		e.preventDefault();
		e.stopPropagation();
		//
		console.log(data.$handle)
		//
		var oe = e.originalEvent,
			touch = (typeof oe.targetTouches !== "undefined") ? oe.targetTouches[0] : null,
			pageX = (touch) ? touch.pageX : e.clientX,
			pageY = (touch) ? touch.pageY : e.clientY;
		//
		var the_class = $(e.target).attr('class');
		var is_dim = the_class.substring(the_class.lastIndexOf("-") + 1);
		//
		//
		data.$handle.addClass('active_handle');
		//
		data.handleLeft = (pageX - data.$handle.position().left)
		//
		onStart(data, elem_glyph);
		//
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
			pageX = (touch) ? touch.pageX : e.clientX,
			pageY = (touch) ? touch.pageY : e.clientY;
		//
		data.mouseStart = e.clientX;
		//
		var pos = ( pageX - data.handleLeft - data.$handle.position().left ) + parseInt(data.$handle.css("left"))
		//
		position(data, pos);
		//
	}

	//
	function onMouseUp(data, e) {
		//
		e.preventDefault();
		e.stopPropagation();
		//
		data.$handle.removeClass('active_handle');
		//
		$(".kern").unbind(events.move);
		//
		data.mouseStart = 0;
		//
	}
	//
	//
	function position(data, pos) {
		//
		var check_bounds = function(_pos){
			//
			var has_bound = false;
			//
			//if (dim == 'h') {
				//
				//if (_pos < data.handleBounds.left) {
					//
					//var has_bound = true;
					//var new_pos = data.handleBounds.left;
					//
				//} else if (_pos > data.handleBounds.right) {
					//
				//	var has_bound = true;
				//	var new_pos = data.handleBounds.right;
					//
				//}
				//
			/*} else if (dim == 'v'){
				//
				if (_pos < data.handleBounds.top) {
					//
					var has_bound = true;
					var new_pos = data.handleBounds.top;
					//
				} else if (_pos > data.handleBounds.bottom) {
					//
					var has_bound = true;
					var new_pos = data.handleBounds.bottom;
					//
				}
				//
			}*/
			//
			if (has_bound) {
				//
				return new_pos;
				//
			} else {
				//
				return _pos;
				//
			}
			//
		};
		//
		var run_pos = function(pos){
			//
			var _direct = 'left';
			var h_num = 0;
			//
			var scroll_ammount = pos;// * _ratio;
			//
			var style_handle  = {};
			style_handle[_direct] = pos;
			//
			var style_content  = {};
			style_content[_direct] = scroll_ammount;
			//
			data.$handle.css(style_handle);
			//
		}
		//
		var pos = check_bounds(pos);
		run_pos(pos);
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
