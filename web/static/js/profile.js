
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

    $('#follow').submit(function(e) {
	e.preventDefault();
	$(this).ajaxSubmit({
	    success: function(data) {
		if (data == 'followed') {
		    $('#follow input[type="hidden"]').prop('name', 'unfollow');
		} else {
		    $('#follow input[type="hidden"]').prop('name', 'follow');
		}
		var value = $('#follow input[type="submit"]').prop('value');
		$('#follow input[type="submit"]').prop('value', $('#follow input[type="submit"]').attr('data-reverse'));
		$('#follow input[type="submit"]').attr('data-reverse', value);
	    },
	    error: function() {
		alert('Opps! Something bad happened. Try again.');
	    }
	});
    });

    $('a[href="#followers"]').click(function(e) {
	e.preventDefault();
	var username = $('#username').text();
	var text = $(this).closest('tr').find('th').text();
	$.get('/ajax/followers/' +  username + '/', function(data) {
	    freeModal(username + ': ' + text, data);
	});
    });
    $('a[href="#following"]').click(function(e) {
	e.preventDefault();
	var username = $('#username').text();
	var text = $(this).closest('tr').find('th').text();
	$.get('/ajax/following/' +  username + '/', function(data) {
	    freeModal(username + ': ' + text, data);
	});
    });
});
