$(document).ready(function() {
    let msg = localStorage.getItem("message");
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
document.querySelector("#id_content").onkeyup = function (e) {
if (e.keyCode == 13) {
    document.querySelector("#send-message").click();
}
};
document.querySelector("#send-message").onclick = function (e) {
    if ($('#id_content').val() != ""){
        chatSocket.send(JSON.stringify());
    }
};
chatSocket.onmessage = function (e) {
    localStorage.setItem("message",$("#id_content").val());
    window.location.reload();
};