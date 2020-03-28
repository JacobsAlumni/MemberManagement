interface Window {
    // login settings prefilled by Django code
    readonly google_login_settings: {
        client_id: string;
        hosted_domain: string;
        prompt: string;
    };
    // login script prefilled by Django code
    readonly login_script_settings: {
        next: string;
        token_endpoint: string;
    }
    // optionally settable init code
    init?: () => void;
}