function confirmDeleteResponse(responseId) {
  if (confirm('Are you sure you want to delete this reply?')) {
    var csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    var actionUrl = '/delete_reply/' + responseId + '/';

    var form = document.createElement('form');
    form.method = 'POST';
    form.action = actionUrl;

    var csrfInput = document.createElement('input');
    csrfInput.type = 'hidden';
    csrfInput.name = 'csrfmiddlewaretoken';
    csrfInput.value = csrfToken;
    form.appendChild(csrfInput);

    document.body.appendChild(form);
    form.submit();
  }
}


