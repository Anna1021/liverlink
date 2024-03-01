$(document).ready(function() {

    hideBlockedMessages()

    $('#conversation').animate(
        {scrollTop:$('#conversation').prop('scrollHeight')});

    function hideBlockedMessages(){
        var blocked_messages = document.getElementsByName('blocked-message');

        for (var i = 0; i < blocked_messages.length; ++i) {
            var message = blocked_messages[i]
            message.innerHTML = "You have blocked this user. Click to reveal text."
            message.addEventListener('click', function() {
                var message_text = message.getAttribute('data-text')
                message.innerHTML = message_text
                message.classList.remove('text-muted')
            })
        }
    }
});

