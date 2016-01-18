
function loadMoreUsers() {
    var button = $("#load_more");
    button.html('<span class="loader">Loading...</span>');
    var next_page = button.attr('data-next-page');
    $.get('/ajax/users/' + location.search + (location.search == '' ? '?' : '&') + 'page=' + next_page, function(data) {
	button.replaceWith(data);
	// Reload disqus comments count
	window.DISQUSWIDGETS = undefined;
	$.getScript("http://schoolidol.disqus.com/count.js");
    });
}

$(function () {
    $('[data-toggle="popover"]').popover();
})

$(document).ready(function() {
    $(window).scroll(
	function () {
	    var button = $('#load_more');
	    if (button.length > 0
		&& button.find('.loader').length == 0
		&& ($(window).scrollTop() + $(window).height())
		>= ($(document).height() - button.height())) {
		loadMoreUsers();
		$('[data-toggle="popover"]').popover();
	    }
	});
});
