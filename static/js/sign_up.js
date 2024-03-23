$(document).ready(function() {
  // Function to show or hide fields based on user type
    $('#id_referral_code').parent().hide();
  
  function showHideFields(userType) {
    if (userType == 'PF' || userType == 'MT') {
        $('#id_referral_code').parent().show();
    } else {
        $('#id_referral_code').parent().hide();
    }
  }

  // Function to handle user type change
  function handleUserTypeChange() {
      var userType = $(this).val();
      localStorage.setItem('userType', userType);
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

    