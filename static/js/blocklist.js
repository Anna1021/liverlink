$(document).ready(function () {
    $('.block-user-toggle-btn').click(function() {
        var userId = $(this).data('user-id');
        var action = $(this).attr('data-action');
        var button = $(this);
        if (action == 'unblock'){
            unblockUser(userId, button);
        }
        else {
            blockUser(userId, button)
        }
    });

    function unblockUser(userId, button) {
        $.ajax({
            url : unblockUserUrl.replace('0', userId),
            type: 'GET', 
            success: function() {
                button.removeClass('btn-unblock').addClass('btn-block');
                button.attr('data-action', 'block');
                button.text('Block'); 
            },
            error: function(xhr) {
                console.error(xhr.responseText);
                alert('Error: Unable to unblock user');
            }
        });
    }

    function blockUser(userId, button) {
        $.ajax({
            url : blockUserUrl.replace('0', userId),
            type: 'GET', 
            success: function() {
                button.removeClass('btn-block').addClass('btn-unblock');
                button.attr('data-action', 'unblock');
                button.text('Unblock'); 
            },
            error: function(xhr) {
                console.error(xhr.responseText);
                alert('Error: Unable to block user');
            }
        });
    }
    
    
});

