
var avatar_size = 2;
var card_size = 133;

$('#countdown').countdown({
    date: countdowndate,
    render: countdownRender
});
$('#countdown2').countdown({
    date: countdowndate,
    render: countdownRender
});

function loadActivities() {
    var container, feed;
    if ($('#myactivities').length > 0) {
	container = $('#myactivities');
	feed = true;
    } else {
	container = $('#activities');
	feed = undefined;
    }
    container.find('.activities').html('<div class="loader">Loading...</div>');
    $.get('/ajax/' + (typeof feed == 'undefined' ? 'activities' : 'feed')
	  + '/?avatar_size=' + avatar_size + '&card_size=' + card_size, function(data) {
	      container.find('.activities').html(data);
	      $(window).scroll(
		  function () {
		      var button = $('a[href="#loadMoreActivities"]');
		      if (button.length > 0
			  && button.find('.loader').length == 0
			  && ($(window).scrollTop() + $(window).height())
			  >= ($(document).height() - button.height())) {
			  loadMoreActivitiesOnClick(button, container, undefined, feed, avatar_size, card_size);
		      }
		  });
	  });
}

$(document).ready(function() {
    $('[data-toggle="popover"]').popover();
    loadActivities();
});
