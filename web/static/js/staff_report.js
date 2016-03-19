
function handle_report(e) {
    e.preventDefault();
    var button = $(this);
    button.closest('td').append('<i class="flaticon-loading"></i>');
    $('.accept-report').hide();
    $('.reject-report').hide();
    $.ajax({
        method: 'POST',
        url: button.data('href'),
        data: {
            'comment': button.closest('td').find('textarea').val(),
        },
        success: function(data) {
            var fakething = button.closest('tr').data('fake-thing');
            $('[data-fake-thing="' + fakething + '"]').hide('slow');
            $('.accept-report').show();
            $('.reject-report').show();
        },
        error: genericAjaxError,
    });
    return false;
}

$(document).ready(function() {
    $('.accept-report').click(handle_report);
    $('.reject-report').click(handle_report);
    $('textarea').click(function(e) {
        $(this).closest('td').find('.textarea-check').show('slow');
    });
});
