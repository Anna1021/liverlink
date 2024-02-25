window.addEventListener('pageshow', function(event) {
  if (event.persisted) {
    //Reloads the page if navigation arrows are used to show widget
    window.location.reload();
  }
});


function googleTranslateElementInit() {
  new google.translate.TranslateElement({pageLanguage: 'auto'}, 'google_translate_element');
}
