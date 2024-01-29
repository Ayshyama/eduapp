document.addEventListener('DOMContentLoaded', (event) => {
    const messages = document.querySelectorAll('.messages');
    messages.forEach((messageContainer) => {
        const messageAlert = messageContainer.querySelector('.alert');
        if (messageAlert) {
            const spanElement = messageContainer.querySelector('.messages span');
            if (messageAlert.classList.contains('alert-success')) {
                spanElement.style.border = '1px solid rgba(1, 255, 84, 0.55)';
            } else if (messageAlert.classList.contains('alert-warning')) {
                spanElement.style.border = '1px solid rgba(255,217,0,0.65)';
            } else if (messageAlert.classList.contains('alert-danger')) {
                spanElement.style.border = '1px solid rgba(255,52,52,0.65)';
            }
        }
    });
});

document.addEventListener('DOMContentLoaded', (event) => {
    const closeButtons = document.querySelectorAll('.nav__close-message');

    closeButtons.forEach((closeButton) => {
        closeButton.addEventListener('click', function() {
            const messageContainer = this.closest('.messages');
            if (messageContainer) {
                messageContainer.style.animation = 'moveOut 1.5s cubic-bezier(.36, 0, .06, 1) forwards';
            }
        });
    });
});
