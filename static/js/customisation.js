document.addEventListener('DOMContentLoaded', function() {
    var pictures = document.querySelectorAll('.picture-container img');
    var selectedPicturePath = '';

    // Add white border to selected picture
    pictures.forEach(function(picture) {
        picture.addEventListener('click', function() {
            pictures.forEach(function(pic) {
                pic.parentElement.classList.remove('picture-selected');
            });

            this.parentElement.classList.add('picture-selected');
            selectedPicturePath = this.src.substring(this.src.lastIndexOf('/', this.src.lastIndexOf('/') - 1) + 1);
        });
    });

    // Update profile picture
    document.getElementById('update-button').addEventListener('click', function() {
        var url = this.getAttribute('data-url');
        var csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({'profile_picture': selectedPicturePath })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Profile picture updated successfully!');
            } else {
                alert('Select a profile picture.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while updating profile picture.');
        });
    });
});
