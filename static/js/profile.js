$(document).ready(function () {

    $('#block-link').click(function() {
        var userId = $(this).data('user-id');
        var action = $(this).attr('data-action');
        var a_element = $(this);
        if (action == 'unblock-user'){
            unblockUser(userId, a_element);
        }
        else {
            blockUser(userId, a_element);
        }
    });

    function unblockUser(userId, a_element) {
        $.ajax({
            url : unblockUserUrl.replace('0', userId),
            type: 'GET', 
            success: function() {
                a_element.attr('data-action', 'block-user');
                a_element.text('Block this user');
            },
            error: function(xhr) {
                console.error(xhr.responseText);
                alert('Error: Unable to unblock user');
            }
        });
    }

    function blockUser(userId, a_element) {
        $.ajax({
            url : blockUserUrl.replace('0', userId),
            type: 'GET', 
            success: function() {
                a_element.attr('data-action', 'unblock-user');
                a_element.text('Unblock this user'); 
            },
            error: function(xhr) {
                console.error(xhr.responseText);
                alert('Error: Unable to block user');
            }
        });
    }
});

