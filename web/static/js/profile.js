
var loadingHTML = '<br><div class="alert alert-warning">Loading...</div>';

function removeLoadOnEmpty(tab_elt, account) {
    if (tab_elt.find('.deck_total').text() == '') {
	tab_elt.find('[href="#loadMoreCards"]').parent().remove();
    }
}

function loadMoreCards(tab, tab_elt, account) {
    var button = tab_elt.find('[href="#loadMoreCards"]');
    var parentbutton = button.parent();
    button.unbind('click');
    button.click(function(e) {
	e.preventDefault();
	parentbutton.html(loadingHTML);
	$.get('/ajax/accounttab/' + account + '/' + tab + '/more/', function(data) {
	    parentbutton.replaceWith(data);
	    popovers();
	});
	return false;
    });
}

var onLoadTab = {
    'deck': function(tab_elt, account) {
	var remaining = parseInt($('#' + account + ' .deck_total_value').text()) - parseInt(tab_elt.find('[href="#loadMoreCards"]').attr('data-cards-limit'));
	if (remaining  > 0) {
	    tab_elt.find('.deck_total').text(remaining);
	} else {
	    tab_elt.find('[href="#loadMoreCards"]').parent().remove();
	}
	loadMoreCards('deck', tab_elt, account);
    },
    'wishlist': function(tab_elt, account) {
	removeLoadOnEmpty(tab_elt, account);
	loadMoreCards('wishlist', tab_elt, account);
    },
    'album': function(tab_elt, account) {
	removeLoadOnEmpty(tab_elt, account);
	loadMoreCards('album', tab_elt, account);
    },
    'presentbox': function(tab_elt, account) {
	removeLoadOnEmpty(tab_elt, account);
	loadMoreCards('presentbox', tab_elt, account);
    },
};

$('ul.nav-tabs li a').click(function (e) {
    e.preventDefault();
    $(this).tab('show');
});
$('ul.nav-tabs li a').on('show.bs.tab', function (e) {
    var id = $(e.target).attr('href');
    var tab_elt = $(id);
    var account = tab_elt.closest('.panel').prop('id');
    if (tab_elt.text() == '') {
	var tab = tab_elt.data('tab');
	tab_elt.html(loadingHTML);
	$.get('/ajax/accounttab/' + account + '/' + tab + '/', function(data) {
	    tab_elt.html(data);
	    if (typeof onLoadTab[tab] != 'undefined') {
		onLoadTab[tab](tab_elt, account);
	    }
	    popovers();
	});
    }
});

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

    if ($('#activities').length > 0 && $(window).width() >= 1200) {
	$.get('/ajax/activities/?avatar_size=0&card_size=133&user=' + $('#username').text(), function(data) {
	    $('#activities').html(data);
	      updateActivities();
	      $(window).scroll(
		  function () {
		      var button = $('a[href="#loadMoreActivities"]');
		      if (button.length > 0
			  && button.find('.loader').length == 0
			  && ($(window).scrollTop() + $(window).height())
			  >= ($('#activities').height())) {
			  feed = $('#myactivities').length > 0 ? true : undefined;
			  loadMoreActivitiesOnClick(button, $('#activities'), undefined, undefined, 0, 133, $('#username').text());
		      }
		  });
	});
    }

    $('.profile-account .nav-tabs li.active').each(function() {
	var tab = $(this).find('a').attr('data-tab');
	var tab_elt = $($(this).find('a').attr('href'));
	var account = $(this).closest('.profile-account').attr('id');
	if (typeof onLoadTab[tab] != 'undefined') {
	    onLoadTab[tab](tab_elt, account);
	}
	
    });
});

(function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = "//connect.facebook.net/en_US/sdk.js#xfbml=1&appId=376082385870922&version=v2.0";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));
