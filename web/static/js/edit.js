
$('a[href=#deleteLink]').click(function(e) {
    e.preventDefault();
    var link = $(this).closest('tr');
    $.get('/ajax/deletelink/' + $(this).attr('data-link-id'), function(data) {
	if (data == 'deleted') {
	    link.remove();
	}
    });
    return false;
});

