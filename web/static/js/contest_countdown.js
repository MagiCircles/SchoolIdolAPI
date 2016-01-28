$(function() {
    if ($('#countdown').length > 0) {
	$('#countdown').countdown({
	    date: countdowndate,
	    render: function(data) {
		$(this.el).text(data.days + ' days, ' + data.hours + ' hours, ' + data.min + ' minutes, ' + data.sec + ' seconds left to vote');
	    }
	});
    }
});
