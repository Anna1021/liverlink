$(document).ready(function() {
    let pageScroll = localStorage.getItem('pageScroll');
    if(pageScroll!=null) window.scrollTo(0,pageScroll);
    let msg = sessionStorage.getItem(storageKey);
    if (msg!=null) $('#id_content').val(msg);
    var currentUrl = window.location.href;
    setScroll();
    if (currentUrl.indexOf('?') === -1) {
        var newUrl = currentUrl + '?first_message='+first_message;
        window.history.pushState({path: newUrl}, '', newUrl);
        if(window.innerWidth<= 770) $('#sidebar-toggle').prop('checked',true);
        window.location.reload();
    }
    if ($('#conversation').scrollTop()<$('#conversation').prop('scrollHeight')-($('#conversation').prop('clientHeight')+120)){
        $('#scroll-down').show();
    }
    let menuNotExpanded = localStorage.getItem('sidebarExpanded');
    if(menuNotExpanded!=null && menuNotExpanded=="true") {
        $('#sidebar-toggle').prop('checked',true);
    } else{
        $('#sidebar-toggle').prop('checked',false);
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
const chatSocket = new WebSocket("wss://" + window.location.host + "/");
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
    localStorage.setItem('sidebarExpanded',$('#sidebar-toggle').prop('checked'))
    localStorage.setItem('pageScroll',window.scrollY)
    return '';
})