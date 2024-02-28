$(document).ready(function () {
  var lightThemeLogo = '/static/images/Pulse-logo_black.png';
  var darkThemeLogo ='/static/images/pulseLogoCropped.png';

  // Set image source based on theme and save to local storage
  function setImageSource(theme) {
    var logoImageSrc = theme === 'light-theme' ? lightThemeLogo : darkThemeLogo;
    $('.img-fluid').attr('src', logoImageSrc);
    localStorage.setItem("currentLogo", logoImageSrc);
  }

  $('#theme').change(function() {
    var theme = $(this).val();
    setTheme(theme);
    setImageSource(theme);
  });

  function setTheme(themeName) {
    let mainDiv = $("#main");
    mainDiv.removeClass();
    mainDiv.addClass(themeName);
    saveTheme(themeName);
  }

  function getCurrentTheme() {
    var themeSelected = $("#theme").val();
    console.log("themeSelected:", themeSelected);
    return themeSelected;
  }

  function saveTheme(themeName) {
    localStorage.setItem("currentTheme", themeName);
  }

  function selectTheme(themeName) {
    $("#theme").val(themeName);
  }

  let storedTheme = localStorage.getItem("currentTheme");
  let storedLogo = localStorage.getItem("currentLogo");

  if (storedTheme) {
    setTheme(storedTheme);
    selectTheme(storedTheme);
    setImageSource(storedTheme); // Use stored theme to determine image source
  } else {
    var currentTheme = getCurrentTheme();
    setTheme(currentTheme);
    setImageSource(currentTheme); // Use current theme to determine image source
  }
});
