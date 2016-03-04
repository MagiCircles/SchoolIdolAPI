
function handle_report(e) {
    e.preventDefault();
    var button = $(this);
    button.closest('td').append('<i class="flaticon-loading"></i>');
    button.closest('td').find('button').hide();
    $.ajax({
        method: 'POST',
        url: button.data('href'),
        data: {
            'comment': button.closest('td').find('textarea').val(),
        },
        success: function(data) {
            button.closest('tr').hide('slow');
        },
        error: genericAjaxError,
    });
    return false;
}

$(document).ready(function() {
    $('.accept-report').click(handle_report);
    $('.reject-report').click(handle_report);
});
