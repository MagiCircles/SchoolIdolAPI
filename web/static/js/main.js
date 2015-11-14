
function getInterfaceColor() {
    return $('body').attr('class').replace('interface-', '');
}

$('a.page-scroll').bind('click', function(event) {
    var $anchor = $(this);
    $('html, body').stop().animate({
	scrollTop: $($anchor.attr('href')).offset().top
    }, 1500, 'easeInOutExpo');
    event.preventDefault();
});

$("#togglebutton").click(function(e) {
    e.preventDefault();
    $("#wrapper").toggleClass("toggled");
});

function freeModal(title, body, buttons) {
    $('#freeModal .modal-header h4').html(title);
    $('#freeModal .modal-body').html(body);
    $('#freeModal .modal-footer').html('<button type="button" class="btn btn-Smile" data-dismiss="modal">Go</button>');
    if (buttons === 0) {
	$('#freeModal .modal-footer').hide();
    } else if (typeof buttons != 'undefined') {
	$('#freeModal .modal-footer').html(buttons);
	$('#freeModal .modal-footer').show();
    }
    $('#freeModal').modal('show');
}

function globalModal(hash, modal_size) {
    if (hash == 'donate') {
	window.location.href = "/donate/";
	return;
    }
    if (hash == 'about') {
	window.location.href = "/about/";
	return;
    }
    $.get('/ajax/modal/' + hash +
	  '/?interfaceColor=' + getInterfaceColor(), function(data) {
	      $('#modal .modal-content').html(data);
	      $('#modal .modal-dialog').removeClass('modal-lg');
	      $('#modal .modal-dialog').removeClass('modal-sm');
	      if (typeof modal_size != 'undefined') {
		  $('#modal .modal-dialog').addClass('modal-' + modal_size);
	      }
	      $('#modal').modal('show');
	      modalHandler();
	  });
}

function updateActivities() {
    $('.likeactivity').off('submit');
    $('.likeactivity').submit(function(e) {
	e.preventDefault();
	$(this).ajaxSubmit({
	    context: this,
	    success: function(data) {
		if (data == 'liked') {
		    $(this).find('input[type=hidden]').prop('name', 'unlike');
		} else {
		    $(this).find('input[type=hidden]').prop('name', 'like');
		}
		var value = $(this).find('button[type=submit]').html();
		$(this).find('button[type=submit]').html($(this).find('button[type=submit]').attr('data-reverse'));
		$(this).find('button[type=submit]').attr('data-reverse', value);
	    },
	    error: function() {
		alert('Oops! Something bad happened. Try again.');
	    }
	});
    });
}

function avatarStatus() {
    $('.avatar_wrapper').each(function() {
	if (typeof $(this).attr('data-user-status') != 'undefined') {
	    $(this).popover({
		title: '<span style="color: ' + $(this).css('color') + '">' + $(this).attr('data-user-status') + '</span>',
		content: '<small style="color: #333">School Idol Tomodachi Donator</small>',
		html: true,
		placement: 'bottom',
		trigger: 'hover',
	    });
	}
    });
}

function modalHandler() {
    $('[data-toggle=ajaxmodal]').unbind('click');
    $('[data-toggle=ajaxmodal]').click(function(e) {
	e.preventDefault();
	globalModal($(this).attr('href').replace('#', '').replace('Modal', ''), $(this).data('modal-size'));
    });
}

function formloaders() {
    $('button[data-form-loader=true]').click(function(e) {
	$(this).html('<i class="flaticon-loading"></i>');
	$(this).unbind('click');
	$(this).click(function(e) {
	    e.preventDefault();
	    return false;
	});
    });
}

$(document).ready(function() {
    var hash = window.location.hash.substring(1);
    if (hash.indexOf("Modal") >= 0) {
	globalModal(hash.replace('Modal', ''));
    }

    modalHandler();

    $('.switchLanguage').click(function(e) {
	e.preventDefault();
	$('#switchLanguage').find('select').val($(this).attr('data-lang'));
	$('#switchLanguage').submit();
    });

    updateActivities();
    avatarStatus();

    formloaders();
});

(function () {
    var s = document.createElement('script'); s.async = true;
    s.type = 'text/javascript';
      s.src = '//' + disqus_shortname + '.disqus.com/count.js';
    (document.getElementsByTagName('HEAD')[0] || document.getElementsByTagName('BODY')[0]).appendChild(s);
}());
