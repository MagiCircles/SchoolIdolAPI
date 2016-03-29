
function disableDeckButton(card_id) {
    $('tr.tr_ownedcard[data-card-id="' + card_id + '"] .flaticon-deck').addClass('disable');
    $('tr.tr_ownedcard[data-card-id="' + card_id + '"] .flaticon-deck').prop('title', deck_disable_title);
    $('tr.tr_ownedcard[data-card-id="' + card_id + '"] .flaticon-deck').prop('data-original-title', deck_disable_title);
    $('[data-toggle="tooltip"]').tooltip('fixTitle');
}

function enableDeckButton(card_id) {
    $('tr.tr_ownedcard[data-card-id="' + card_id + '"] .flaticon-deck').removeClass('disable');
    $('tr.tr_ownedcard[data-card-id="' + card_id + '"] .flaticon-deck').prop('title', deck_enable_title);
    $('tr.tr_ownedcard[data-card-id="' + card_id + '"] .flaticon-deck').prop('data-original-title', deck_enable_title);
    $('[data-toggle="tooltip"]').tooltip('fixTitle');
}

var editable = {
    deck: {
	data: function(disabled) { return { stored: 'Album' } },
	success: function(button, data) {
	    button.addClass('flaticon-' + data['stored'].toLowerCase());
	    var card_id = button.closest('tr').data('card-id');
	    disableDeckButton(card_id);
	    button.closest('tr').find('.td-for-skill').text('');
	},
    },
    album: {
	data: function(disabled) { return { stored: 'Deck' } },
	success: function(button, data) {
	    button.addClass('flaticon-' + data['stored'].toLowerCase());
	    var ownedcard_tr = button.closest('tr');
	    var card_id = ownedcard_tr.data('card-id');
	    var card_tr = $('tr.tr_card[data-id="' + card_id + '"]');
	    if ($('tr.tr_ownedcard[data-card-id="' + card_id + '"] .flaticon-album').length == 0) {
		enableDeckButton(card_id);
	    }
	    if (card_tr.data('rarity') != 'N' && !card_tr.data('is_special')) {
		button.closest('tr').find('.td-for-skill').html('<i class="flaticon-skill disable"><small>1</small></i><div class="skill-form" style="display: none"><input type="number" min="1" max="8" value="1" class="form-control input-sm"><button class="btn btn-' + card_tr.data('attribute') + ' btn-sm" type="button">' + go_message + '</button>');
		ownedCardButtonsHandler(ownedcard_tr);
	    }
	},
    },
    idolized: {
	data: function(disabled) { return { idolized: disabled } },
	success: function(button, data) {
	    button.addClass('flaticon-idolized');
	    if (!data['idolized']) {
		button.addClass('disable');
		button.closest('tr').find('.flaticon-max-level').hide();
		button.closest('tr').find('.flaticon-max-level').addClass('disable');
		button.closest('tr').find('.flaticon-max-bond').hide();
		button.closest('tr').find('.flaticon-max-bond').addClass('disable');
	    } else {
		button.closest('tr').find('.flaticon-max-level').show('fast');
		button.closest('tr').find('.flaticon-max-bond').show('fast');
	    }
	},
    },
    'max-level': {
	data: function(disabled) { return { max_level: disabled } },
	success: function(button, data) {
	    button.addClass('flaticon-max-level');
	    if (!data['max_level']) {
		button.addClass('disable');
	    }
	},
    },
    'max-bond': {
	data: function(disabled) { return { max_bond: disabled } },
	success: function(button, data) {
	    button.addClass('flaticon-max-bond');
	    if (!data['max_bond']) {
		button.addClass('disable');
	    }
	},
    },
    skill: {
	data: function(level) { return { skill: level } },
	success: function(button, data) {
	    button.removeClass();
	    button.addClass('flaticon-skill');
	    button.closest('td').find('small').text(data['skill']);
	    button.closest('td').find('.skill-form input').val(data['skill']);
	    if (data['skill'] < 2) {
		button.addClass('disable');
	    }
	},
    },
};

function ownedCardButtonsHandler(ownedCardTr) {
    for (elt in editable) {
	ownedCardTr.find('.flaticon-' + elt).unbind('click');
	ownedCardTr.find('.flaticon-' + elt).click(function(e) {
	    e.preventDefault();
	    var button = $(this);
	    var disabled = button.hasClass('disable');
	    var ownedcard_id = button.closest('tr').data('id');
	    var elt = button.attr('class').replace('flaticon-', '').replace('disable', '').replace(' ', '');
	    if (elt == 'skill') {
		button.hide();
		button.closest('td').find('.skill-form').show();
		button.closest('td').find('.skill-form button').unbind('click');
		button.closest('td').find('.skill-form button').click(function(e) {
		    e.preventDefault();
		    button.removeClass();
		    button.addClass('flaticon-loading');
		    button.closest('td').find('.skill-form').hide();
		    button.show();
		    $.ajax({
			method: 'POST',
			url: '/ajax/albumbuilder/editcard/' + ownedcard_id + '/',
			data: editable[elt]['data'](button.closest('td').find('.skill-form input').val()),
			success: function(data) {
			    editable[elt]['success'](button, data);
			},
			error: genericAjaxError,
		    });
		    return false;
		});
	    } else if (typeof editable[elt] != 'undefined') {
		if (!(elt == 'deck' && disabled)) {
		    button.removeClass();
		    button.addClass('flaticon-loading');
		    $.ajax({
			method: 'POST',
			url: '/ajax/albumbuilder/editcard/' + ownedcard_id + '/',
			data: editable[elt]['data'](disabled),
			success: function(data) {
			    button.removeClass();
			    editable[elt]['success'](button, data);
			},
			error: genericAjaxError,
		    });
		}
		return false;
	    }
	});
    }
    ownedCardTr.find('.flaticon-delete').click(function(e) {
	e.preventDefault();
	var button = $(this);
	var ownedcard_tr = button.closest('tr');
	var ownedcard_id = ownedcard_tr.data('id');
	var card_id = ownedcard_tr.data('card-id');
	var card_tr = $('tr.tr_card[data-id="' + card_id + '"]');
	button.removeClass();
	button.addClass('flaticon-loading');
	$.ajax({
	    method: '',
	    url: '/ajax/deletecard/' + ownedcard_id + '/',
	    success: function(data) {
		ownedcard_tr.remove();
		card_tr.find('td').attr('rowspan', card_tr.find('td').first().prop('rowspan') - 1);
		if ($('tr.tr_ownedcard[data-card-id="' + card_id + '"]').length == 0) {
		    card_tr.append('<td colspan="6" class="tr_card_padder"></td>');
		} else {
		    if ($('tr.tr_ownedcard[data-card-id="' + card_id + '"] .flaticon-album').length == 0) {
			enableDeckButton(card_id);
		    }
		}
	    },
	});
    });
}

$(document).ready(function() {
    $('.tr_card').each(function() {
	var card_id = $(this).data('id');
	if ($('tr.tr_ownedcard[data-card-id="' + card_id + '"] .flaticon-album').length > 0) {
	    disableDeckButton(card_id);
	}
    });
    $('.tr_ownedcard').each(function() {
	ownedCardButtonsHandler($(this));
    });
    $('.flaticon-add').click(function(e) {
	e.preventDefault();
	var button = $(this);
	var card_tr = button.closest('tr');
	var card_id = card_tr.data('id');
	button.removeClass();
	button.addClass('flaticon-loading');
	var stored = 'Album';
	if ($('tr.tr_ownedcard[data-card-id="' + card_id + '"] .flaticon-album').length > 0) {
	    stored = 'Deck';
	}
	var max_bond = 0;
	var max_level = 0;
	var idolized = 0;
	if (stored == 'Album') {
	    idolized = $('tr.tr_ownedcard[data-card-id="' + card_id + '"] .flaticon-idolized:not(.disable)').length > 0 ? 1 : 0;
	    max_level = $('tr.tr_ownedcard[data-card-id="' + card_id + '"] .flaticon-max-level:not(.disable)').length > 0 ? 1 : 0;
	    max_bond = $('tr.tr_ownedcard[data-card-id="' + card_id + '"] .flaticon-max-bond:not(.disable)').length > 0 ? 1 : 0;
	}
	if (stored == 'Album' && $('tr.tr_ownedcard[data-card-id="' + card_id + '"] .flaticon-deck').length > 0) {
	    result = confirm(album_confirm_add_when_deck);
	    if (!result) {
		button.removeClass();
		button.addClass('flaticon-add');
		return false;
	    }
	}
	$.ajax({
	    method: 'POST',
	    url: '/ajax/albumbuilder/addcard/' + card_id + '/',
	    data: {
		account: button.closest('table').data('account-id'),
		stored: stored,
		idolized: idolized,
		max_level: max_level,
		max_bond: max_bond,
	    },
	    success: function(data) {
		button.removeClass();
		button.addClass('flaticon-add');
		var tr = $(data);
		button.closest('tr').after(tr);
		ownedCardButtonsHandler(tr);
		card_tr.find('.tr_card_padder').remove();
		card_tr.find('td').attr('rowspan', card_tr.find('td').first().prop('rowspan') + 1);
		disableDeckButton(card_id);
	    },
	    error: genericAjaxError,
	});
	return false;
    });
});
