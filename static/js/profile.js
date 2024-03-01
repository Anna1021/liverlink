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

    $('#friend-link').click(function() {
        var userId = $(this).data('user-id');
        var action = $(this).attr('data-action');
        if (action == 'add-friend'){
            addFriend(userId);
        }
        else if (action == 'remove-friend'){
            removeFriend(userId);
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

    function addFriend(userId) {
        $.ajax({
            url : friendRequestUserUrl.replace('0', userId),
            type: 'GET', 
            success: function() {
                $('#friend-link').attr('data-action', 'inactive');
                $('#friend-link').text('Request sent');
                $('#friend-link').css('font-style', 'italic');
                $('#friend-link').removeAttr('href');
            },
            error: function(xhr) {
                console.error(xhr.responseText);
                alert('Error: Unable to send friend request');
            }
        });
    }

    function removeFriend(userId) {
        $.ajax({
            url : removeFriendUrl.replace('0', userId),
            type: 'GET', 
            success: function() {
                $('#friend-link').attr('data-action', 'add-friend');
                $('#friend-link').text('Add friend');
            },
            error: function(xhr) {
                console.error(xhr.responseText);
                alert('Error: Unable to remove friend');
            }
        });
    }
});

