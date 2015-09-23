
$('#id_verification').change(function(e) {
    $('#verification-note').remove();
    $('#id_verification').closest('.form-group').after('<div id="verification-note">' + $('#verification-' + $('#id_verification').val()).html() + '</div>');
});

