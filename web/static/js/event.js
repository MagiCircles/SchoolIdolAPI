
function loadmoreranking() {
    $('.load_more').unbind('click');
    $('.load_more').click(function(e) {
	e.preventDefault();
	var button = $(this);
	var buttonTr = button.closest('tr');
	var table = button.closest('table');
	var language = table.find('caption').data('language');
	var page = button.data('page');
	button.replaceWith('<i class="flaticon-loading"></i>');
	$.get('/ajax/eventranking/' + $('#event-title').data('id') + '/' + language + '/?page=' + (parseInt(page) + 1), function(data) {
	    buttonTr.remove();
	    var newTable = $(data);
	    newTable.find('caption').remove();
	    button.remove();
	    table.append(newTable.html());
	    loadmoreranking();
            $('[data-toggle="tooltip"]').tooltip();
	});
	return false;
    });
}

function playButton() {
    //if (href="#play" data-itunes-id="{{ event.song.itunes_id }}")
    var button = $('[href="#play"]');
    var song = button.closest('.itunes-song');
    if (button.length > 0) {
	loadiTunesData(song, function(data) {
	    data = data['results'][0];
	    song.find('a.itunes-link').prop('href', data['trackViewUrl'] + '&at=1001l8e6');
	    song.find('.flaticon-loading').remove();
	    song.find('a.itunes-link').show('slow');
	    button.show('slow');
	    song.find('audio source').prop('src', data['previewUrl'])
	    song.find('audio')[0].load();
	}, function() {
	});
	button.click(function(e) {
	    e.preventDefault();
	    if (button.find('.flaticon-pause').length > 0) {
		song.find('audio')[0].pause();
		button.find('i').removeClass();
		button.find('i').addClass('flaticon-play');
	    } else {
		song.find('audio')[0].play();
		button.find('i').removeClass();
		button.find('i').addClass('flaticon-pause');
	    }
	    return false;
	});
    }
}

$(function() {
    $('[data-toggle="tooltip"]').tooltip();
    if ($('#countdown').length > 0) {
	$('#countdown').countdown({
	    date: countdowndate,
	    render: countdownRender
	});
    }
    loadmoreranking();
    playButton();
});
