import { Vue, Prop } from 'vue-property-decorator';
import { submitForm, submitFormAjax } from "./form";
import debounce from "./debounce";

/** The result of a validation REST API Call */
export interface ValidateResult {
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
}
/** A class that implements a validatable form */
export default abstract class FormVueValidatable extends Vue {

    /** initial validation result */
    @Prop({type: Object, required: false, default: () => ({valid: false, errors: {}})})
    readonly initialValidationResult!: ValidateResult

    /* holds the current validation result */
    validateResult: ValidateResult = this.initialValidationResult;

    /** function to get the current instance of the form to validate */
    abstract get formInstance(): HTMLFormElement

    /** the list of form keys to send to the server. If undefined, sends all form keys to the server */
    abstract readonly formKeys: string[] | null;

    /** the endpoint to send validate requests to. Mandatory */
    abstract readonly validateEndpoint: string;

    /** the endpoint to submit requests to. If undefined, uses the action="" parameter of the Form */
    abstract readonly submitEndpoint: string | null;

    /** Submits the form if it is valid */
    submitForm = async () => {
        const validation = await this.validateForm();
        // For debugging: Force submit
        (window as any).forceSubmit = () => { submitForm(this.formInstance, this.submitEndpoint, this.formKeys); }
        if (validation.valid) {
            submitForm(this.formInstance, this.submitEndpoint, this.formKeys);
        }
    }

    /** Makes a validation request for this form, and then returns the result */
    validateForm = async (): Promise<ValidateResult> => {
        const validated = await submitFormAjax<ValidateResult>(this.formInstance, this.validateEndpoint, this.formKeys);
        this.validateResult = validated;
        return validated;
    }

    // timer to debounce validate requests with
    readonly debounceValidateTimer = 200;
    validateFormDebounced = debounce(this.validateForm.bind(this), this.debounceValidateTimer);
}