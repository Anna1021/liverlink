$(document).ready(function() {
    hideBlockedContent()

    function hideBlockedContent(){
        var blocked_content = document.querySelectorAll('[data-blocked="true"]');
        for (var i = 0; i < blocked_content.length; ++i) {
            let content = blocked_content[i]
            content.innerHTML = "You have blocked this user. Click to reveal text."
            content.addEventListener('click', function() {
                var content_text = content.getAttribute('data-text')
                content.innerHTML = content_text
                content.classList.remove('text-muted')
            }.bind(this, content))
        }
    }
});