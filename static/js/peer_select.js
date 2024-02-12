$(document).ready(function() {
    // Initially hide all conditional fields
    function hideAllConditionalFields() {
        $('#id_age_of_diagnosis_min').parent().hide();
        $('#id_age_of_diagnosis_max').parent().hide();
        $('#id_condition').parent().hide();
        $('#id_child_age_of_diagnosis_min').parent().hide();
        $('#id_child_age_of_diagnosis_max').parent().hide();
        $('#id_child_condition').parent().hide();
    }

    hideAllConditionalFields();

    // Function to show/hide fields based on the checkbox selection
    function updateFieldVisibility() {
        // Hide all fields initially
        hideAllConditionalFields();

        // Check each user type checkbox to determine which fields to show
        $("input[name='user_type']").each(function() {
            if ($(this).is(':checked')) {
                var userType = $(this).val(); // 'patient' or 'parent'
                if (userType === 'patient') {
                    // Show patient-related fields
                    $('#id_age_of_diagnosis_min').parent().show();
                    $('#id_age_of_diagnosis_max').parent().show();
                    $('#id_condition').parent().show();
                } else if (userType === 'parent') {
                    // Show parent-related fields
                    $('#id_child_age_of_diagnosis_min').parent().show();
                    $('#id_child_age_of_diagnosis_max').parent().show();
                    $('#id_child_condition').parent().show();
                }
            }
        });
    }

    // Bind the change event to user type checkboxes
    $("input[name='user_type']").change(updateFieldVisibility);

    // Initial call to set the correct visibility state based on the current checkbox state
    updateFieldVisibility();
});