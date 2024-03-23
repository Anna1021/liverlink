$(document).ready(function() {

    // Only show the hospital field if the user is from the United Kingdom
    if ($('#id_location').val() != 'GB') {
        $('#id_hospital').parent().hide();
    }

    $('#id_location').change(function() {
        if ($(this).val() == 'GB') {
            $('#id_hospital').parent().show();
        } else {
            $('#id_hospital').parent().hide();
        }
    });
});