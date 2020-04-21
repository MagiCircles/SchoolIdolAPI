
function picturesJSONToHTML(json, page) {
    var html = '';
    $.each(json, function(index, picture) {
	html += '<a href="http://danbooru.donmai.us/posts/' + picture.id + '" target="_blank"><img src="http://danbooru.donmai.us' + picture.preview_file_url + '" /></a>'
    });
    html += '<button id="load_more" class="btn btn-lg margin20 btn-' + idol_attribute + ' btn-block" data-next-page="' + (parseInt(page) + 1) + '">Load more</button>';
    return html;
}

function loadPicturesJSON(page, callback) {
    $.get('http://danbooru.donmai.us/posts.json?tags=official_art%20' + idol_tag + '%20rating:s&page=' + page + '&limit=27', callback);
}

function loadMorePictures() {
    var button = $("#load_more");
    button.html('<span class="loader">Loading...</span>');
    var next_page = button.attr('data-next-page');
    loadPicturesJSON(next_page, function(data) {
	button.replaceWith(picturesJSONToHTML(data, next_page));
    });
}

$(document).ready(function() {
    loadPicturesJSON(1, function(data) {
	$('#idol_pictures').html(picturesJSONToHTML(data, 1));
	$(window).scroll(
	    function () {
		var button = $('#load_more');
		if (button.length > 0
		    && button.find('.loader').length == 0
		    && ($(window).scrollTop() + $(window).height())
		    >= ($(document).height() - button.height())) {
		    loadMorePictures();
		    $('[data-toggle="popover"]').popover();
		}
	    });
	if ($('#load_more').visible(true)) {
	    if ($(this).find('.loader').length == 0) {
		loadMorePictures();
	    }
	}
    });
});
