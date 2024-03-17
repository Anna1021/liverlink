$(document).ready(function() {
    $('#id_users').mousedown(function(e){
        e.preventDefault();
        const option = e.target;
        option.selected = !option.selected;
        $(this).trigger('change');
    })
})