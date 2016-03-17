
$('a[href="#deleteLink"]').click(function(e) {
    e.preventDefault();
    var link = $(this).closest('tr');
    $.get('/ajax/deletelink/' + $(this).attr('data-link-id'), function(data) {
	if (data == 'deleted') {
	    link.remove();
	}
    });
    return false;
});

$('#id_type').change(function(e) {
    $(this).closest('form').find('.alert').remove();
    if ($('#id_type').val() == 'otonokizaka') {
	$(this).closest('form').prepend('<div class="alert alert-info">Your Otonokizaka ID should look like "X-Nick" where X is your user ID and Nick is your nickname. Go to your Otonokizaka profile and look at the URL.</div>');
    }
});
