$(document).ready(function() {
    var currentUrl = window.location.href;
    if (currentUrl.indexOf('?') === -1) {
        var newUrl = currentUrl + '?first_message='+first_message;
        window.history.pushState({path: newUrl}, '', newUrl);
        window.location.reload();
    }
    let msg = sessionStorage.getItem(storageKey);
    if (msg!=null) $('#id_content').val(msg);
    hideBlockedMessages()
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
    setInterval(function(){
        if (conversation_id!="0"){
            sessionStorage.setItem(storageKey,$("#id_content").val())
        }
    },2000)
    window.addEventListener('beforeunload', function() {
        sessionStorage.setItem('scrollPosition', window.scrollY);
    });
    window.addEventListener('load', function() {
        var scrollPosition = sessionStorage.getItem('scrollPosition');
        if (scrollPosition !== null && currentUrl !== this.document.referrer) {
            window.scrollTo(0, parseInt(scrollPosition));
            sessionStorage.removeItem('scrollPosition');
        }
    });
});

const chatSocket = new WebSocket("ws://" + window.location.host + "/");
if(conversation_id!=0){
    document.querySelector("#id_content").focus();
    document.querySelector('#message-form').addEventListener("submit", function(){
        chatSocket.send(JSON.stringify({sender:username,conversation_id:conversation_id}));
        sessionStorage.clear();
    })
    let delete_buttons = document.querySelectorAll(".delete_all")
    delete_buttons.forEach(function(button){
        button.addEventListener("click",function(){
            chatSocket.send(JSON.stringify({sender:username,conversation_id:conversation_id}));
        })
    })
}
chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    let usernames = data.users.split("', '");
    if (usernames.includes(username) && username != data.sender){
        reloadPage();
    }
};

function reloadPage(){
    sessionStorage.setItem(storageKey,$("#id_content").val());
    sessionStorage.setItem('noScroll',true);
    window.location.reload();
}