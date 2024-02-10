$(document).ready(function() {
    // Disable the buttons initially
    $('#direct').disabled = true;
    $('#group').disabled = true;
    // Enable both buttons if 1 user selected

    // Disable direct message button if multiple users selected
    $('#id_users').change(function() {
      if ($(this).val().length == 0) {
        $('#direct').disabled = true;
        $('#group').disabled = true;
      } else if ($(this).val().length == 1) {
        $('#direct').disabled = false;
        $('#group').disabled = false;
      } else {
        $('#direct').disabled = true;
        $('#group').disabled = false;
      }
    });
  });
