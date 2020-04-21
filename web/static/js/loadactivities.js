
function getButton(parent) {
    return parent.find('a[href="#loadMoreActivities"]');
}

function loadMoreActivitiesOnClick(button, parent, account, feed, avatar_size, card_size, user, new_, all) {
    var div = button.parent();
    var page = div.attr('data-page');
    div.html('<span class="loader">Loading...</span>');
    $.get('/ajax/' + (typeof feed == 'undefined' ? 'activities' : 'feed')
	  + '/?page=' + page
	  + (typeof account == 'undefined' ? '' : ('&account=' + account))
	  + (window.location.hash.indexOf('#search=') == 0 ? '&search=' + window.location.hash.substr(8) : '')
	  + (typeof user == 'undefined' ? '' : ('&user=' + user))
	  + (typeof avatar_size == 'undefined' ? '' : ('&avatar_size=' + avatar_size))
	  + (typeof card_size == 'undefined' ? '' : ('&card_size=' + card_size))
	  + (all ? '&all' : '') + (new_ ? '&new' : ''),
	  function(data) {
	      div.replaceWith(data);
	      loadMoreActivities(parent, account, feed, avatar_size);
	      avatarStatus();
	      updateActivities();
	      // Reload disqus comments count
	      window.DISQUSWIDGETS = undefined;
	      $.getScript("https://schoolidol.disqus.com/count.js");
	  });
}

function loadMoreActivities(parent, account, feed, avatar_size, card_size) {
    avatarStatus();
    updateActivities();
    // Reload disqus comments count
    window.DISQUSWIDGETS = undefined;
    $.getScript("https://schoolidol.disqus.com/count.js");
    var button = getButton(parent);
    button.click(function(e) {
	e.preventDefault();
	loadMoreActivitiesOnClick(button, parent, account, feed, avatar_size, card_size);
    });
}
