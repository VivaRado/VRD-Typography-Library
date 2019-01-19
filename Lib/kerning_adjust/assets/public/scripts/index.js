//
function display_alert(alert_text, target_container, animation){
	//
	if (alert_text) {
		//
		var alert_text = alert_text.toString();
		var target_alert = target_container;
		//
		alert_class = alert_text.substring(alert_text.indexOf('_'),0);
		display_data = toTitleCase(alert_text.substring(alert_text.indexOf('_')+1).toString().replace(/_/g,' '), true)
		//
		//
		if(animation == 'appended'){
			//
			if(target_alert.children('ul').length == 0){
				
				target_alert.append('<ul></ul>');

			}
			//
			target_alert.find('ul').append('<li class="'+alert_class+'">'+display_data+'</li>');
			target_alert.removeClass('hide').addClass('active_alert').show();
			//
		} else {
			//
			target_alert.empty();
			target_alert.append('<ul></ul>');
			target_alert.find('ul').append('<li class="'+alert_class+'">'+display_data+'</li>');
			target_alert.removeClass('hide').addClass('active_alert').show();
			//
		}
		//
		if(animation != 'static'){
			//
			anim_type = setTimeout(function(){
				//
				target_alert.hide().removeClass('active_alert').addClass('hide');
				target_alert.empty();
				//
				if(animation == 'static'){

					clearTimeout(anim_type)
					anim_type = null;
				}
				//
			},3000);
			//
		}
	}
}
//
function toTitleCase(str,_style) {
	//
	if (_style) {
		//
		delim = "| ";
		//
		var _articles = ["by","and","the","an","is"]; // "a" omited
		var _conjunctions = ["and", "but", "or", "for", "nor"];
		//
		var _prep_space_place = ["above","across","along","among","away","behind","below","beside","between","next"];
		var _prep_space_position = ["beyond","down","from","in","front","inside","near","off"];
		var _prep_space_direction = ["into","on","opposite","out","outside","over","around","through","to","toward","under","up"];
		var _prep_time = ["after","before","at","during"];
		var _prep_other = ["of","against","except","as","like","about","with","without"];
		//
		var _prepositions = [].concat(_prep_space_place, _prep_space_position, _prep_space_direction, _prep_time, _prep_other);
		//
		var all_words = [].concat(_articles, _conjunctions, _prepositions).join(delim);
		//
		var re = new RegExp("(?! "+all_words+")(?:^|\\s)\\w", "g");
		//
		return str.replace(re, function(match) {
			return match.toUpperCase();
		});
		//
	} else {
		//
		return str.replace(/(?:^|\s)\w/g, function(match) {
			return match.toUpperCase();
		});
		//
	}
	//
}
//
var socket_ids = {};
//
var got = {}
got.got_a = false;
got.got_b = false;
//got.got_c = false;
//
$(document).ready(function() {
	//
	get_data_timer = setInterval(data_timer, 1000);
	//
	init_socket = function(callback){
		//
		var socket_node = io.connect('http://localhost:8008');
		var socket_flask = io.connect('http://localhost:5000/test');
		//
		socket_node.on('connect', function () { 
			//
			console.log('SOCKET CONNECTED NODEJS')
			display_alert("success_nodejs_socket_connected", $(".display_alert"), "static")
			//
			//
			socket_node.on('disconnected', function() {
				//
				console.log('SOCKET DISCONNECTED NODEJS')
				//
			});
			//
			socket_ids.socket_node_id = socket_node.id;
			//
		});
		//
		socket_node.on('message',function(log){
			//
			display_alert(log, $(".display_alert"), "static")
			//
		});
		//
		socket_flask.on('connect', function () { 
			//
			console.log('SOCKET CONNECTED FLASK')
			display_alert("success_flask_socket_connected", $(".display_alert"), "static")
			//
			socket_flask.on('disconnected', function() {
				//
				console.log('SOCKET DISCONNECTED FLASK')
				//
			});
			//
			socket_ids.socket_flask_id = socket_flask.id;
			//
			socket_flask.emit('join', {room: socket_ids.socket_node_id});
			//
		});
		//
		var numbers_received = [];
		//
		socket_flask.on('flask_message', function(msg) {
			//
			if (msg.thread_state == "aborted" || msg.thread_state == "ended") {
				//
				$('.thread_abort').addClass("hide");
				//
			}
			//
			if (msg.thread_data) {
				//
				json_thread_data = JSON.parse( msg.thread_data )
				//
				if(json_thread_data.hasOwnProperty('get_classes')){
					//
					localStorage.setItem( efo_name, JSON.stringify(json_thread_data))
					//
					got.got_a = true;
					//
				}
				//
				if(json_thread_data.hasOwnProperty('get_glif_width')){
					//
					localStorage.setItem( "get_glif_width", JSON.stringify(json_thread_data.get_glif_width))
					//
					got.got_b = true;
					//
				}
				//
				if(json_thread_data.hasOwnProperty('update_adjustments_json')){
					//
					console.log("update_adjustments_json")
					//console.log(JSON.stringify(json_thread_data.update_adjustments_json))
					//
					//localStorage.setItem( efo_name+'_kerning', JSON.stringify(json_thread_data.update_adjustments_json))
					//
					//
					//got.got_c = true;
					//
				}
				//
			}
			//
			display_alert(msg.text, $(".display_alert"), "static");
			//
		});
		//
		if (callback) { callback(socket_node, socket_flask);}
		//
	};
	//
	action_python_thread = function(c_node_id, tell, data, callback){
		//
		if (tell) {
			//
			if (tell == "abort") {
				//
				_tell = "abort";
				//
				display_alert("warning_thread_aborted", $(".display_alert"), "static");
				//
			} else {
				//
				_tell = tell;
				//display_alert("warning_cannot_tell_that_to_thread", $(".display_alert"), "static"); // it takes offense
				//
			}
			//
		} else {
			//
			_tell = "active"
			//
		}
		//
		if (data) {
			_data = data;
		} else {
			_data = "";
		}
		//
		$.ajax({
			url: "/thread",
			type: "POST",
			dataType: "json",
			data: {
				"id": c_node_id, 
				"tell": _tell,
				"efo":$(".efo_source").attr("data-efo"),
				"data":_data
			},
			timeout : 100000,
			error: function(xhr) {
				//
				display_alert(xhr.responseText, $(".display_alert"), "static");
				//
			},
			success: function(response, responseJSON, data) {
				//
				if ( callback ){callback()};
				//
			}
			//
		});
		//
		//
	}
	//
	function range_laber_coverage(_slider, cur_val){
		//
		labels = _slider.find(".rangeslider__labels").children()
		//
		labels.each(function(index, value) {
			//
			t_label = labels.eq(index)
			t_label_val = parseInt(t_label.attr("data-val"))
			//
			if (cur_val >= t_label_val) {
				//
				t_label.addClass("_c")
				//
			} else {
				//
				t_label.removeClass("_c")
				//
			}
			//
		});
		//
	}
	//
	$('input[type="range"].range_slider').rangeslider({
		//
		polyfill: false,
		rangeClass: 'rangeslider',
		disabledClass: 'rangeslider--disabled',
		horizontalClass: 'rangeslider--horizontal',
		fillClass: 'rangeslider__fill',
		handleClass: 'rangeslider__handle',
		onInit: function(value) {
			$rangeEl = this.$range;
			//
			var rangeLabels = this.$element.attr('labels');
			rangeLabels = rangeLabels.split(', ');
			//
			// add labels
			$rangeEl.append('<div class="rangeslider__labels"></div>');
			//
			$(rangeLabels).each(function(index, value) {
				//
				$rangeEl.find('.rangeslider__labels').append('<span class="rangeslider__labels__label" data-val="'+value+'">' + value + '</span>');
				//
			});
			//
			range_laber_coverage(this.$range, this.value)
			//
		},
		onSlide: function(position, value) {
			//
			range_laber_coverage(this.$range, value)
			//
		}//,
		/*onSlideEnd: function(position, value) {
			//
		}*/
	});
	//
	$('.rangeslider__labels__label').on("click", function(e){

		_val = $(this).attr("data-val");
		//
		$(this).parents(".rangeslider-wrap").find(".range_slider").val(_val).change()
		//
		
	});
	//
	//
	function check_guide_visibility(_input){
		//
		if(_input.is(':checked')){
			//
			return true
			//
		} else {
			//
			return false
			//
		}
		//
	}
	//
	function do_guide_check(_t){
		//
		is_guides = check_guide_visibility(_t)
		//
		if(is_guides){
			//
			$('.kern').removeClass('guides_hide');
			//
		} else {
			//
			$('.kern').addClass('guides_hide');
			//
		}
	}
	//
	do_guide_check($('#onoff_guides'))
	//
	$('#onoff_guides').click(function(){
		//
		do_guide_check($(this))
		//
	})
	//
	init_socket();
	//
	var efo_dir = $(".efo_source").attr("data-efo");
	var efo_name = efo_dir.substring(efo_dir.lastIndexOf('/')+1);
	//
	$('.thread_active').bind('click', function(e){
		//
		$('.thread_abort').removeClass("hide");
		//
		json_kerning_data = localStorage.getItem(efo_name+'_kerning')
		//
		action_python_thread(socket_ids.socket_node_id, "update_adjustments_json", json_kerning_data);
		//action_python_thread(socket_ids.socket_node_id)
		//
	});
	//
	//
	$('.thread_abort').bind('click', function(e){
		//
		$(this).addClass("hide");
		//
		action_python_thread(socket_ids.socket_node_id, "abort")
		//
	});
	//
	function get_data(){
		//
		if (!localStorage.getItem(efo_name)) {
			//
			action_python_thread(socket_ids.socket_node_id, "get_classes");
			//
		}
		//
		if (!localStorage.getItem("get_glif_width")) {
			//
			action_python_thread(socket_ids.socket_node_id, "get_glif_width");
			//
		}
		//
	}
	//
	function get_screenshot(c, callback){
		//
		$(".modal-screenshot").find(".screenshot_result").empty();
		//
		domtoimage.toJpeg(c, { "quality": 1, "bgcolor": "#fff" }).then(function(dataUrl) { // toPng
			//
			var img = new Image();
			img.src = dataUrl;
			//
			$(".screenshot_info").empty();
			$(".screenshot_info").hide();
			//
			$(".modal-screenshot").find(".screenshot_result").append(img);
			//
			if (callback) { callback() }
			//
		  })
		  .catch(function(error) {
			console.error('oops, something went wrong!', error);
		  });
		//
		/*html2canvas(c).then(function(canvas) {
			//
			FAIL
			//
		});*/
		//
	}
	//
	function data_timer() {
		//
		//console.log(localStorage.getItem(efo_name), localStorage.getItem("get_glif_width"))
		if (localStorage.getItem(efo_name) && localStorage.getItem("get_glif_width")) {

			$(".kern").kern_adjust({
				"class_kern_elem": $("#onoff_class_kerning"),
				"efo_name": efo_name,
				"kern_classes": JSON.parse(localStorage.getItem(efo_name))["get_classes"],
				"glif_width": JSON.parse(localStorage.getItem("get_glif_width")),
				"masters":{"thn":[100,0],"reg":[400,0],"bld":[700,0],"thn_it":[100,1],"reg_it":[400,1],"bld_it":[700,1]},
				onSlideEnd: function(k_object) {
					//
				}
			});
			//
			$(window).trigger('resize');
			//
			stop_data_timer();
			//
		} else {
			//
			get_data();
			//
		}
	}
	//
	function stop_data_timer() {
		//
		clearInterval(get_data_timer);
		//
	}
	//
	setTimeout(function(){
		//
		get_data();
		//
	},1000);
	//
	$('.screenshot_active').on("click",function(){
		//
		var d = new Date();
		//
		$(".screenshot_info").show();
		$(".screenshot_info").text(efo_name+': '+d.toLocaleString());
		//
		get_screenshot($("#capture")[0], function(){
			$('.modal-screenshot').modal({
				show: true,
				backdrop: 'static'
			});
			
		});
		//

	});
	//
});
//
