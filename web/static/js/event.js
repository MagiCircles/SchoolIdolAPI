
$('.event-edit').click(function(event) {
    event.preventDefault();
    freeModal($($(this).attr('href') + 'title').html(),
	      $($(this).attr('href')).html(), 0);

});

$(function() {
    if ($('#countdown').length > 0) {
	$('#countdown').countdown({
	    date: countdowndate,
	    render: function(data) {
		$(this.el).text(data.days + ' days, ' + data.hours + ' hours, ' + data.min + ' minutes, ' + data.sec + ' seconds left');
	    }
	});
    }
});
