$(document).ready(function() {
  // Function to show or hide fields based on user type
    $('#id_condition').parent().hide();
    $('#id_age_of_diagnosis').parent().hide();
    $('#id_child_condition').parent().hide();
    $('#id_child_age_of_diagnosis').parent().hide();
    $('#id_condition').parent().hide();
    $('#id_age_of_diagnosis').parent().hide();
    $('#id_referral_code').parent().hide();
    
  function showHideFields(userType) {
      if (userType == 'PT') {
          $('#id_condition').parent().show();
          $('#id_age_of_diagnosis').parent().show();
          $('#id_child_condition').parent().hide();
          $('#id_child_age_of_diagnosis').parent().hide();
          $('#id_referral_code').parent().hide();
      } else if (userType == 'PR') {
          $('#id_condition').parent().hide();
          $('#id_age_of_diagnosis').parent().hide();
          $('#id_child_condition').parent().show();
          $('#id_child_age_of_diagnosis').parent().show();
          $('#id_referral_code').parent().hide();
      } else if (userType == 'MT') {
          $('#id_condition').parent().show();
          $('#id_age_of_diagnosis').parent().show();
          $('#id_child_condition').parent().hide();
          $('#id_child_age_of_diagnosis').parent().hide();
          $('#id_referral_code').parent().show();
      } else {
          $('#id_condition').parent().hide();
          $('#id_age_of_diagnosis').parent().hide();
          $('#id_child_condition').parent().hide();
          $('#id_child_age_of_diagnosis').parent().hide();
      }
  }

  // Function to handle user type change
  function handleUserTypeChange() {
      var userType = $(this).val();
      // Store the user type in local storage
      localStorage.setItem('userType', userType);
      // Show or hide fields based on the selected user type
      showHideFields(userType);
  }

  // Retrieve the user type from local storage and set it
  var storedUserType = localStorage.getItem('userType');
  if (storedUserType) {
      $('#id_user_type').val(storedUserType);
      showHideFields(storedUserType);
  }

  // Bind the change event to the user type selection
  $('#id_user_type').change(handleUserTypeChange);
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