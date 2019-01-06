//
function display_alert(alert_text, target_container, animation){
	//
	console.log("alert_text")
	console.log(alert_text)
	//
	//alert_text = "success_test"
	//
	if (alert_text) {
		//
		var alert_text = alert_text.toString();
		var target_alert = target_container;
		//
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
			
			//return	
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
$(document).ready(function() {
	//
	init_socket = function(callback){
		//
		var socket_node = io.connect('http://localhost:8008');
		var socket_flask = io.connect('http://localhost:5000/test');
		//
		
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
			console.log(log)
			console.log("=====")
			display_alert(log, $(".display_alert"), "static")
			//
		});
		//
		socket_flask.on('connect', function () { 
			//
			console.log('SOCKET CONNECTED FLASK')
			display_alert("success_flask_socket_connected", $(".display_alert"), "static")
			//
			//
			socket_flask.on('disconnected', function() {
				//
				console.log('SOCKET DISCONNECTED FLASK')
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
			console.log("got_message_for_relay")
			//
			console.log("Received number: " + msg.number);
			display_alert(msg.text, $(".display_alert"), "static");
			//
			//
		});
		//
		if (callback) { callback(socket_node, socket_flask);}
		//
	};
	//
	action_python = function(c_node_id){
		//
		$.ajax({
			url: "/gather",
			type: "POST",
			data: {"id": c_node_id},
			timeout : 100000,
			error: function(xhr) {
				//
				//console.log(xhr, '');
				console.log(xhr.responseText, '');
				//
			},
			success: function(response, responseJSON, data) {
				//
				console.log(response, '');
				//
			}
			//
		});
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
			//console.log(t_label_val, cur_val)
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
		// Feature detection the default is `true`.
			//
			polyfill: false,
			// Default CSS classes
			rangeClass: 'rangeslider',
			disabledClass: 'rangeslider--disabled',
			horizontalClass: 'rangeslider--horizontal',
			fillClass: 'rangeslider__fill',
			handleClass: 'rangeslider__handle',

			// Callback function
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

			// Callback function
			onSlide: function(position, value) {
				//
				range_laber_coverage(this.$range, value)
				//
				/*var $handle = this.$range.find('.rangeslider__handle__value');
				$handle.text(this.value);*/
			},

			// Callback function
			/*onSlideEnd: function(position, value) {
				range_laber_coverage(this.$range, value)
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
	setTimeout(function(){
		//
		$(".kern").kern_adjust();
		//
	},100);
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
			$('.kern').removeClass('guides_hide')
			//
		} else {
			//
			$('.kern').addClass('guides_hide')
			//
		}
	}
	//
	do_guide_check($('.onoffswitch-checkbox'))
	//
	$('.onoffswitch-checkbox').click(function(){
		//
		do_guide_check($(this))
		//
	})
	//
	init_socket();
	//
	$('.run_python').bind('click', function(e){
		//
		action_python(socket_ids.socket_node_id)
		//
	});
	//
	//
});
//
