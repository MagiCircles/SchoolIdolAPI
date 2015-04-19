
$(function () {
    $('[data-toggle="popover"]').popover();
})

$(".sidebar-toggle").click(function(e) {
    e.preventDefault();
    $("#wrapper").toggleClass("active");
});

function addCardButtonHandler() {
    // ADD CARD
    $('a[href="#addCard"]').unbind('click');
    $('a[href="#addCard"]').click(function(e) {
	var addCardButton = $(this);
	var card = addCardButton.closest('.card');
	$('#id_card').val(card.prop('id')).change();
	addCardFormHandler(card.find('img.non_idolized').prop('src'),
			   card.find('img.idolized').prop('src'));

	var savedForm = undefined;
	$('#addCardModal').on('hidden.bs.modal', function () {
	    if (typeof savedForm != 'undefined') {
		$('#addCardModal .modal-body').html(savedForm);
		$('#addCardModal').unbind('hidden.bs.modal');
	    }
	})
	var onSubmit = function(e) {
	    e.preventDefault();
	    $(this).ajaxSubmit({
		success: function(data) {
		    if ($(data).hasClass('ownedcardonbottom')) {
			addCardButton.before(data);
			$('#addCardModal').modal('hide');
			editCardFormHandler();
			$('[data-toggle="popover"]').popover();
			if (typeof savedForm != 'undefined') {
			    $('#addCardModal .modal-body').html(savedForm);
			}
		    } else {
			savedForm = $('#addCardModal .modal-body').html();
			$('#addCardModal .modal-body').html(data);
			$('#addCardModal form.add').submit(onSubmit);
			addCardFormHandler(card.find('img.non_idolized').prop('src'),
					   card.find('img.idolized').prop('src'));
		    }
		},
		error: function() {
		    $('#addCardModal').modal('hide');
		    alert('Opps! Something bad happened. Try again.');
		}
	    });
	};
	$('#addCardModal form.add').unbind('submit');
	$('#addCardModal form.add').submit(onSubmit);
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
    var oldButtonContent = button.html();
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
	$('#sidebar-wrapper #id_stored').val('Album').change();
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

addCardButtonHandler();
$(document).ready(function() {
    addCardButtonHandler();
    statistics_buttons();
    // center_images();
    pagination();
    youtubeRatio();
    shareButtons();

    changeAccount();
    $('#id_select_account').change(function(event) {
	changeAccount();
    });


    $('.idol #disqus_thread').bind('DOMNodeInserted', function() {
	$(this).height($('.idol table').height());
    });
});
