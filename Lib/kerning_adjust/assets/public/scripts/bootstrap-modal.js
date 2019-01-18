!function ($) {

  "use strict"; // jshint ;_;

  var slide_modal;

 /* MODAL CLASS DEFINITION
  * ====================== */

  var Modal = function (content, options) {
    this.options = options
    this.$element = $(content)
      .delegate('[data-dismiss="modal"]', 'click.dismiss.modal', $.proxy(this.hide, this))
    
  }

  Modal.prototype = {

      constructor: Modal

    , toggle: function () {
        return this[!this.isShown ? 'show' : 'hide']()
      }

    , show: function () {

        var that = this;

        var e = $.Event('show');
        this.$element.trigger(e)
        
        //
        that.$element.removeClass('hide')
        //
        that.$element.show();

        //
        if (this.options.shift) {
          $('body').addClass('modal_slide_animating');
          that.$element.css({'top':0})
        } else {
           that.$element.addClass('in')
        }
        //
        $('#root').addClass('modal_open')
        //
       // var e = $.Event('show')

        //this.$element.trigger(e)
        //
        //
        if (this.isShown || e.isDefaultPrevented()) return
        //
        that.$element.show()
        //
        if (this.options.shift) {
          //
          $('#root').addClass('modal_open_fullscreen');
          $('body').addClass('modal-shift-'+this.options.shift);
          //
        } else {
          //
          $('body').addClass('modal-open')
          //
        }
        //
        this.isShown = true

        escape.call(this)
        backdrop.call(this, function () {
          var transition = $.support.transition && that.$element.hasClass('fade')

          if (!that.$element.parent().length) {
            that.$element.appendTo(document.body) //don't move modals dom position
          }

          if (that.options.shift) {

          } else {

            that.$element.show()

          }

          if (transition) {
            that.$element[0].offsetWidth // force reflow
          }

          if (that.options.shift) {

            that.$element.trigger('shown')
            
          } else {

            console.log('add in')
  
            that.$element.addClass('in')
            transition ?
              that.$element.one($.support.transition.end, function () { that.$element.trigger('shown') }) :
              that.$element.trigger('shown')

          }
          

          //
          if (that.options.shift) {
            setTimeout(function(){

              that.$element.addClass('revealed_modal');
              
            },500);
            setTimeout(function(){

              that.$element.removeClass('concealed_modal');
              
              //
            },1000);
          }
          //
        })
      }

    , hide: function (e) {
        e && e.preventDefault()

        var that = this

        if (that.options.shift) {
          $('body').addClass('modal_slide_animating');
          that.$element.css({'top':'-100%'})
        }

        e = $.Event('hide')

        this.$element.trigger(e)

        if (!this.isShown || e.isDefaultPrevented()) return

        this.isShown = false

        if (that.options.shift) {
          
          $('body').removeClass('modal-shift-'+this.options.shift);

        } else {
          $('body').removeClass('modal-open')

          //$('body').find('#root').removeClass('modal_open');
          $('body').find('#root').addClass('modal_closed');
          
        }

        escape.call(this)

        if (that.options.shift) {
          slide_modal = setTimeout(function(){
            //
            that.$element.removeClass('revealed_modal').removeClass('concealed_modal');
            $('body').removeClass('modal_slide_animating');
            //
            setTimeout(function(){
              //
              that.$element.css({'display':'none'})
              //
            },500);
            //
            clearTimeout(slide_modal)
            //
          },500);
        }else{
          this.$element.removeClass('in')
          this.$element.addClass('hide')
          $.support.transition && this.$element.hasClass('fade') ?
            hideWithTransition.call(this) :
            hideModal.call(this)
        }
        $('#root').removeClass('modal_open');
        $('#root').removeClass('modal_open_fullscreen');

      }

  }


 /* MODAL PRIVATE METHODS
  * ===================== */

  function hideWithTransition() {
    var that = this
      , timeout = setTimeout(function () {
          that.$element.off($.support.transition.end)
          hideModal.call(that)
        }, 500)

    this.$element.one($.support.transition.end, function () {
      clearTimeout(timeout)
      hideModal.call(that)
    })
  }

  function hideModal(that) {
    this.$element
      .hide()
      .trigger('hidden')

    backdrop.call(this)
  }

  function backdrop(callback) {
    var that = this
      , animate = this.$element.hasClass('fade') ? 'fade' : ''

    var is_root_has_menu = $('#root').find('.menu__overlay');

    if (this.isShown && this.options.backdrop) {
      var doAnimate = $.support.transition && animate
      //
      //
      if (is_root_has_menu.length) {
        this.$backdrop = is_root_has_menu;
        if (that.options.shift) {
        } else {
          this.$backdrop.css({'display':'block'});
          this.$backdrop.addClass(animate);
        }
      } else {
        //
        this.$backdrop = $('<div class="modal-backdrop ' + animate + '" />')
          .appendTo(document.body)
        //
      }
        if (this.options.backdrop != 'static') {
          this.$backdrop.click($.proxy(this.hide, this))
        }
        if (doAnimate) this.$backdrop[0].offsetWidth // force reflow

        if (that.options.shift) {
        } else {

        this.$backdrop.addClass('in')
        }

        doAnimate ?
          this.$backdrop.one($.support.transition.end, callback) :
          callback()

    } else if (!this.isShown && this.$backdrop) {

      this.$backdrop.removeClass('in')

      if (is_root_has_menu.length) {
        this.$backdrop.css({'display':'none'});
      }else{
        $.support.transition && this.$element.hasClass('fade')?
          this.$backdrop.one($.support.transition.end, $.proxy(removeBackdrop, this)) :
          removeBackdrop.call(this)
      }

    } else if (callback) {
      callback()
    }
  }

  function removeBackdrop() {
    this.$backdrop.remove()
    this.$backdrop = null
  }

  function escape() {
    var that = this
    if (this.isShown && this.options.keyboard) {
      $(document).on('keyup.dismiss.modal', function ( e ) {
        e.which == 27 && that.hide()
      })
    } else if (!this.isShown) {
      $(document).off('keyup.dismiss.modal')
    }
  }


 /* MODAL PLUGIN DEFINITION
  * ======================= */

  $.fn.modal = function (option, callback) {
    return this.each(function () {
      var $this = $(this)
        , data = $this.data('modal')
        , options = $.extend({}, $.fn.modal.defaults, $this.data(), typeof option == 'object' && option)
      if (!data) $this.data('modal', (data = new Modal(this, options)))
      if (typeof option == 'string') data[option]()
      else if (options.show) data.show()
    });
  }

  $.fn.modal.defaults = {
      backdrop: true
    , keyboard: true
    , show: true
    , shift: false
  }

  $.fn.modal.Constructor = Modal


 /* MODAL DATA-API
  * ============== */

  $(function () {
    $('body').on('click.modal.data-api', '[data-toggle="modal"]', function ( e ) {
      var $this = $(this), href
        , $target = $($this.attr('data-target') || (href = $this.attr('href')) && href.replace(/.*(?=#[^\s]+$)/, '')) //strip for ie7
        , option = $target.data('modal') ? 'toggle' : $.extend({}, $target.data(), $this.data())

      e.preventDefault()
      $target.modal(option)
    })
  })

}(window.jQuery);