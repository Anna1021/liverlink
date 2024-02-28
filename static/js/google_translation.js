window.addEventListener('pageshow', function(event) {
  if (event.persisted) {
    //Reloads the page if navigation arrows are used to show widget
    window.location.reload();
  }
});

function googleTranslateElementInit() {
  new google.translate.TranslateElement({pageLanguage: 'auto'}, 'google_translate_element');
}

function loadGoogleTranslateScript() {
  var script = document.createElement('script');
  script.type = 'text/javascript';
  script.src = '//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
  document.body.appendChild(script);
}

//Always loads widget
window.onload = loadGoogleTranslateScript;