$(document).ready(function() {
    hideBlockedComments()

    function hideBlockedComments(){
        var blocked_comments = document.getElementsByName('blocked-comment');
        for (var i = 0; i < blocked_comments.length; ++i) {
            let comment = blocked_comments[i]
            comment.innerHTML = "You have blocked this user. Click to reveal text."
            comment.addEventListener('click', function() {
                var comment_text = comment.getAttribute('data-text')
                comment.innerHTML = comment_text
                comment.classList.remove('text-muted')
            }.bind(this, comment))
        }
    }
});