$(document).ready(function () {
    function setFont(fontName) {
      let mainDiv = $("#main-font");
      mainDiv.removeClass();
      mainDiv.addClass(fontName);
      saveFont(fontName);
    }
  
    function getCurrentFont() {
      var fontSelected = $("#font-selector").val();
      console.log("fontSelected:", fontSelected);
      return fontSelected;
    }
  
    function saveFont(fontName) {
      localStorage.setItem("currentFont", fontName);
    }
  
    function selectFont(fontName) {
      $("#font-selector").val(fontName);
    }
  
    $("#font-selector").change(function () {
      let currentFont = getCurrentFont();
      setFont(currentFont);
    });

    let storedFont = localStorage.getItem("currentFont");
    if (storedFont) {
      setFont(storedFont);
      selectFont(storedFont);
    } else {
      setFont(getCurrentFont());
    }
  });
  