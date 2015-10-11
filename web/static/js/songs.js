
function collapseSongs() {
    $('.song a[data-target^=#collapseMore]').unbind('click');
    $('.song a[data-target^=#collapseMore]').click(function(event) {
	event.preventDefault();
	$($(this).attr('data-target')).collapse('toggle');
	var song = $(this).closest('.song');
	if (song.find('.itunes a').attr('href') == '') {
	    loadiTunesData($(this).closest('.song'), function() {}, function() {});
	}
	return false;
    });
}

function pauseAllSongs() {
    $('audio').each(function() {
	$(this)[0].pause();
	$(this).closest('div').find('[href=#play] i').removeClass();
	$(this).closest('div').find('[href=#play] i').addClass('flaticon-play');
    });
}

function loadiTunesData(song, successCallback, errorCallback) {
    var itunes_id = song.find('[href=#play]').data('itunes-id');
    $.ajax({
	"url": 'https://itunes.apple.com/lookup',
	"dataType": "jsonp",
	"data": {
	    "id": itunes_id,
	},
	"error": function (jqXHR, textStatus, message) {
	    errorCallback();
	    alert('Oops! This music doesn\'t seem to be valid anymore. Please contact us and we will fix this.');
	},
	"success": function (data, textStatus, jqXHR) {
	    data = data['results'][0];
	    song.find('.itunes').find('.album').prop('src', data['artworkUrl60']);
	    song.find('.itunes').find('a').prop('href', data['trackViewUrl']);
	    song.find('.itunes').show('slow');
	    song.find('audio source').prop('src', data['previewUrl'])
	    song.find('audio')[0].load();
	    successCallback(data);
	}
    });
}

function playSongButtons() {
    $('audio').on('ended', function() {
	pauseAllSongs();
    });
    $('[href=#play]').unbind('click');
    $('[href=#play]').click(function(event) {
	event.preventDefault();
	var button = $(this);
	var button_i = button.find('i');
	var song = button.closest('.song');
	// Stop all previously playing audio
	if (button_i.prop('class') == 'flaticon-pause') {
	    pauseAllSongs();
	    return;
	}
	pauseAllSongs();
	if (song.find('audio source').attr('src') != '') {
	    song.find('audio')[0].play();
	    button_i.removeClass();
	    button_i.addClass('flaticon-pause');
	} else {
	    button_i.removeClass();
	    button_i.addClass('flaticon-loading');
	    loadiTunesData(song, function(data) {
		song.find('audio')[0].play();
		button_i.removeClass();
		button_i.addClass('flaticon-pause');
	    }, function() {
		button_i.removeClass();
		button_i.addClass('flaticon-play');
	    });
	}
	return false;
    });
}

function load_more_function() {
    var button = $("#load_more");
    button.html('<div class="loader">Loading...</div>');
    var next_page = button.attr('data-next-page');
    $.get('/ajax/songs/' + location.search + (location.search == '' ? '?' : '&') + 'page=' + next_page, function(data) {
	button.replaceWith(data);
	pagination();

	collapseSongs();
	songs_stats_buttons();
	playSongButtons();

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

$(document).ready(function() {
    pagination();
    collapseSongs();
    songs_stats_buttons();
    playSongButtons();
});
