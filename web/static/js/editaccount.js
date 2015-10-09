
function showverificationdetails() {
    $('#verification-note').remove();
    var verification_type = $('#id_verification').val();
    $('#id_verification').closest('.form-group').after('<div id="verification-note">' + $('#verification-' + verification_type).html() + '</div>');
    if (verification_type == 2) {
	$('#id_allow_during_events').closest('.form-group').show();
    } else {
	$('#id_allow_during_events').closest('.form-group').hide();
    }
}

$('#id_verification').change(function(e) {
    showverificationdetails();
});

$(document).ready(function() {
    showverificationdetails();
});
