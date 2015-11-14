
$(document).ready(function() {
    $('.link-stars-side a .name').hide();
    $('.link-stars-side a .btn').hover(function() {
	$('.link-stars-side a .name').hide();
	$(this).parent().find('.name').show();
    }, function() {
	$(this).parent().find('.name').hide();
    });
});
