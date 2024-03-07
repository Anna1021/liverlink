document.addEventListener('DOMContentLoaded', function() {
    
    const feedTypeInput = document.getElementById('feedType');
  
    toggleFeedButton.addEventListener('click', function() {
      if (feedTypeInput.value === 'global') {
        feedTypeInput.value = 'friends';
      } else {
        feedTypeInput.value = 'global';
      }
  
      // Submit the form when the button is clicked
      document.getElementById('feedForm').submit();
    });
  });
  