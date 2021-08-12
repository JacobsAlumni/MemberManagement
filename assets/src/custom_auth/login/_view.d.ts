interface CredentialResponse {
    credential: string;
    select_by: string;
    clientId: string;
}

interface Window {
    // login script prefilled by Django code
    readonly login_script_settings: {
        next: string;
        token_endpoint: string;
    }
    // optional callback function for google login, set by javascript
    handleGoogleLogin?: (response: CredentialResponse) => void;
}