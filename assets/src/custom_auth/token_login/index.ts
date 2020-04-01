// Automatically render the login view
document.addEventListener('DOMContentLoaded', function() {
    const tokenForm = document.getElementById('token_form');
    if (tokenForm === null) return;
    (tokenForm as HTMLFormElement).submit();
});
