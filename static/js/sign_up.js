$(document).ready(function() {
    $('#id_condition').parent().hide();
    $('#id_age_of_diagnosis').parent().hide();
    $('#id_child_condition').parent().hide();
    $('#id_child_age_of_diagnosis').parent().hide();
    $('#id_condition').parent().hide();
    $('#id_age_of_diagnosis').parent().hide();
    $('#id_referral_code').parent().hide();
    $('#id_transplant').parent().hide();
    $('#id_child_transplant').parent().hide();
  
    // Show or hide the fields when the user type changes
    $('#id_user_type').change(function() {
      if ($(this).val() == 'PT') {
        $('#id_condition').parent().show();
        $('#id_age_of_diagnosis').parent().show();
        $('#id_child_condition').parent().hide();
        $('#id_child_age_of_diagnosis').parent().hide();
        $('#id_referral_code').parent().hide();
        $('#id_transplant').parent().show();
        $('#id_child_transplant').parent().hide();
      } else if ($(this).val() == 'PR') {
        $('#id_condition').parent().hide();
        $('#id_age_of_diagnosis').parent().hide();
        $('#id_child_condition').parent().show();
        $('#id_child_age_of_diagnosis').parent().show();
        $('#id_referral_code').parent().hide();
        $('#id_transplant').parent().hide();
        $('#id_child_transplant').parent().show();
      } else if ($(this).val() == 'MT') {
        $('#id_condition').parent().show();
        $('#id_age_of_diagnosis').parent().show();
        $('#id_child_condition').parent().hide();
        $('#id_child_age_of_diagnosis').parent().hide();
        $('#id_referral_code').parent().show();
        $('#id_transplant').parent().show();
        $('#id_child_transplant').parent().hide();
      } else {
        $('#id_condition').parent().hide();
        $('#id_age_of_diagnosis').parent().hide();
        $('#id_child_condition').parent().hide();
        $('#id_child_age_of_diagnosis').parent().hide();
        $('#id_referral_code').parent().hide();
        $('#id_transplant').parent().hide();
        $('#id_child_transplant').parent().hide();
      }
    });
  });

    // Only show the hospital field if the user is from the United Kingdom
    $('#id_hospital').parent().hide();

    $('#id_location').change(function() {
      if ($(this).val() == 'GB') {
          $('#id_hospital').parent().show();
      } else {
          $('#id_hospital').parent().hide();
      }
    });