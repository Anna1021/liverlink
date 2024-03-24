$(document).ready(function() {
    $('[data-toggle="tooltip"]').tooltip();
    $('.like-post').each(function() {
        var $this = $(this);
        var postId = $this.data('post-id');
        var csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

        $this.click(function(e) {
            e.preventDefault();

            if ($this.hasClass('request-in-progress')) {
                return;
            }

            $this.addClass('request-in-progress'); 

            $.ajax({
                url: likePostUrl.replace('0', postId),
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken
                },
                dataType: 'json',
                success: function(data) {
                    if (data.liked) {
                        $this.removeClass('bi-hand-thumbs-up').addClass('bi-hand-thumbs-up-fill');
                    } else {
                        $this.removeClass('bi-hand-thumbs-up-fill').addClass('bi-hand-thumbs-up');
                    }
                    var $likeCount = $('#like-count-' + postId);
                    $likeCount.text(data.like_count);
                },
                complete: function() {
                    $this.removeClass('request-in-progress');
                }
            });
        });
    });
});