$(document).ready(function() {
    let msg = sessionStorage.getItem(storageKey);
    if (msg!=null) $('#id_content').val(msg);
    var currentUrl = window.location.href;
    setScroll();
    if (currentUrl.indexOf('?') === -1) {
        var newUrl = currentUrl + '?first_message='+first_message;
        window.history.pushState({path: newUrl}, '', newUrl);
        window.location.reload();
    }
    hideBlockedMessages()
    if ($('#conversation').scrollTop()<$('#conversation').prop('scrollHeight')-($('#conversation').prop('clientHeight')+120)){
        $('#scroll-down').show();
    }
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
    function setScroll(){
        let scrollPos = 0;
        let previousUrl = document.referrer;
        if (sessionStorage.getItem(scrollKey)!==null) {
            if (sessionStorage.getItem(scrollKey)>$('#conversation').prop('clientHeight')+120) {
                scrollPos = sessionStorage.getItem(scrollKey);
            } else if (previousUrl.split("?")[0]==currentUrl.split("?")[0] && previousUrl.split("?")[1]!=currentUrl.split("?")[1]){
                if (previousUrl.split('=').length > 1 && currentUrl.split('=').length > 1){
                    scrollPos = sessionStorage.getItem(scrollKey);
                }
            } else if (previousUrl==currentUrl && previousUrl.split('=').length == 1){
                scrollPos = sessionStorage.getItem(scrollKey);
            }
        }  
        scrollPos = $('#conversation').prop('scrollHeight')-scrollPos;
        $('#conversation').scrollTop(scrollPos);
    }
    $('#conversation').scroll(function(){
        if ($(this).scrollTop()<$(this).prop('scrollHeight')-($('#conversation').prop('clientHeight')+120)){
            $('#scroll-down').show();
        }else{
            $('#scroll-down').hide();
        }
    })

});

function scrollDown(){
    $('#conversation').animate(
        {scrollTop:$('#conversation').prop('scrollHeight')}
    )
}

let posting = false;
const chatSocket = new WebSocket("ws://" + window.location.host + "/");
if(conversation_id!=0){
    document.querySelector("#id_content").focus();
    document.querySelector('#message-form').addEventListener("submit", function(){
        posting=true;
        chatSocket.send(JSON.stringify({sender:username,conversation_id:conversation_id}));
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
        window.location.reload();
    }
};


window.addEventListener('beforeunload', function(e){
    if (!posting){
        sessionStorage.setItem(storageKey,$("#id_content").val());
        sessionStorage.setItem(scrollKey,$('#conversation').prop('scrollHeight')-$('#conversation').scrollTop());
    }else{
        sessionStorage.clear();
    }
    return '';
})