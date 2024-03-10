$(document).ready(function() {
    let msg = sessionStorage.getItem("message");
    if (msg!=null) $('#id_content').val(msg);
    
    $('#conversation').animate(
        {scrollTop:$('#conversation').prop('scrollHeight')});
});

const chatSocket = new WebSocket("ws://" + window.location.host + "/");
chatSocket.onopen = function (e) {
console.log("The connection was setup successfully !");
};
chatSocket.onclose = function (e) {
console.log("Something unexpected happened !");
};
document.querySelector("#id_content").focus();
document.querySelector('#message-form').addEventListener("submit", function(){
    chatSocket.send(JSON.stringify({sender:username}));
    sessionStorage.clear();
})
chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    if (username != data.sender){
        reloadPage();
    }
};

function reloadPage(){
    sessionStorage.setItem("message",$("#id_content").val());
    window.location.reload();
}