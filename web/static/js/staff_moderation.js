
function loadDisqus(cursor) {
    $.ajax({
        method: 'GET',
        url: 'https://disqus.com/api/3.0/posts/list.json?api_key=' + disqus_api_key + '&forum=schoolidol&limit=25&related=thread&order=desc' + (typeof cursor != 'undefined' ? '&cursor=' + cursor : ''),
        success: function(data) {
            $('#disqus_comments').find('.disqus_loading').remove();
            $('#disqus_comments').find('#loadMoreDisqus').remove();
            $.each(data.response, function(i, item) {
                $('#disqus_comments').append('<li class="dsq-widget-item" data-id="' + item.id + '"><div class="pull-right"><a href="#report" class="btn btn-warning" style="color: white">Report this comment</a></div>' + (item.author.isAnonymous ? '<a href="#">[Anonymous ' + item.author.name + ']</a>' : '<a href="' + item.author.profileUrl + '"><img class="dsq-widget-avatar" src="' + item.author.avatar.large.cache + '"></a> <a class="dsq-widget-user" href="' + item.author.profileUrl + '">' + item.author.username + '</a>') + ' <span class="dsq-widget-comment">' + item.message + '</span> <p class="dsq-widget-meta"><a href="' + item.thread.link + '" target="_blank">' + item.thread.clean_title + '</a>&nbsp;·&nbsp;<a href="' + item.url + '" target="_blank"><time class="timeago" datetime="' + new Date(item.createdAt.replace('T', 'Z')).toISOString() + '">' + item.createdAt + '</time></a></p><hr></li>');
            });
            $('#disqus_comments').append('<a href="#" id="loadMoreDisqus" class="btn btn-default btn-block">Load more comments</a>');
            $('#loadMoreDisqus').click(function(e) {
                e.preventDefault();
                $(this).replaceWith('<div class="disqus_loading" style="font-size: 4em; text-align: center;"><i class="flaticon-loading"></i></div>');
                loadDisqus(data.cursor.next);
                return false;
            });
            $('[href="#report"]').unbind('click');
            $('[href="#report"]').click(function(e) {
                e.preventDefault();
                var comment = $(this).closest('.dsq-widget-item');
                var id = comment.data('id');
                $(this).replaceWith('<i class="flaticon-loading"></i>');
                $.ajax({
                    method: 'POST',
                    url: 'https://disqus.com/api/3.0/posts/report.json?api_key=' + disqus_api_key + '&post=' + id,
                    success: function(data) {
                        comment.find('.flaticon-loading').replaceWith('<div class="alert alert-warning">Reported!</div>');
                    },
                });
                return false;
            });
            jQuery("time.timeago").timeago();
        },
    });
}

$(document).ready(function() {
    loadDisqus();
});
