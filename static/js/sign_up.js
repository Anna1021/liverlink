$(document).ready(function() {
    // Hide the fields initially
    $('#id_condition').parent().hide();
    $('#id_age_of_diagnosis').parent().hide();
    $('#id_child_condition').parent().hide();
    $('#id_child_age_of_diagnosis').parent().hide();
    $('#id_mentor_condition').parent().hide();
    $('#id_mentor_age_of_diagnosis').parent().hide();
  
    // Show or hide the fields when the user type changes
    $('#id_user_type').change(function() {
      if ($(this).val() == 'PT') {
        $('#id_condition').parent().show();
        $('#id_age_of_diagnosis').parent().show();
        $('#id_child_condition').parent().hide();
        $('#id_child_age_of_diagnosis').parent().hide();
        $('#id_mentor_condition').parent().hide();
        $('#id_mentor_age_of_diagnosis').parent().hide();
      } else if ($(this).val() == 'PR') {
        $('#id_condition').parent().hide();
        $('#id_age_of_diagnosis').parent().hide();
        $('#id_child_condition').parent().show();
        $('#id_child_age_of_diagnosis').parent().show();
        $('#id_mentor_condition').parent().hide();
        $('#id_mentor_age_of_diagnosis').parent().hide();
      } else if ($(this).val() == 'MT') {
        $('#id_condition').parent().hide();
        $('#id_age_of_diagnosis').parent().hide();
        $('#id_child_condition').parent().hide();
        $('#id_child_age_of_diagnosis').parent().hide();
        $('#id_mentor_condition').parent().show();
        $('#id_mentor_age_of_diagnosis').parent().show();
      } else {
        $('#id_condition').parent().hide();
        $('#id_age_of_diagnosis').parent().hide();
        $('#id_child_condition').parent().hide();
        $('#id_child_age_of_diagnosis').parent().hide();
      }
    });
  });

  $('#id_country').change(function() {
    var selectedCountry = $(this).val();
    if(selectedCountry) {
        $.ajax({
            url: '/get_cities/',
            data: {
                'country': selectedCountry
            },
            success: function (data) {
                $('#id_city').html(data);
            }
        });
    }
});