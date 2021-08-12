import "./index.css";
import getCookie from "../../base/utils/cookie";

/**
 * Workaround for Login Button not working properly
 * is to only load it onload, and also add it dynamically
 * see e.g. https://github.com/google/google-api-javascript-client/issues/397
 */
function loadGoogleAPI() {
    const scriptNode = document.createElement('script');
    scriptNode.src = "https://accounts.google.com/gsi/client";
    scriptNode.type = 'text/javascript';
    scriptNode.charset = 'utf-8';
    document.getElementsByTagName('head')[0].appendChild(scriptNode);
}

document.addEventListener('DOMContentLoaded', function () {
    window.handleGoogleLogin = function(response: CredentialResponse) {
        const csrftoken = getCookie('csrftoken');
        if (!csrftoken) throw new Error('no csrftoken cookie');

        fetch(window.login_script_settings.token_endpoint, {
            method: 'POST',
            body: 'token=' + response.credential,
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

    // load the google api (unless we're in test mode)
    if(!window.jsTestModeFlag) loadGoogleAPI();
});