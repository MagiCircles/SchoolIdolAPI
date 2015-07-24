
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

function updateActivities() {
	$('.likeactivity').off('submit');
	$('.likeactivity').submit(function(e) {
		e.preventDefault();
		$(this).ajaxSubmit({
			context: this,
			success: function(data) {
				if (data == 'liked') {
					$(this).find('input[type=hidden]').prop('name', 'unlike');
				} else {
					$(this).find('input[type=hidden]').prop('name', 'like');
				}
				var value = $(this).find('button[type=submit]').html();
				$(this).find('button[type=submit]').html($(this).find('button[type=submit]').attr('data-reverse'));
				$(this).find('button[type=submit]').attr('data-reverse', value);
			},
			error: function() {
				alert('Opps! Something bad happened. Try again.');
			}
		});
    });
}
