
var r_hidden = false;

function check_counters() {
    var counter_smile = $('.initial_setup_card[data-attribute="Smile"] img.owned').length;
    var counter_pure = $('.initial_setup_card[data-attribute="Pure"] img.owned').length;
    var counter_cool = $('.initial_setup_card[data-attribute="Cool"] img.owned').length;
    if (counter_smile >= 9
	&& counter_pure >= 9
	&& counter_cool >= 9) {
	$("#r_idolized").hide();
	$("#r").hide();
	$('.link-stars-side a[href="#r_idolized"]').parent().hide();
	r_hidden = true;
    } else {
	$("#r_idolized").show();
	$("#r").show();
	$('.link-stars-side a[href="#r_idolized"]').parent().show();
	r_hidden = false;
    }
}

function set_next_button_text(section) {
    if (section.find('.initial_setup_card img.owned').length > 0) {
	$('.next_buttons a').first().text($('.next_buttons').data('next-message'));
    } else {
	$('.next_buttons a').first().text($('.next_buttons').data('dont'));
    }
}

$(document).ready(function() {
    $('[data-toggle="popover"]').popover();
    check_counters();

    var account_id = $('#initialsetup_account').data('id');
    $('.initial_setup_card img.card').click(function(e) {
	e.preventDefault();
	var img = $(this);
	var card = img.closest('.initial_setup_card');
	var card_id = card.data('card-id');
	var idolized = img.hasClass('idolized');
	var owned = img.hasClass('owned');
	var section = card.closest('.home-section');
	card.find('img.card').hide();
	card.find('.loader').show();
	if (owned) {
	    var ownedcard_id = img.attr('data-ownedcard-id');
	    $.ajax({
		method: 'GET',
		url: '/ajax/deletecard/' + ownedcard_id + '/',
		success: function(data) {
		    img.removeClass('owned');
		    img.attr('data-ownedcard-id', '');
		    card.find('img.card').show();
		    card.find('.loader').hide();
		    check_counters();
		    set_next_button_text(section);
		},
		error: genericAjaxError,
	    });
	} else {
	    $.ajax({
		method: 'POST',
		url: '/ajax/albumbuilder/addcard/' + card_id + '/',
		data: {
		    account: account_id,
		    stored: 'Deck',
		    idolized: idolized ? 1 : 0,
		    max_level: 0,
		    max_bond: 0,
		    json: 1,
		},
		success: function(data) {
		    img.addClass('owned');
		    img.attr('data-ownedcard-id', data['id']);
		    card.find('img.card').show();
		    card.find('.loader').hide();
		    check_counters();
		    set_next_button_text(section);
		},
		error: genericAjaxError,
	    });
	}
	return false;
    });
    $(window).scroll(function() {
	var cutoff = $(window).scrollTop();
	var progress = (((cutoff + $(window).height()) / $(document).height()) * 100);
	$('.next_buttons .progress-bar').width(progress + '%');
	if (progress > 10) {
	    $('.next_buttons .progress-bar').text(Math.round(progress) + '%');
	} else {
	    $('.next_buttons .progress-bar').text('');
	}
	$('.home-section').each(function() {
	    var section = $(this);
	    var rainbow = section.data('rainbow');
	    if (typeof rainbow == 'undefined'
		|| ((rainbow == '8' || rainbow == '9') && r_hidden)) {
		$('.next_buttons a').first().hide();
		$('.next_buttons a').last().parent().removeClassPrefix('color-Rainbow-');
		$('.next_buttons .progress-bar').removeClassPrefix('bg-Rainbow-');
		$('.next_buttons .progress-bar').addClass('progress-bar-success');
	    } else {
		var top_section = section.offset().top;
		var bottom_section = section.offset().top + section.outerHeight();
		var button_cutoff = cutoff + $(window).height() - 176; // size of next buttons section when button is shown
		if (top_section < button_cutoff && bottom_section >= button_cutoff) {
		    $('.next_buttons a').first().removeClassPrefix('btn-Rainbow-');
		    $('.next_buttons a').first().addClass('btn-Rainbow-' + rainbow);
		    $('.next_buttons a').first().show();
		    $('.next_buttons a').first().prop('href', section.data('next-section'));
		    $('.next_buttons a').last().parent().removeClassPrefix('color-Rainbow-');
		    $('.next_buttons a').last().parent().addClass('color-Rainbow-' + rainbow);
		    set_next_button_text(section);
		    $('.next_buttons .progress-bar').removeClass('progress-bar-success');
		    $('.next_buttons .progress-bar').removeClassPrefix('bg-Rainbow-');
		    $('.next_buttons .progress-bar').addClass('bg-Rainbow-' + rainbow);
		    return false;
		}
	    }
	});
    });
    $('a[href="#saveprogress"]').click(function(e) {
	e.preventDefault();
	var seen_cards = current_seen_cards.slice();
	$('.initial_setup_card').each(function() {
	    if ($(this).offset().top < $(window).scrollTop()) {
		var card_id = $(this).data('card-id');
		if ($.inArray(card_id, seen_cards) == -1) {
		    seen_cards.push(card_id);
		}
	    }
	});
	freeModal($('.next_buttons a').last().text(), '<a href="/cards/initialsetup/?account=' + account_id + '&saveprogress=' + seen_cards.sort().join(',') + '" class="btn btn-' + btnColor + ' btn-lg" style="white-space: normal;">' + bookmark_message + ' <i class="flaticon-link"></i></a>');
	return false;
    });
});
