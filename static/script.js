function showPopup(id) {
    document.getElementById(id).style.display = 'flex';
}

function hidePopup(id) {
    document.getElementById(id).style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function() {
    var flashMessages = document.querySelector('.flash-messages');
    if (flashMessages) {
        flashMessages.style.display = 'block';
        setTimeout(function() {
            flashMessages.style.display = 'none';
            }, 3000);
    }
});