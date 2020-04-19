import getCookie from "./cookie";

/**
 * Turns a 
 * @param formData 
 * @param keys 
 */
function formData2URLSearchParams(formData: FormData, keys: string[] | null): URLSearchParams {
    const params = new URLSearchParams();
    formData.forEach((v, key) => {
        // if we have some keys and the current key isn't in it, don't add it
        if(keys !== null && keys.indexOf(key) === -1) return;

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
export async function submitFormAjax<T extends {}>(form: HTMLFormElement, endpoint: string, keys: string[] | null): Promise<T> {
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

export async function submitForm(form: HTMLFormElement, endpoint: string | null, keys?: string[] | null): Promise<void> {
    // create a new form element
    const newFormElement = document.createElement('form');
    newFormElement.setAttribute('method', 'POST');
    if (typeof endpoint === 'string') {
        newFormElement.setAttribute('action', endpoint);
    } else if (form.hasAttribute('action')) {
        const actionAttribute = form.getAttribute('action');
        if (typeof actionAttribute === 'string') {
            newFormElement.setAttribute('action', actionAttribute);
        }
    }

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

    // add the element to the body, and then submit it
    document.body.appendChild(newFormElement);
    newFormElement.submit();
}