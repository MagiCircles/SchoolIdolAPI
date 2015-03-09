
function getInterfaceColor() {
    return $('body').attr('class').replace('interface-', '');
}

function freeModal(title, body) {
    $('#freeModal .modal-header h4').html(title);
    $('#freeModal .modal-body').html(body);
    $('#freeModal').modal('show');
}

function globalModal(hash) {
    $.get('/ajax/modal/' + hash +
	  '/?interfaceColor=' + getInterfaceColor(), function(data) {
	      $('#modal .modal-content').html(data);
	      $('#modal').modal('show');
	      modalHandler();
	  });
}

function modalHandler() {
    $('[data-toggle=ajaxmodal]').click(function(e) {
	e.preventDefault();
	globalModal($(this).attr('href').replace('#', '').replace('Modal', ''));
    });
}

$(document).ready(function() {
    var hash = window.location.hash.substring(1);
    if (hash.indexOf("Modal") >= 0) {
	globalModal(hash.replace('Modal', ''));
    }

    modalHandler();

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
