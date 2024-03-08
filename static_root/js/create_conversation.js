$(document).ready(function() {
    $('#direct').prop('disabled',true);
    $('#group').prop('disabled',true);

    // Enable both buttons if 1 user selected
    // Disable direct message button if multiple users selected
    $('#id_users').change(function() {
      if ($(this).val().length == 0) {
        $('#direct').prop('disabled',true);
        $('#group').prop('disabled',true);
      } else if ($(this).val().length == 1) {
        $('#direct').prop('disabled',false);
        $('#group').prop('disabled',false);
      } else {
        $('#direct').prop('disabled',true);
        $('#group').prop('disabled',false);
      }
    });
  });
