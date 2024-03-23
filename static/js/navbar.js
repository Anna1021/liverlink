$(document).ready(function() {
    // Highlight the active button on page load
    var currentUrl = window.location.href;
    $('.navbar-item a').each(function() {
        if ($(this).attr('href') === currentUrl) {
            $(this).addClass('active');
        }
    });
});

