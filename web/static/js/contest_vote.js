var submitted = null;

$('form').submit(function(e) {
    $('#vote_side').val(submitted);
    $('#left').attr('disabled', 'disabled');
    $('#right').attr('disabled', 'disabled');
    return true;
});

$('#left').click(function() { submitted = 'left' });
$('#right').click(function() { submitted = 'right' });

$(document).keydown(function(e) {
    switch(e.which) {
    case 37:
	e.preventDefault();
	$('#left').click();
	break;
    case 39:
	e.preventDefault();
	$('#right').click();
	break;
    default: return;
    }
});
