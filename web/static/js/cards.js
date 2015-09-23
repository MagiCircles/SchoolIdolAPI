
function hidePopovers() {
    $('.ownedcardonbottom').popover('hide');
    $('.ownedcardonbottom').popover('disable');
    $('[data-toggle=popover]').popover('hide');
}

$(function () {
    $('[data-toggle="popover"]').popover();

    // Dismiss popovers on click outside
    $('body').on('click', function (e) {
	if ($(e.target).data('toggle') !== 'popover'
	    && $(e.target).parents('.popover.in').length === 0) {
	    hidePopovers();
	}
    });
})

function addCardButtonHandler() {
    // ADD CARD
    $('a[href="#auickAddCard"]').unbind('click');
    console.log('bind quickadd event click');
    $('a[href="#quickAddCard"]').click(function(e) {
	e.preventDefault();
	console.log('called twice');
	var button = $(this);
	var card = button.closest('.card');
	if (card.find('.flaticon-loading').length == 0) {
	    button.hide();
	    button.before('<i class="flaticon-loading"></i>');
	    var form = $('#quickaddform');
	    form.find('[name=card]').attr('value', card.prop('id'));
	    form.find('[name=card]').closest('.form-group').hide();
	    form.find('input.btn').removeClass('btn-Smile btn-Pure btn-Cool btn-All btn-default');
	    form.find('input.btn').addClass('btn-' + card.attr('data-attribute'));
	    form.find('form').attr('action', '/ajax/addcard/');
	    var onError = function() {
		$('i.flaticon-loading').remove();
		$('a[href="#quickAddCard"]').show();
		alert('Oops! Something bad happened. Try again.');
	    };
	    form.find('form').ajaxSubmit({
		success: function(data) {
		    var ownedcardbutton = $(data);
		    $('i.flaticon-loading').remove();
		    $('a[href="#quickAddCard"]').show();
		    if (ownedcardbutton.hasClass('ownedcardonbottom')) {
			button.before(ownedcardbutton);
			button.before(' ');
			editCardFormHandler();
			$('[data-toggle="popover"]').popover();
			form.find('form').attr('action', '/ajax/editcard/' + ownedcardbutton.attr('data-id') + '/');
			$('a[href="#quickAddCard"]').popover('hide');
			ownedcardbutton.popover({
			    'html': true,
			    'placement': 'top',
			    'content': form.html(),
			}).parent().delegate('form', 'submit', function(e) {
			    e.preventDefault();
			    button.hide();
			    button.before('<i class="flaticon-loading"></i>');
			    hidePopovers();
			    $(this).ajaxSubmit({
				success: function(data) {
				    var newownedcardbutton = $(data);
				    $('i.flaticon-loading').remove();
				    $('a[href="#quickAddCard"]').show();
				    ownedcardbutton.replaceWith(newownedcardbutton);
				    editCardFormHandler();
				    $('[data-toggle="popover"]').popover();
				},
				error: onError,
			    });
			    return false;
			}).delegate('#id_owner_account', 'change', function() {
			    form.find('#id_owner_account option').removeAttr('selected');
			    form.find('#id_owner_account option').prop('selected', false);
			    form.find('#id_owner_account option[value=' + $(this).val() + ']').attr('selected', true);
			}).delegate('a[href=#editCard]', 'click', function() {
			    onClickEditCard($(this), ownedcardbutton);
			});
			ownedcardbutton.popover('show');
			ownedcardbutton.on('shown.bs.popover', function () {
			    $('[data-toggle=popover]').popover('hide');
			});
		    }
		},
		error: onError,
	    });
	}
	return false;
    });
}

function shareButtons() {
    stLight.options({
	publisher: "f651d0dd-8213-437a-be4a-5ccc4d544d03",
	doNotHash: true,
	doNotCopy: true,
	hashAddressBar: false,
    });
    stButtons.locateElements();
}

function youtubeRatio() {
    var showYoutubeIframe = function(embed_video, link) {
	if (embed_video.length > 0) {
	    embed_video.html('<iframe style="width: 100%" height="200" src="' + embed_video.attr('data-url') + '?rel=0&amp;controls=0&amp;showinfo=0" frameborder="0" allowfullscreen></iframe>' + (link ? '<div class="text-right padding20 padding-novertical"><small class="padding-"><a href="https://www.youtube.com/user/Umidahh/playlists" target="_blank">Watch all the stories</a></small></div>' : '') + '<br>');
	    var width = embed_video.parent().width();
	    embed_video.find('iframe').height(width * (450 / 800));
	}
    };
    $('.more.collapse').on('show.bs.collapse', function() {
	showYoutubeIframe($(this).find('.embed_video'), true);
	showYoutubeIframe($(this).find('.embed_japanese_video'), false);
    });
    $('.already_collapsed').each(function() {
	showYoutubeIframe($(this).find('.embed_video'), true);
	showYoutubeIframe($(this).find('.embed_japanese_video'), false);
    });
}

// function center_images() {
//     $('.card_images').each(function() {
// 	if ($(this).closest('.panel-body').children('.row').length > 0) {
// 	    var height = $(this).closest('.panel-body').height();
// 	    $(this).css('margin-top', (height / 2) - ($(this).find('.idolized').height() / 2));
// 	}
//     });
// }

function load_more_function() {
    var button = $("#load_more");
    button.html('<div class="loader">Loading...</div>');
    var next_page = button.attr('data-next-page');
    $.get('/ajax/cards/' + location.search + (location.search == '' ? '?' : '&') + 'page=' + next_page, function(data) {
	button.replaceWith(data);
	pagination();
	addCardButtonHandler();
	editCardFormHandler();
	statistics_buttons();
	youtubeRatio();
	shareButtons();
	collapseCards();
	// center_images();

	// Reload disqus comments count
	window.DISQUSWIDGETS = undefined;
	$.getScript("http://schoolidol.disqus.com/count.js");

	$('[data-toggle="popover"]').popover();
    });
}

function pagination() {
    var button = $("#load_more");
    $(window).scroll(
	function () {
	    if (button.length > 0
		&& button.find('.loader').length == 0
		&& ($(window).scrollTop() + $(window).height())
		>= ($(document).height() - button.height())) {
		load_more_function();
	    }
	});
}

function statistics_buttons() {
    $('.btn.minimum_statistics').unbind('click');
    $('.btn.minimum_statistics').click(function() {
	card = $(this).closest('.card')
	card.find('.statistics_minimum').show()
	card.find('.statistics_non_idolized_maximum').hide()
	card.find('.statistics_idolized_maximum').hide()
	card.find('.hp_non_idolized').show()
	card.find('.hp_idolized').hide()
    })
    $('.btn.non_idolized_statistics').unbind('click');
    $('.btn.non_idolized_statistics').click(function() {
	card = $(this).closest('.card')
	card.find('.statistics_minimum').hide()
	card.find('.statistics_non_idolized_maximum').show()
	card.find('.statistics_idolized_maximum').hide()
	card.find('.hp_non_idolized').show()
	card.find('.hp_idolized').hide()
    })
    $('.btn.idolized_statistics').unbind('click');
    $('.btn.idolized_statistics').click(function() {
	card = $(this).closest('.card')
	card.find('.statistics_minimum').hide()
	card.find('.statistics_non_idolized_maximum').hide()
	card.find('.statistics_idolized_maximum').show()
	card.find('.hp_non_idolized').hide()
	card.find('.hp_idolized').show()
    })
}

function collapseCards() {
    $('.card a[data-target^=#collapseMore]').unbind('click');
    $('.card a[data-target^=#collapseMore]').click(function(event) {
	event.preventDefault();
	$($(this).attr('data-target')).collapse('toggle');
	return false;
    });
}

function changeAccount() {
    if ($('#id_select_account').val() == '') {
	$('#sidebar-wrapper #id_stored').val('').change();
	$('#sidebar-wrapper #id_stored').prop('disabled', 'disabled');
	$('#sidebar-wrapper #id_idolized').val('').change();
	$('#sidebar-wrapper #id_idolized').prop('disabled', 'disabled');
	$('#sidebar-wrapper #id_max_level').val('').change();
	$('#sidebar-wrapper #id_max_level').prop('disabled', 'disabled');
	$('#sidebar-wrapper #id_max_bond').val('').change();
	$('#sidebar-wrapper #id_max_bond').prop('disabled', 'disabled');
    } else {
	$('#sidebar-wrapper #id_stored').prop('disabled', false);
	if(event.type == "change"){
		$('#sidebar-wrapper #id_stored').val('Deck').change();
	}
	$('#sidebar-wrapper #id_idolized').prop('disabled', false);
	$('#sidebar-wrapper #id_max_level').prop('disabled', false);
	$('#sidebar-wrapper #id_max_bond').prop('disabled', false);
    }
}

if (typeof stLight != 'undefined') { // Adblocks prevents loading
    stLight.options({
	publisher:'f651d0dd-8213-437a-be4a-5ccc4d544d03',
    });
}

$(document).ready(function() {
    addCardButtonHandler();
    statistics_buttons();
    // center_images();
    pagination();
    youtubeRatio();
    shareButtons();
    collapseCards();

    changeAccount();
    $('#id_select_account').change(function(event) {
	changeAccount();
    });


    $('.idol #disqus_thread').bind('DOMNodeInserted', function() {
	$(this).height($('.idol table').height());
    });

    if ($('#id_sub_unit').val() != ''
	|| $('#id_idol_year').val() != ''
	|| $('#id_collection').val() != ''
	|| $('#id_is_promo').val() != ''
	|| $('#id_is_special').val() != ''
	|| $('#id_is_event').val() != ''
	|| $('#id_skill').val() != ''
       ) {
	$('#morefilters.collapse').collapse('show');
    }

});
