
$(document).ready(function() {
    $('#template div').each(function() {
	var template = $(this);
	var button = $('<button class="btn btn-default btn-' + template.data('btn') + ' btn-sm">' + template.data('name') + '</button>')
	$('#templates-buttons').append(button).append(' ');
	button.click(function(e) {
	    $('#id_verification_comment').text(template.text());
	});
    });
    $('#staffverification').submit(function(e) {
	e.preventDefault();
	var form = $(this);
	form.ajaxSubmit({
	    success: function(data) {
		$('#staffverification').hide();
		$('#staffcancelverification').show();
		$('#steps').collapse('show');
	    },
	    error: function() {
		alert('Oops! Something bad happened. Try again.');
	    }
	});
	return false;
    });
    $('#staffcancelverification').submit(function(e) {
	e.preventDefault();
	var form = $(this);
	form.ajaxSubmit({
	    success: function(data) {
		$('#staffverification').show();
		$('#staffcancelverification').hide();
		$('#steps').collapse('hide');
	    },
	    error: function() {
		alert('Oops! Something bad happened. Try again.');
	    }
	});
	return false;
    });
    $('.delete-verification-image').click(function(e) {
	e.preventDefault();
	var button = $(this);
	$.ajax({
	    url: button.prop('href'),
	    success: function(data) {
		button.closest('.verification-image').remove();
	    },
	    error: function() {
		alert('Oops! Something bad happened. Try again.');
	    }	    
	});
	return false;
    });
});
