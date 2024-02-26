var lightThemeLogo = '/static/images/Pulse-logo_black.png';
var darkThemeLogo = '/static/images/pulseLogoCropped.png';

document.getElementById("theme-switcher").onchange = function(event) {
  var theme = event.target.value;
  var bodyElement = document.body;
  var mainNavbar = document.querySelector('.navbar');
  var leftNavbar = document.querySelector('.card');
  var feedCard = document.querySelector('.col-md-9 .card'); 
  var welcomeText = document.querySelector('.col-md-9 .card h1'); 
  var buttons = document.querySelectorAll('.btn');

  bodyElement.className = theme;
  mainNavbar.className = 'navbar navbar-expand-lg ' + (theme === 'light-theme' ? 'navbar-light bg-light' : 'navbar-dark bg-dark');
  leftNavbar.className = 'card ' + (theme === 'light-theme' ? 'bg-light' : 'bg-dark');
  feedCard.className = 'card ' + (theme === 'light-theme' ? 'bg-light' : 'bg-dark');
  welcomeText.className = (theme === 'light-theme' ? 'text-dark' : 'text-light');

  var logoImage = document.querySelector('.img-fluid');
  logoImage.src = (theme === 'light-theme' ? lightThemeLogo : darkThemeLogo);

  buttons.forEach(function(button) {
    button.className = 'btn btn-lg ' + (theme === 'light-theme' ? 'btn-outline-dark' : 'btn-outline-light') + ' mb-3 w-100';
  });
};
