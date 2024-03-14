$(document).ready(function () {
  var lightThemeLogo = '/static/images/Liver_Link_logo_black.png';
  var darkThemeLogo = '/static/images/LiverLinkLogoCropped.png';
  var darkBackground = '/static/images/background2.jpg';
  var lightBackground = '/static/images/background_light.jpg';

  // Set image source based on theme and save to local storage
  function setImageSource(theme) {
    var logoImageSrc = theme === 'light-theme' ? lightThemeLogo : darkThemeLogo;
    var backgroundImageSrc = theme === 'light-theme' ? lightBackground : darkBackground; // Determine the background image based on theme
    $('.img-fluid').attr('src', logoImageSrc);
    var className = theme === 'light-theme'? 'bi bi-moon-fill': 'bi bi-sun';
    $('#theme').removeClass();
    $('#theme').addClass(className);
    console.log('current class name:', className);
    $('body').css('background-image', 'url(' + backgroundImageSrc + ')'); // Set the background image
    localStorage.setItem("currentLogo", logoImageSrc);
    localStorage.setItem("currentThemeLogo", themeImageSrc);
    localStorage.setItem("currentBackground", backgroundImageSrc); 
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
    setTheme(currentTheme); 
    setImageSource(currentTheme); 
  });

  let storedTheme = localStorage.getItem("currentTheme");

  if (storedTheme) {
    setTheme(storedTheme);
    setImageSource(storedTheme); // Use stored theme to determine image source and background
  } else {
    var defaultTheme = 'dark-theme'; 
    setTheme(defaultTheme);
    setImageSource(defaultTheme); // Use default theme to determine image source and background
  }
});
