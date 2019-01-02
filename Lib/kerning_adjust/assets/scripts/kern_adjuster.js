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
		//console.log("kern_adjuster")
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
		itm = $('.'+classes.glyph+_a);
		//
		a_width = parseInt($('.'+classes.glyph+_a).width());
		a_init_width = parseInt($('.'+classes.glyph+_a).attr("data-init-width"));
		//b_width = $('.'+classes.glyph+_b).width()
		//
		$('.'+classes.glyph+_a).find('i').css({"width":Math.abs(a_init_width - a_width), "right":-(Math.abs(a_init_width - a_width))});
		//
	}
	//
	function set_pair_kern_diff(glyph){
		//
		g_left = parseCeilInt(glyph.css("left"));
		//
		if (g_left == 0) {
			//
			g_left = parseCeilInt(glyph.css("margin-left"));
			//
		}
		//
		//console.log(g_left)
		//
		_neg = "diff_neg";
		_pos = "diff_pos";
		_b = glyph.find('b');
		_i = glyph.find('i');
		_i_prev = glyph.prev().find('i');
		//
		a_left = Math.abs(g_left);
		a_init_width = Math.abs(glyph.attr("data-init-width"));
		//
		if (g_left < 0) {
			//
			diff_class = _neg;
			//
			a_init_width = Math.abs(glyph.width() - Math.abs(a_left))
			//
		} else {
			//
			diff_class = _pos;
			//
			a_init_width = Math.abs(glyph.width()) - Math.abs( parseInt( _i_prev.width() ) );
			//
		}
		//
		//
		_b.removeClass(_pos);
		_b.removeClass(_neg);
		_b.addClass(diff_class);
		_b.css({"width":a_left, "right": a_init_width });
		//
	}
	//
	function fragmentFromString(strHTML) {
		//
		return document.createRange().createContextualFragment(strHTML);
		//
	}
	//
	function get_tex_size(txt, font) {
		//
        this.element = document.createElement('canvas');
        this.context = this.element.getContext("2d");
        this.context.font = font;
        return this.context.measureText(txt).width;
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
			//
			if (data.$fragment_map.length == 0) { // if we have a fragment_map dont place the elements again.
				//
				t.empty()
				//
				get_px_fontsize = undefined;
				//	
				for (var i = 0; i < a.length; i++) {
					//
					f_string = '<span class="'+classes.glyph_base+' '+classes.glyph+(i+1)+'" data-init-width="0">'+a[i]+kern_tag_now+kern_tag_alt+'</span>'
					//
					frag = fragmentFromString(f_string);
					//
					if (i == 0) {

						// append just one to get the em to pixel ratio
						f_w = $(f_string).hide().appendTo('.calc')//.width() // render width
						get_px_fontsize = parseFloat(getComputedStyle($(".calc span")[0]).fontSize)
						
					}
					//
					var f_w = get_tex_size(a[i], get_px_fontsize+"px AdventProVar");
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
				get_px_fontsize = parseFloat(getComputedStyle($(".sample .kern span")[0]).fontSize)
				//
				for (var i = 0; i < data.$fragment_map.length; i++) {
					//
					var e_w = get_tex_size(elem.text(), get_px_fontsize+"px AdventProVar"); // render width with canvas
					//var e_w = elem.clone().hide().appendTo('.calc').width() // render width by placing fragment in doc
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
				if (data.$fragment_map[i+1]) {
					//
					determine_pair_kerning(data.$fragment_map[i][0],data.$fragment_map[i+1][0])
					//
					elem = $('.'+classes.glyph+data.$fragment_map[i][0]);
					set_pair_kern_diff(elem);
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
			//console.log(inputs[i].value)
			//
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
		//
		var _t_l = parseCeilInt(_t.css("left"))
		//
		////console.log("transfer_t_m", _t_l)
		//
		_t.css({"left":0, "margin-left": _t_l })
		//
	}
	//
	function parseCeilInt(num){
		//
		return Math.ceil(parseFloat(num))
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
	//
	//
	//
	//
	//
	//
	//
	//
	//
	//
	//
	//
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
				$glyph: ''
			}, opts);
			//
			data.handleBounds = {};
			data.glyph_left = 0;
			//
			$kern_adjust.data(namespace, data)
			//
			document.querySelectorAll('.typeface:not(.loaded_kern)').forEach(function(li) {
				//
				li.className += ' loaded_kern';
				var sliders = '#' + li.id + ' input';
				var samples = '#' + li.id + ' .sample';
				//
				//console.log(sliders)
				//
				var inputs = document.querySelectorAll(sliders);
				var outputs = document.querySelectorAll(samples);
				//
				//console.log(inputs)
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
				$(data.$inputs[i]).on('input', function(){
					variable_axes(data) // dont do on input do change // now rendering with canvas instead of placing the object in dom
					//console.log($(this).val())
					arranger(data,data.$kern_adjust, ''); // could on input, but would be laggy because it takes time to get new initial widths
				}); // .on 'input' 
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
			//setTimeout(function(){
			
				$(".kern").unbind(events.move);

			//},100);
			//
		});
		//
		$("html").mouseleave(function() {
			//
			//setTimeout(function(){
			
				$(".kern").unbind(events.move);

			//},100);
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
		var oe = e.originalEvent,
			touch = (typeof oe.targetTouches !== "undefined") ? oe.targetTouches[0] : null,
			pageX = (touch) ? touch.pageX : e.clientX,
			pageY = (touch) ? touch.pageY : e.clientY;
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
		if (data.$glyph.prev().length == 0 ) { return; }
		// calculate bounds before moving
		data.d_right = parseCeilInt(data.$glyph.next().position().left) + parseCeilInt(data.$glyph.next().css("left")) - parseCeilInt(data.$glyph.position().left );
		data.d_left = parseCeilInt(data.$glyph.prev().position().left) - parseCeilInt(data.$glyph.prev().css("left")) - parseCeilInt(data.$glyph.position().left );
		//
		pos = parseCeilInt(pageX) - parseCeilInt(data.$glyph.position().left)
		//
		data.glyph_left = pos;
		//
		onStart(data, elem_glyph);
		//
	}
	//
	var _ratio = 0.5;
	//var direction = "";

	//var oldx = 0;
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
		//
		var pos = parseCeilInt(pageX) - parseCeilInt(data.glyph_left) - parseCeilInt(data.$glyph.position().left) + parseCeilInt(data.$glyph.css("left") )
		//
		var _pos = check_bounds(data, pos);
		//

		//
		//console.log(_pos, pos)
		//
		position(data, _pos);
		//
		set_pair_kern_diff(data.$glyph);
		//
	}
	//
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
		data.$glyph.next().css({"margin-left": parseCeilInt( data.$glyph.next().attr("data-original-margin")) })
		//
		transfer_to_margin(data.$glyph)
		//
		data.mouseStart = 0;
		//
	}
	//
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
