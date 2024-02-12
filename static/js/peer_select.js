document.addEventListener('DOMContentLoaded', function () {
    const userTypeCheckboxes = document.querySelectorAll('input[name="user_type"]');
    const patientFields = ['id_age_of_diagnosis_min', 'id_age_of_diagnosis_max', 'id_condition'];
    const parentFields = ['id_child_age_of_diagnosis_min', 'id_child_age_of_diagnosis_max', 'id_child_condition'];

    function toggleFields() {
        let userTypes = [];
        userTypeCheckboxes.forEach(function(checkbox) {
            if (checkbox.checked) {
                userTypes.push(checkbox.value);
            }
        });

        function displayFields(fieldIds, display) {
            fieldIds.forEach(function(fieldId) {
                const fieldWrapper = document.querySelector('.' + fieldId + '_wrapper');
                if (fieldWrapper) {
                    fieldWrapper.style.display = display ? '' : 'none';
                }
            });
        }
        if (userTypes.includes('patient')) {
            displayFields(patientFields, true);
        } else {
            displayFields(patientFields, false);
        }
        if (userTypes.includes('parent')) {
            displayFields(parentFields, true);
        } else {
            displayFields(parentFields, false);
        }
        if (userTypes.length === 0) {
            displayFields(patientFields.concat(parentFields), false);
        }
    }
    userTypeCheckboxes.forEach(function(checkbox) {
        checkbox.addEventListener('change', toggleFields);
    });
    toggleFields();
});