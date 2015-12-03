
$(document).ready(function() {
    $('.post-activity').each(function() {
	var form = $(this).find('form');
	var file_input = $('<input type="file" name="imgur" />');
	form.find('#id_right_picture').hide();
	form.find('#id_right_picture').parent().find('.help-block').hide();
	form.find('#id_right_picture').parent().append(file_input);
	form.submit(function(e) {
	    e.preventDefault();
	    form.find('[type=submit]').replaceWith('<i class="flaticon-loading"></i>');
	    var file = file_input[0].files[0];
	    var reader = new FileReader();
	    reader.onloadend = function() {
		var formData = new FormData();
		formData.append(file.name, file);
		$.ajax({
		    url: 'https://api.imgur.com/3/image',
		    method: 'POST',
		    headers: {
			Authorization: "Client-ID " + imgurClientID,
			Accept: 'application/json'
		    },
		    data: {
			image: reader.result.split('base64,')[1],
			type: 'base64',
			title: 'School Idol Tomodachi',
			description: 'Posted on http://schoolido.lu/user/' + $.trim($('#username').text()) + '/',
		    },
		    success: function(data) {
			form.find('#id_right_picture').val(data.data.link);
			form.unbind("submit").submit();
		    },
		    error: genericAjaxError,
		});
	    };
	    if (file) {
		reader.readAsDataURL(file);
	    } else {
		form.unbind("submit").submit();
	    }
	    return false;
	});
    });
});
