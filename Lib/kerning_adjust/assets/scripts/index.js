//
$(document).ready(function() {
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
	//$(".range_slider").val(100).change();
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
});