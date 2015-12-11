
function addCardFormHandler(non_idolized_card_url, idolized_card_url) {
    $('#addCardModal #id_max_level').parent().hide();
    $('#addCardModal #id_max_bond').parent().hide();

    var expirationHandler = function() {
	if ($('#addCardModal #id_stored').val() == 'Box') {
	    $('#addCardModal label[for=id_expires_in]').parent().show();
	} else {
	    $('#addCardModal label[for=id_expires_in]').parent().hide();
	    $('#addCardModal label[for=id_expires_in]').parent().find('input').val('');
	}
    };
    expirationHandler();

    if (typeof non_idolized_card_url == 'undefined') {
	$('#addCardModal #id_idolized').prop('checked', true);
	$('#addCardModal #id_max_level').parent().show();
	$('#addCardModal #id_max_bond').parent().show();
	$('#addCardModal #id_idolized').parent().hide();
	$('#addCardModal img.non_idolized').hide();
	$('#addCardModal img.idolized').prop('src', idolized_card_url);
    } else {
	$('#addCardModal #id_idolized').parent().show();
	$('#addCardModal img.non_idolized').prop('src', non_idolized_card_url);
	$('#addCardModal img.idolized').prop('src', idolized_card_url).hide();

	var idolizedCheckBoxHandler = function() {
	    if($('#addCardModal #id_idolized').is(":checked") || $('#addCardModal #id_idolized').val() == 'True') {
		$('#addCardModal #id_max_level').parent().show();
		$('#addCardModal #id_max_bond').parent().show();
		$('#addCardModal img.idolized').show();
		$('#addCardModal img.non_idolized').hide();
	    } else {
		$('#addCardModal #id_max_level').parent().hide();
		$('#addCardModal #id_max_bond').parent().hide();
		$('#addCardModal #id_max_level').prop('checked', false);
		$('#addCardModal #id_max_bond').prop('checked', false);
		$('#addCardModal img.idolized').hide();
		$('#addCardModal img.non_idolized').show();
	    }
	};
	idolizedCheckBoxHandler();

	$('#addCardModal #id_idolized').unbind('change');
	$('#addCardModal #id_idolized').change(idolizedCheckBoxHandler);
    }

    $('#addCardModal #id_stored').unbind('change');
    $('#addCardModal #id_stored').change(function() {
	expirationHandler();
    });
}

function onClickEditCard(cardButton, ownedcardelt) {
    var saveAddForm = $('#addCardModal .modal-body').html();
    var saveAddTitle = $('#addCardModal .modal-title').text();
    var card = cardButton.closest('.card');
    $.get('/ajax/editcard/' + ownedcardelt.attr('data-id') + '/', function(data) {
	$('#addCardModal .modal-body').html(data);
	$('#addCardModal .modal-title').text((is_japanese ? 'カードの変更' : 'Edit card'));
	$('#addCardModal').modal('show');
	hidePopovers();

	addCardFormHandler($('#addCardModal img.non_idolized').prop('src'),
			   $('#addCardModal img.idolized').prop('src'));

	var onDone = function() {
	    $('#addCardModal').modal('hide');
	    $('#addCardModal .modal-body').html(saveAddForm);
	    $('#addCardModal .modal-title').text(saveAddTitle);
	};

	$('#addCardModal form.edit').unbind('submit');
	var onSubmit = function(e) {
	    e.preventDefault();
	    $(this).ajaxSubmit({
		success: function(data) {
		    if ($(data).hasClass('ownedcardonbottom')) {
			ownedcardelt.replaceWith(data);
			onDone();
			editCardFormHandler();
			$('[data-toggle="popover"]').popover();
		    } else {
			$('#addCardModal .modal-body').html(data);
			$('#addCardModal form.edit').submit(onSubmit);
			addCardFormHandler($('#addCardModal img.non_idolized').prop('src'),
					   $('#addCardModal img.idolized').prop('src'));
		    }
		},
		error: function() {
		    onDone();
		    alert('Opps! Something bad happened. Try again.');
		}
	    });
	};
	$('#addCardModal form.edit').submit(onSubmit);
	$('#addCardModal form.delete').unbind('submit');
	$('#addCardModal form.delete').submit(function(e) {
	    e.preventDefault();
	    $(this).ajaxSubmit({
		success: function(data) {
		    ownedcardelt.replaceWith(data);
		    onDone();
		    editCardFormHandler();
		},
		error: function() {
		    onDone();
		    alert('Opps! Something bad happened. Try again.');
		}
	    });
	});
	$('#addCardModal').on('hidden.bs.modal', function (e) {
	    onDone();
	})
    });
}

function editCardFormHandler() {
    // EDIT CARD
    $('a[href="#editCard"]').unbind('click');
    $('a[href="#editCard"]').click(function(e) {
	var cardButton = $(this);
	onClickEditCard(cardButton, cardButton);
	return false;
    });
}

$(document).ready(function() {
    editCardFormHandler();
});
