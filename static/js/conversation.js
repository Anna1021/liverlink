$(document).ready(function() {

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
var messageInput = document.querySelector(
    "#id_content"
).value;
chatSocket.send(JSON.stringify({ message: messageInput, sender:user}));
};
chatSocket.onmessage = function (e) {
    window.location.reload();
};