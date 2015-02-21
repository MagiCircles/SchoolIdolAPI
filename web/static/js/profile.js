
$('label.cardstype').click(function () {
    $(this).find('input').tab('show');

});
$('label.cardstype').on('show.bs.tab', function (e) {
    var tab = $($(e.target).attr('data-target'));
    var account = tab.closest('.panel').prop('id');
    if (tab.text() == '') {
	tab.html('<div class="alert alert-warning">Loading...</div>');
	$.get('/ajax/ownedcards/' + account + '/' + tab.attr('data-stored') + '/', function(data) {
	    tab.html(data);
	})
    }
})

$(function () {
    $('[data-toggle="popover"]').popover();
});

$(".owned_card").popover({
    html : true,
    placement: 'top',
    trigger: 'hover',
    content: function() {
	return $(this).find('.owned_card_details').html();
    },
});

$(document).ready(function() {
    $('.topprofile .description').html(Autolinker.link($('.topprofile .description').html(), { newWindow: true, stripPrefix: true } ));
});
