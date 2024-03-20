$(document).ready(function() {
    reported()

    function reported(){
        var reported_object = document.getElementById('reported');
        if (reported_object) {
            reported_object.innerHTML = "You have reported this. Click to reveal."
            reported_object.addEventListener('click', function() {
                var question_text = reported_object.getAttribute('data-text')
                reported_object.innerHTML = question_text
                reported_object.classList.remove('text-muted')
            })
        }
    }
});

