$(document).ready(function() {

    $('#conversation').animate(
        {scrollTop:$('#conversation').prop('scrollHeight')});
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

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