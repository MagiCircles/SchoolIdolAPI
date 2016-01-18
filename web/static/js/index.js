
var avatar_size = 2;
var card_size = 133;

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
	      if (container.find('.activities .alert-warning')) {
		  container.find('.activities .alert-warning').replaceWith('<a href="/users/" target="_blank" class="fontx3 padding50" style="display: block">' + follow_sentence + '</a>');
	      }
	      updateActivities();
	      $(window).scroll(
		  function () {
		      var button = $('a[href="#loadMoreActivities"]');
		      if (button.length > 0
			  && button.find('.loader').length == 0
			  && ($(window).scrollTop() + $(window).height())
			  >= ($(document).height() - button.height())) {
			  feed = $('#myactivities').length > 0 ? true : undefined;
			  loadMoreActivitiesOnClick(button, container, undefined, feed, avatar_size, card_size);
		      }
		  });
	  });
}

$(function() {
    if ($('#countdown').length > 0) {
	$('#countdown').countdown({
	    date: countdowndate,
	    render: countdownRender
	});
    }
});


$(document).ready(function() {
    $('[data-toggle="popover"]').popover();
    loadActivities();

    $('#activities-buttons .all').click(function() {
	if ($('#activities').length == 0) {
	    $('#myactivities').attr('id', 'activities');
	    console.log('all');
	    loadActivities();
	}
    });
    $('#activities-buttons .following').click(function() {
	if ($('#myactivities').length == 0) {
	    console.log('following');
	    $('#activities').attr('id', 'myactivities');
	    loadActivities();
	}
    });
});
