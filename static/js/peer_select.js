$(document).ready(function () {
    $('.add-friend-btn').click(function() {
        var userId = $(this).data('user-id');
        var addButton = $(this);
        sendFriendRequest(userId, addButton);
    });

    function sendFriendRequest(userId, addButton) {
        $.ajax({
            url : sendFriendRequestUrl.replace('0', userId),
            type: 'GET', 
            success: function() {
                addButton.removeClass('btn-secondary').addClass('success_button');
                addButton.text('✓ Friend request sent'); 
            },
            error: function(xhr) {
                console.error(xhr.responseText);
                alert('Error: Unable to send friend request');
            }
        });
    }
    
    function hideAllConditionalFields() {
        $('#id_age_of_diagnosis_min').parent().hide();
        $('#id_age_of_diagnosis_max').parent().hide();
        $('#id_condition').parent().hide();
        $('#id_child_age_of_diagnosis_min').parent().hide();
        $('#id_child_age_of_diagnosis_max').parent().hide();
        $('#id_child_condition').parent().hide();
        $('#id_mentor_age_of_diagnosis_min').parent().hide();
        $('#id_mentor_age_of_diagnosis_max').parent().hide();
        $('#id_mentor_condition').parent().hide();
        $('#id_transplant').parent().hide();
        $('#id_child_transplant').parent().hide();
        $('#id_expertise').parent().hide();

    }

    hideAllConditionalFields();

    function updateFieldVisibility() {
        hideAllConditionalFields();

        // Check each user type checkbox to determine which fields to show
        $("input[name='user_type']").each(function () {
            if ($(this).is(':checked')) {
                var userType = $(this).val(); 
                if (userType === 'PT') {
                    $('#id_age_of_diagnosis_min').parent().show();
                    $('#id_age_of_diagnosis_max').parent().show();
                    $('#id_condition').parent().show();
                    $('#id_transplant').parent().show();
                } else if (userType === 'PR') {
                    $('#id_child_age_of_diagnosis_min').parent().show();
                    $('#id_child_age_of_diagnosis_max').parent().show();
                    $('#id_child_condition').parent().show();
                    $('#id_child_transplant').parent().show();
                } else if (userType === 'MT') {
                    $('#id_mentor_age_of_diagnosis_min').parent().show();
                    $('#id_mentor_age_of_diagnosis_max').parent().show();
                    $('#id_mentor_condition').parent().show();
                    $('#id_transplant').parent().show();
                } else if (userType === 'PF') {
                    $('#id_expertise').parent().show();
                }
            }
        });
    }

    // Bind the change event to user type checkboxes
    $("input[name='user_type']").change(updateFieldVisibility);

    // Initial call to set the correct visibility state based on the current checkbox state
    updateFieldVisibility();
});

