
function getButton(parent) {
    return parent.find('a[href="#loadMoreActivities"]');
}

function loadMoreActivitiesOnClick(button, parent, account, feed, avatar_size) {
    var div = button.parent();
    var page = div.attr('data-page');
    div.html('<span class="loader">Loading...</span>');
    $.get('/ajax/' + (typeof feed == 'undefined' ? 'activities' : 'feed')
	  + '/?page=' + page
	  + (typeof account == 'undefined' ? '' : ('&account=' + account))
	  + (typeof avatar_size == 'undefined' ? '' : ('&avatar_size=' + avatar_size))
	  ,
	  function(data) {
	      div.replaceWith(data);
	      loadMoreActivities(parent, account, feed, avatar_size);
	      avatarStatus();
	      updateActivities();
	      // Reload disqus comments count
	      window.DISQUSWIDGETS = undefined;
	      $.getScript("http://schoolidol.disqus.com/count.js");
	  });
}

function loadMoreActivities(parent, account, feed, avatar_size) {
    avatarStatus();
    updateActivities();
    var button = getButton(parent);
    button.click(function(e) {
	e.preventDefault();
	loadMoreActivitiesOnClick(button, parent, account, feed, avatar_size);
    });
}
