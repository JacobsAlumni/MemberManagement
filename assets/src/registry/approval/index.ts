const idEmail = document.getElementById('id_email') as HTMLInputElement;

(function(suggestion: string) {
    const button = document.createElement('button');
    idEmail.parentNode!.insertBefore(button, idEmail.nextSibling);

    button.className = 'uk-button uk-button-secondary uk-button-small';
    button.style.marginTop = '1em';
    button.appendChild(document.createTextNode(window.auto_email));
    
    button.addEventListener('click', function(e) {
        e.preventDefault();
        idEmail.value = suggestion;
    });
})(window.auto_email)
