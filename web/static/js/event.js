
$('.event-edit').click(function(event) {
    event.preventDefault();
    freeModal($($(this).attr('href') + 'title').html(),
	      $($(this).attr('href')).html(), 0);
});
