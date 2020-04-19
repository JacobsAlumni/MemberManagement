interface Window {
    readonly form_valid: {
        valid: boolean;
        values: {
            [key: string]: string
        }
        errors: {
            [key: string]: Array<{message: string; code: string;}>
        }
    };
}
