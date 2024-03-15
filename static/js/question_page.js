$(document).ready(function() {

    hideBlockedQuestion()
    hideBlockedReplies()

    function hideBlockedQuestion(){
        var question = document.getElementById('blocked-question');
        if (question) {
            question.innerHTML = "You have blocked this user. Click to reveal question."
            question.addEventListener('click', function() {
                var question_text = question.getAttribute('data-text')
                question.innerHTML = question_text
                question.classList.remove('text-muted')
            })
        }
    }

    function hideBlockedReplies(){
        var blocked_responses = document.getElementsByName('blocked-response');

        for (var i = 0; i < blocked_responses.length; ++i) {
            let response = blocked_responses[i];
            response.innerHTML = "You have blocked this user. Click to reveal response.";
            response.addEventListener('click', function() {
                var response_text = response.getAttribute('data-text');
                response.innerHTML = response_text;
                response.classList.remove('text-muted');
            }.bind(this, response));
        };
    }
});

