
function eventedit() {
    $('.event-edit').unbind('click');
    $('.event-edit').click(function(event) {
	event.preventDefault();
	freeModal($($(this).attr('href') + 'title').html(),
		  $($(this).attr('href')).html(), 0);
    });
}

function loadmoreranking() {
    $('.load_more').unbind('click');
    $('.load_more').click(function(e) {
	e.preventDefault();
	var button = $(this);
	var buttonTr = button.closest('tr');
	var table = button.closest('table');
	var language = table.find('caption').data('language');
	var page = button.data('page');
	button.replaceWith('<i class="flaticon-loading"></i>');
	$.get('/ajax/eventranking/' + $('#event-title').data('id') + '/' + language + '/?page=' + (parseInt(page) + 1), function(data) {
	    buttonTr.remove();
	    var newTable = $(data);
	    newTable.find('caption').remove();
	    button.remove();
	    table.append(newTable.html());
	    eventedit();
	    loadmoreranking();
	});
	return false;
    });
}

$(function() {
    if ($('#countdown').length > 0) {
	$('#countdown').countdown({
	    date: countdowndate,
	    render: countdownRender
	});
    }
    eventedit();
    loadmoreranking();
});
