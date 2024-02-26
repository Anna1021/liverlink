document.addEventListener('DOMContentLoaded', function() {
    var lightThemeLogo = '/static/images/Pulse-logo_black.png';
    var darkThemeLogo = '/static/images/pulseLogoCropped.png';
  
    document.getElementById("theme-switcher").onchange = function(event) {
      var theme = event.target.value;
      var bodyElement = document.body;
      var mainNavbar = document.querySelector('.navbar');
      var leftNavbar = document.querySelector('.card');
      var feedCard = document.querySelector('.col-md-9 .card'); 
      var welcomeText = document.querySelector('.col-md-9 .card h1'); 
      var welcomeUserText = document.querySelector('.card-header .card-title');
      var buttons = document.querySelectorAll('.btn');

      bodyElement.classList.toggle("light-theme", theme === 'light-theme');
      bodyElement.classList.toggle("dark-theme", theme === 'dark-theme');
      mainNavbar.classList.toggle('navbar-light', theme === 'light-theme');
      mainNavbar.classList.toggle('bg-light', theme === 'light-theme');
      mainNavbar.classList.toggle('navbar-dark', theme === 'dark-theme');
      mainNavbar.classList.toggle('bg-dark', theme === 'dark-theme');
      leftNavbar.classList.toggle('bg-light', theme === 'light-theme');
      leftNavbar.classList.toggle('bg-dark', theme === 'dark-theme');
      feedCard.classList.toggle('bg-light', theme === 'light-theme');
      feedCard.classList.toggle('bg-dark', theme === 'dark-theme');
      welcomeText.classList.toggle('text-dark', theme === 'light-theme');
      welcomeText.classList.toggle('text-light', theme === 'dark-theme');
      welcomeUserText.classList.toggle('text-dark', theme === 'light-theme');
      welcomeUserText.classList.toggle('text-light', theme === 'dark-theme');

      var logoImage = document.querySelector('.img-fluid');
      logoImage.src = (theme === 'light-theme' ? lightThemeLogo : darkThemeLogo);

      buttons.forEach(function(button) {
        button.classList.toggle('btn-outline-dark', theme === 'light-theme');
        button.classList.toggle('btn-outline-light', theme === 'dark-theme');
      });
    };
  });
  