function toggle(b){
    if (b.innerHTML == 'Rename'){
        b.innerHTML = 'Cancel';
    } else{
        b.innerHTML = 'Rename';
    }
    let label = document.getElementById('conversation-name');
    let input = document.getElementById('conversation-name-input');
    if (b.innerHTML == 'Rename') {
        label.style.display = 'inline';
        input.style.display = 'none';
      } else {
        label.style.display = 'none';
        input.style.display = 'inline';
      }
}