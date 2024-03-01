$(document).ready(function () {

    $('#block-link').click(function() {
        var userId = $(this).data('user-id');
        var action = $(this).attr('data-action');
        if (action == 'unblock-user'){
            unblockUser(userId);
        }
        else {
            blockUser(userId);
        }
    });

    function unblockUser(userId) {
        $.ajax({
            url : unblockUserUrl.replace('0', userId),
            type: 'GET', 
            success: function() {
                location.reload()
            },
            error: function(xhr) {
                console.error(xhr.responseText);
                alert('Error: Unable to unblock user');
            }
        });
    }

    function blockUser(userId) {
        $.ajax({
            url : blockUserUrl.replace('0', userId),
            type: 'GET', 
            success: function() {
                location.reload()
            },
            error: function(xhr) {
                console.error(xhr.responseText);
                alert('Error: Unable to block user');
            }
        });
    }
});

