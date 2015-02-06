
$(document).ready(function() {
    var hash = window.location.hash.substring(1);
    if (hash.indexOf("Modal") >= 0) {
	if ($('#' + hash).length > 0) {
	    $('#' + hash).modal('show');
	}
    }
});
