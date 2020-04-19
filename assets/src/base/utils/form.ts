import getCookie from "./cookie";

/**
 * Turns a 
 * @param formData 
 * @param keys 
 */
function formData2URLSearchParams(formData: FormData, keys?: string[]): URLSearchParams {
    const params = new URLSearchParams();
    formData.forEach((v, key) => {
        // if we have some keys and the current key isn't in it, don't add it
        if(keys !== undefined && keys.indexOf(key) === -1) return;

        if(typeof v !== 'string') {
            console.warn('formData2URLSearchParams: File is not supported. ');
            return;
        }

        // else append it
        params.append(key, v);
    });
    return params;
}

/**
 * Submits a form via ajax
 * @param endpoint Endpoint to send form data to.
 * @param form HTML Form Element containing data to submit
 * @param keys Optional. Set of keys to submit. 
 */
export async function submitFormAjax<T extends {}>(form: HTMLFormElement, endpoint: string, keys?: string[]): Promise<T> {
    // we need a csrf token for this
    const csrftoken = getCookie('csrftoken');
    if (!csrftoken) throw new Error('no csrftoken cookie');

    // read formdata
    const params = formData2URLSearchParams(new FormData(form), keys);

    // make a request
    const response = await fetch(endpoint, {
        method: 'post',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: params.toString(),
    });

    // if the request failed, throw an error
    if (response.status !== 200)
        throw new Error("response.status !== 200");
    
    // return the validated json
    return (await response.json()) as T;
}

export async function submitForm(form: HTMLFormElement, endpoint?: string, keys?: string[]): Promise<void> {
    // create a new form element
    const newFormElement = document.createElement('form');
    newFormElement.setAttribute('method', 'POST');
    newFormElement.setAttribute('action', endpoint || form.getAttribute('action')!);

    // iterate over formdata and set all the values
    const formData = new FormData(form);
    formData.forEach((v, k) => {
        if(typeof v !== 'string') {
            console.warn('submitForm: File is not supported. ');
            return;
        }

        const newInput = document.createElement('input');
        newInput.setAttribute('type', 'hidden');
        newInput.setAttribute('name', k);
        newInput.setAttribute('value', v);
        newFormElement.appendChild(newInput);
    });

    // submit the form with all the magic data in it
    newFormElement.submit();
}