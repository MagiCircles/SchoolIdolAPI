
$(document).ready(function() {
    var hash = window.location.hash.substring(1);
    if (hash.indexOf("Modal") >= 0) {
	if ($('#' + hash).length > 0) {
	    $('#' + hash).modal('show');
	}
    }

    $('.switchLanguage').click(function(e) {
	e.preventDefault();
	$('#switchLanguage').find('select').val($(this).attr('data-lang'));
	$('#switchLanguage').submit();
    });
});

var disqus_developer = 1;
var disqus_shortname = 'schoolidol';
(function () {
    var s = document.createElement('script'); s.async = true;
    s.type = 'text/javascript';
      s.src = '//' + disqus_shortname + '.disqus.com/count.js';
    (document.getElementsByTagName('HEAD')[0] || document.getElementsByTagName('BODY')[0]).appendChild(s);
}());
