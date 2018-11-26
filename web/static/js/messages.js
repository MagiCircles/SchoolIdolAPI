
function load_more_function() {
    var button = $("#load_more");
    button.html('<div class="loader">Loading...</div>');
    var next_page = button.attr('data-next-page');
    $.get((typeof(receiver_username) == 'undefined' ?
           '/ajax/messages/'
           : '/ajax/messages/' + receiver_username + '/')
          + location.search + (location.search == '' ? '?' : '&') + 'page=' + next_page, function(data) {
	          button.replaceWith(data);
	          pagination();
          });
}

function pagination() {
    var button = $("#load_more");
    $(window).scroll(
	function () {
	    if (button.length > 0
		&& button.find('.loader').length == 0
		&& ($(window).scrollTop() + $(window).height())
		>= ($(document).height() - button.height())) {
		load_more_function();
	    }
	});
}

$(document).ready(function() {
    pagination();
});
