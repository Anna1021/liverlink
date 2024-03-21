$(document).ready(function() {
    reported();

    function reported() {
        var reportedObjects = document.querySelectorAll('[data-reported="true"]');
        if (reportedObjects.length > 0) {
            reportedObjects.forEach(function(reportedObject) {
                reportedObject.innerHTML = "You have reported this. Click to reveal.";
                reportedObject.addEventListener('click', function() {
                    var questionText = reportedObject.getAttribute('data-text');
                    reportedObject.innerHTML = questionText;
                    reportedObject.classList.remove('text-muted');
                });
            });
        }
    }
});
