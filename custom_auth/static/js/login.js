document.addEventListener('DOMContentLoaded', function () {
    function getCookie(name) {
        var nameEQ = name + "=";
        var ca = document.cookie.split(';');
        for (var i = 0; i < ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0) == ' ') c = c.substring(1, c.length);
            if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
        }
        return null;
    }

    function handleGoogleLogin(user) {
        var loginBtn = document.getElementById('g-signin')
        var loginText = document.getElementById('g-signin-text')

        var token = user.getAuthResponse().id_token
        var firstName = user.getBasicProfile().getGivenName()

        // Update presentation to let user know they're being logged in
        loginText.innerText = 'Hi ' + firstName + '!'
        loginBtn.disabled = true



        var csrftoken = getCookie('csrftoken');
        var headers = new Headers();
        headers.append('X-CSRFToken', csrftoken);
        headers.append("Content-Type", "application/x-www-form-urlencoded");

        fetch(login_script_settings.token_endpoint, {
            method: 'POST',
            body: 'token=' + token,
            headers: headers
        }).then(function (response) {
            if (response.ok === true && response.status === 200) {
                if (login_script_settings.next !== '') {
                    window.location.assign(login_script_settings.next)
                } else {
                    window.location.assign('/')
                }
            } else {
                window.location.reload()
            }
        })
    }

    // Attach to window so async Google script can call this
    window.init = function init() {
        var signInButton = document.getElementById('g-signin')

        gapi.load('auth2', function () {
            // google_login_settings is filled with variables in Django template (global)
            gapi.auth2.init(google_login_settings).then(function () {
                var a = gapi.auth2.getAuthInstance();
                a.attachClickHandler('g-signin', { scope: 'email', longtitle: true }, handleGoogleLogin, function (error) {
                    console.log(error)
                    if (error.error !== 'popup_closed_by_user') {
                        alert("An unknown error occured.");
                    }
                });
                signInButton.disabled = false
            }).catch(function (e) { console.log(e) })
        });

    }
});