$(document).ready(function () {
  var lightThemeLogo = '/static/images/Pulse-logo_black.png';
  var darkThemeLogo = '/static/images/pulseLogoCropped.png';
  var moonLogo = '/static/images/moon.png';
  var sunLogo = '/static/images/sun.png';
  var darkBackground = '/static/images/background2.png';
  var lightBackground = '/static/images/background_light.png';

  // Set image source based on theme and save to local storage
  function setImageSource(theme) {
    var logoImageSrc = theme === 'light-theme' ? lightThemeLogo : darkThemeLogo;
    var themeImageSrc = theme === 'light-theme' ? sunLogo : moonLogo;
    $('.img-fluid').attr('src', logoImageSrc);
    $('.theme-icon').attr('src', themeImageSrc);
    localStorage.setItem("currentLogo", logoImageSrc);
    localStorage.setItem("currentThemeLogo", themeImageSrc);
  }

  function setTheme(themeName) {
    let mainDiv = $("#main");
    mainDiv.removeClass();
    mainDiv.addClass(themeName);
    saveTheme(themeName);
  }

  function getCurrentTheme() {
    var themeSelected = $('#main').attr('class');
    console.log("themeSelected:", themeSelected);
    return themeSelected;
  }

  function saveTheme(themeName) {
    localStorage.setItem("currentTheme", themeName);
  }

  $('#theme').click(function() {
    var currentTheme = getCurrentTheme() === 'light-theme' ? 'dark-theme' : 'light-theme'; // Toggle theme
    setTheme(currentTheme); // Apply the theme
    setImageSource(currentTheme); // Update image sources accordingly
  });

  let storedTheme = localStorage.getItem("currentTheme");

  if (storedTheme) {
    setTheme(storedTheme);
    setImageSource(storedTheme); // Use stored theme to determine image source
  } else {
    var defaultTheme = 'light-theme'; // Default theme
    setTheme(defaultTheme);
    setImageSource(defaultTheme); // Use default theme to determine image source
  }
});
