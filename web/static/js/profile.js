
var loadingHTML = '<br><div class="alert alert-warning">Loading...</div>';

$('ul.nav-tabs li a').click(function (e) {
    e.preventDefault();
    $(this).tab('show');
});
$('ul.nav-tabs li a').on('show.bs.tab', function (e) {
    var id = $(e.target).attr('href');
    var tab = $(id);
    var account = tab.closest('.panel').prop('id');
    if (tab.text() == '') {
	if (id.indexOf('#accountTabActivities') == 0) {
	    tab.html(loadingHTML);
	    $.get('/ajax/activities/?avatar_size=1&card_size=133&account=' + account, function(data) {
		tab.html(data);
		loadMoreActivities(tab, account, undefined, 1);
	    });
	} else if (id.indexOf('#accountTabEvents') == 0) {
	    tab.html(loadingHTML);
	    $.get('/ajax/eventparticipations/' + account + '/', function(data) {
		tab.html(data);
	    });
	}
    }
});

$('label.cardstype').click(function (e) {
    e.preventDefault();
    $(this).find('input').tab('show');
});

$('label.cardstype').on('show.bs.tab', function (e) {
    var tab = $($(e.target).attr('data-target'));
    var account = tab.closest('.panel').prop('id');
    if (tab.text() == '') {
	tab.html(loadingHTML);
	$.get('/ajax/ownedcards/' + account + '/' + tab.attr('data-stored') + '/', function(data) {
	    tab.html(data);
	    popovers();
	})
    }
})

$(function () {
    $('[data-toggle="popover"]').popover();
});

function popovers() {
    $(".owned_card").popover({
	html : true,
	placement: 'top',
	trigger: 'hover',
	content: function() {
	    return $(this).find('.owned_card_details').html();
	},
    });
}

$(document).ready(function() {
    $('.topprofile .description').html(Autolinker.link($('.topprofile .description').html(), { newWindow: true, stripPrefix: true } ));
    popovers();

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

(function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = "//connect.facebook.net/en_US/sdk.js#xfbml=1&appId=376082385870922&version=v2.0";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));
