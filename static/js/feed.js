document.addEventListener('DOMContentLoaded', function() {
    const toggleFeedButton = document.getElementById('toggleFeedButton');
    const feedTypeInput = document.getElementById('feedType');
  
    toggleFeedButton.addEventListener('click', function() {
      if (feedTypeInput.value === 'global') {
        feedTypeInput.value = 'friends';
        toggleFeedButton.textContent = 'Friends Only Feed';
      } else {
        feedTypeInput.value = 'global';
        toggleFeedButton.textContent = 'Global Feed';
      }
  
      // Submit the form when the button is clicked
      document.getElementById('feedForm').submit();
    });
  });
  