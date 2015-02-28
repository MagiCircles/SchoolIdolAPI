
$(document).ready(function() {
    loadMoreActivities($('#activities'), undefined, true);
    $(window).scroll(
	function () {
	    var button = $('a[href="#loadMoreActivities"]');
	    if (button.length > 0
		&& button.find('.loader').length == 0
		&& ($(window).scrollTop() + $(window).height())
		>= ($(document).height() - button.height())) {
		loadMoreActivitiesOnClick(button, $('#activities'), undefined, true);
	    }
	});
});
