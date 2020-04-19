import Vue from "vue";
import { submitForm, submitFormAjax } from "./form";
import debounce from "./debounce";

/** The result of a validation REST API Call */
interface ValidateResult {
    valid: boolean;
    errors: {
        [key: string]: Array<{message: string; code: string;}>
    }
}

/** A class that implements a validatable form */
export default abstract class VueValidatable extends Vue {

    /* holds the current validation result */
    validateResult: ValidateResult = {valid: false, errors: {}};

    /** function to get the current instance of the form to validate */
    abstract get formInstance(): HTMLFormElement

    /** the list of form keys to send to the server. If undefined, sends all form keys to the server */
    abstract readonly formKeys: string[] | undefined;

    /** the endpoint to send validate requests to. Mandatory */
    abstract readonly validateEndpoint: string;

    /** the endpoint to submit requests to. If undefined, uses the action="" parameter of the Form */
    abstract readonly submitEndpoint: string | undefined;

    /** Submits the form if it is valid */
    async submitForm() {
        const validation = await this.validateForm();
        if (validation.valid) {
            submitForm(this.formInstance, this.submitEndpoint, this.formKeys);
        }
    }

    /** Makes a validation request for this form, and then returns the result */
    async validateForm(): Promise<ValidateResult> {
        const validated = await submitFormAjax<ValidateResult>(this.formInstance, this.validateEndpoint, this.formKeys);
        this.validateResult = validated;
        return validated;
    }

    // timer to debounce validate requests with
    readonly debounceValidateTimer = 200;
    validateFormDebounced = debounce(this.validateForm.bind(this), this.debounceValidateTimer);
}