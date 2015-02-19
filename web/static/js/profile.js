
$('label.cardstype').click(function () {
    $(this).find('input').tab('show');
});

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
