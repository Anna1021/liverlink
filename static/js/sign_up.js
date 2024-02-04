$(document).ready(function() {
    $('#id_user_type').change(function() {
        if ($(this).val() == 'PT') {
            $('#patient_fields').show();
            $('#parent_fields').hide();
        } else if ($(this).val() == 'PR') {
            $('#parent_fields').show();
            $('#patient_fields').hide();
        }
    });
});