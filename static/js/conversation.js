$(document).ready(function() {
    let msg = sessionStorage.getItem("message");
    if (msg!=null) $('#id_content').val(msg);
    hideBlockedMessages()
    $('#conversation').animate(
        {scrollTop:$('#conversation').prop('scrollHeight')});
    function hideBlockedMessages(){
        var blocked_messages = document.getElementsByName('blocked-message');
        for (var i = 0; i < blocked_messages.length; ++i) {
            let message = blocked_messages[i]
            message.innerHTML = "You have blocked this user. Click to reveal text."
            message.addEventListener('click', function() {
                var message_text = message.getAttribute('data-text')
                message.innerHTML = message_text
                message.classList.remove('text-muted')
            }.bind(this, message))
        }
    }
});

const chatSocket = new WebSocket("ws://" + window.location.host + "/");
document.querySelector("#id_content").focus();
document.querySelector('#message-form').addEventListener("submit", function(){
    chatSocket.send(JSON.stringify({sender:username,conversation_id:conversation_id}));
    sessionStorage.clear();
})
chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    let usernames = data.users.split("', '");
    if (usernames.includes(username) && username != data.sender){
        reloadPage();
    }
};

function reloadPage(){
    sessionStorage.setItem("message",$("#id_content").val());
    window.location.reload();
}