// kern_adjust: 0.001
(function ($, window) {
	//"use strict";

	var $window = $(window);

	var namespace = "kern_adjust",
		$body = null,
		classes = {
			base: "kern_adjust",
			content: "kern_adjust-content",
			bar: "kern_adjust-bar",
			track: "kern_adjust-track",
			handle: "kern_adjust-handle",
			isHorizontal: "kern_adjust-horizontal",
			isVertical: "kern_adjust-vertical",
			isSetup: "kern_adjust-setup",
			isActive: "kern_adjust-active"
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
					$kern_adjust.empty()
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
	//
	function determine_pair_kerning(_class, _a, _b) {
		//
		itm = $('.'+_class+_a)
		//
		a_width = $('.'+_class+_a).width()
		a_init_width = $('.'+_class+_a).attr("data-init-width")
		b_width = $('.'+_class+_b).width()
		//
		$('.'+_class+_a).find('i').css({"width":a_init_width - a_width, "right":-(a_init_width - a_width)})
		//
	}
	//
	function fragmentFromString(strHTML) {
		//
		return document.createRange().createContextualFragment(strHTML);
		//
	}
	//
	function injector(data, t, splitter, _class, after) {
		var a = data.$initial_text.split(splitter), inject = '';
		var classes = []
		var inject = ''
		if (a.length) {
			//
			if (data.$fragment_map.length == 0) { // if we have a fragment_map dont render the elements again.
				//
				t.empty()
				//
				for (var i = 0; i < a.length; i++) {
					//
					f_string = '<span class="'+_class+(i+1)+'" data-init-width="0">'+a[i]+'<i></i></span>'
					//
					frag = fragmentFromString(f_string);
					//
					f_w = $(f_string).hide().appendTo('.calc').width() // render width
					frag.firstChild.setAttribute("data-init-width", f_w)
					//
					data.$fragment_temp.appendChild(frag)
					//
					data.$fragment_map.push([i+1,f_w])
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
					elem = $('.'+_class+data.$fragment_map[i][0]);
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
					determine_pair_kerning(_class,data.$fragment_map[i][0],data.$fragment_map[i+1][0])
					//
				}
				//
			}
			//
		}
		//
	}
	//
	function doAxes(data) {
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
		if (opts.horizontal == true) {
			dims.push("horizontal");
		}
		if(opts.vertical == true) {
			dims.push("vertical")	
		}
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
				$fragment_map: []
			}, opts);
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
			injector(data,$kern_adjust, '', 'char', '');
			//
			console.log(data.$initial_text)
			//
			pub.reset.apply($kern_adjust);
			//
		}
		//
		interact(data)
		//
	}
	//
	function interact(data){
		//
		function var_sliders(data){
			var i, l;
			for (i=0, l=data.$inputs.length; i<l; i++) {
				$(data.$inputs[i]).on('input', function(){
					doAxes(data)
				});
				$(data.$inputs[i]).on('change', function(){
					doAxes(data) // dont do on input
					injector(data,data.$kern_adjust, '', 'char', ''); // could fo on input, but would be laggy because it takes time to get new widths
				}); // .on 'input' 
			}
		}
		//
		var_sliders(data)
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
