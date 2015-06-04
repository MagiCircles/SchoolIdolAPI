
$('.event-edit').click(function(event) {
    event.preventDefault();
    freeModal($($(this).attr('href') + 'title').html(),
	      $($(this).attr('href')).html(), 0);

});

$(function() {
    if ($('#countdown').length > 0) {
	$('#countdown').countdown({
	    date: countdowndate,
	    render: countdownRender
	});
    }
});
