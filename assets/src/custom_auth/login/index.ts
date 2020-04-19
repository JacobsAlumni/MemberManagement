import "./index.css";
import getCookie from "../../base/utils/cookie";

/**
 * Workaround for Login Button not working properly
 * is to only load it onload, and also add it dynamically
 * see e.g. https://github.com/google/google-api-javascript-client/issues/397
 */
function loadGoogleAPI() {
    const scriptNode = document.createElement('script');
    scriptNode.src = "https://apis.google.com/js/platform.js?onload=init";
    scriptNode.type = 'text/javascript';
    scriptNode.charset = 'utf-8';
    document.getElementsByTagName('head')[0].appendChild(scriptNode);
}

document.addEventListener('DOMContentLoaded', function () {
    // grab element references from the page
    const loginBtn = document.getElementById('g-signin') as HTMLButtonElement;
    const loginText = document.getElementById('g-signin-text') as HTMLSpanElement;

    function handleGoogleLogin(user: gapi.auth2.GoogleUser) {
        const token = user.getAuthResponse().id_token;
        const givenName = user.getBasicProfile().getGivenName();

        // Update presentation to let user know they're being logged in
        loginText.innerText = 'Hi ' + givenName + '!';
        loginBtn.disabled = true;

        const csrftoken = getCookie('csrftoken');
        if (!csrftoken) throw new Error('no csrftoken cookie');

        fetch(window.login_script_settings.token_endpoint, {
            method: 'POST',
            body: 'token=' + token,
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        }).then(function (response) {
            const next = window.login_script_settings.next;

            // if the response isn't ok, don't do anything
            if (response.ok !== true || response.status !== 200) {
                if (next) {
                    window.location.assign('?next='+encodeURIComponent(next)+'&error=googlefail');
                } else {
                    window.location.assign('?error=googlefail')
                }
                return;
            }
            
            // go to the next url
            window.location.assign(next || '/');
        });
    }

    // Add an init handler
    window.init = function init() {
        gapi.load('auth2', function () {
            gapi.auth2.init(window.google_login_settings).then((a) => {
                a.attachClickHandler('g-signin', { scope: 'email' }, handleGoogleLogin, (error) => console.error(error));
                loginBtn.disabled = false;
            }).catch((e: Error) => console.log(e))
        });
    }

    // load the google api (unless we're in test mode)
    if(!window.jsTestModeFlag) loadGoogleAPI();
});