$(function () {
    var $form = $('#feedback-form');
    $form.on('submit', function (event) {
        event.preventDefault();
        event.preventDefault();
        $.post($form.attr('action'), $form.serialize())
            .done(function () {
                $form.find('input[type="submit"]').hide();
                $form.find('input:visible,textarea:visible').removeClass('error').addClass('success');
            })
            .fail(function (data) {
                $form.find('input:visible,textarea:visible').removeClass('error');
                $.each(data.responseJSON, function (field_name) {
                    $form.find('[name="' + field_name + '"]').addClass('error');
                });
            });
    });
});
