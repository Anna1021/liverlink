$(document).ready(function() {
    // Hide the fields initially
    $('#id_condition').parent().hide();
    $('#id_age_of_diagnosis').parent().hide();
    $('#id_child_condition').parent().hide();
    $('#id_child_age_of_diagnosis').parent().hide();
  
    // Show or hide the fields when the user type changes
    $('#id_user_type').change(function() {
      if ($(this).val() == 'PT') {
        $('#id_condition').parent().show();
        $('#id_age_of_diagnosis').parent().show();
        $('#id_child_condition').parent().hide();
        $('#id_child_age_of_diagnosis').parent().hide();
      } else if ($(this).val() == 'PR') {
        $('#id_condition').parent().hide();
        $('#id_age_of_diagnosis').parent().hide();
        $('#id_child_condition').parent().show();
        $('#id_child_age_of_diagnosis').parent().show();
      } else {
        $('#id_condition').parent().hide();
        $('#id_age_of_diagnosis').parent().hide();
        $('#id_child_condition').parent().hide();
        $('#id_child_age_of_diagnosis').parent().hide();
      }
    });

    $('#id_hospital').parent().hide();

    // Show or hide the hospital field based on location
    $('#id_location').change(function() {
      if ($(this).val() == 'GB') {  // Replace 'some_value' with the condition value
          $('#id_hospital').parent().show();
      } else {
          $('#id_hospital').parent().hide();
      }
  });
});