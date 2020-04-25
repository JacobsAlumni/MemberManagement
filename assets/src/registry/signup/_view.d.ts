interface Window {
    readonly form_valid: {
        valid: boolean;
        values: {
            [key: string]: string | string[]
        }
        choices: {
            [key: string]: Array<[string, string]> | null
        }
        errors: {
            [key: string]: Array<{message: string; code: string;}>
        }
    };
}
