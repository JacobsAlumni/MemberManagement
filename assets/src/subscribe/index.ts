import "./index.css";

// stripe instance
let stripe: stripe.Stripe;
let cardReady = false;
let ibanReady = false;
let card: stripe.elements.Element;
let iban: stripe.elements.Element;

// read a lot of html elements
const errorElement = document.getElementById('card-errors') as HTMLDivElement;
const ibanElements = document.getElementById('stripe-iban-elements') as HTMLDivElement;
const cardElements = document.getElementById('stripe-card-elements') as HTMLDivElement;
const presubmitButton = document.getElementById('button_id_presubmit') as HTMLButtonElement;
const starterButton = document.getElementById('button_id_starter') as HTMLButtonElement | null;
const paymentElement = document.getElementById('id_payment_type') as HTMLSelectElement;
const formElement = document.getElementById('payment-form') as HTMLFormElement;
const nameElement = document.getElementById('name') as HTMLInputElement;
const cardTokenElement = document.getElementById('id_card_token') as HTMLInputElement;
const sourceIDElement = document.getElementById('id_source_id') as HTMLInputElement;
const goToStarterElement = document.getElementById('id_go_to_starter') as HTMLInputElement | null;

/**
 * Creates a token from a stripe element
 * @param data 
 */
function create_token(element: stripe.elements.Element): Promise<{token?: {id: string}, error?: undefined} | {token?: undefined, error: stripe.Error}> {
    if (!window.stripe_publishable_key)
        return Promise.resolve({ token: { id: 'fake-token-id' } });
    
    return stripe.createToken(element).then(x => {
        if (x.error) return {'error': x.error};
        return {token: {id: x.token!.id}};
    });
}

/**
 * Creates a source from a stripe element
 */
function create_source(element: stripe.elements.Element, data: any): Promise<{source: {id: string}, error?: undefined} | {source?: undefined,error: stripe.Error}> {
    if (!window.stripe_publishable_key)
        return Promise.resolve({ source: { id: 'fake-source-id' }});
    
    return stripe.createSource(element, data).then(x => {
        if (x.error) return {'error': x.error};
        return {source: {id: x.source!.id}};
    });
}

// create an error elemenet
function set_error(message?: string){
    if (message) {
        errorElement.style.display = 'block';
        errorElement.style.visibility = 'visible';
        errorElement.textContent = message;
    } else {
        errorElement.style.display = 'none';
        errorElement.style.visibility = 'hidden';
        errorElement.textContent = '';
    }
}


function updateReadyState(mode: 'card' | 'iban') {
    if (mode === 'card') cardReady = true;
    if (mode === 'iban') ibanReady = true;
    if (cardReady && ibanReady) {
        presubmitButton.removeAttribute('disabled');
        if (window.allow_go_to_starter && starterButton) {
            starterButton.removeAttribute('disabled');
        }
    }
}

function handleChangeError(event: any) {
    set_error(event.error ? event.error.message : undefined);
}

function handlePaymentChange() {
    set_error();
    
    const value = paymentElement.options[paymentElement.selectedIndex].value;
    if (value === 'card') {
        cardElements.style.display = 'block';
        ibanElements.style.display = 'none';
    } else {
        cardElements.style.display = 'none';
        ibanElements.style.display = 'block';
    }
}


function handleFormSubmit(event: Event) {
    event.preventDefault();

    const value = paymentElement.options[paymentElement.selectedIndex].value;
    if (value === 'card') {
        submitCard();
    } else if ( value === 'sepa' ) {
        submitSepa();
    } else {
        set_error('Something went wrong, please try again later or contact support. ')
    }
}

// handle submitting a card
function submitCard() {
    create_token(card).then(function(result) {
        if (result.error) {
            set_error(result.error.message);
            return;
        }
        
        submitForm(result.token!.id, undefined, false);
    });
};
    
// handle submitting a sepa token
function submitSepa() {
    create_source(iban, {
        type: 'sepa_debit',
        currency: 'eur',
        owner: {
            name: nameElement.value,
        },
        mandate: {},
    }).then(function(result) {
        if (result.error) {
            set_error(result.error.message);
            return;
        }

        submitForm(undefined, result.source.id, false);
    })
};

function submitForm(card_token?: string, source_id?: string, go_to_starter?: boolean) {
    // unmount both elements to be sure they do not leak
    // any data to the server
    card.unmount();
    iban.unmount();

    // fill form data
    cardTokenElement.value = card_token || '';
    sourceIDElement.value = source_id || '';
    nameElement.value = '';
    if (window.allow_go_to_starter && goToStarterElement) {
        goToStarterElement.value = go_to_starter ? 'true' : '';
    }

    // and submit the form
    formElement.submit();
}

(function() {
    set_error();

    // initialize stripe API, either with the real key or an obviously fake one for testing
    // when initializing fails, bail out
    try {
        stripe = Stripe(window.stripe_publishable_key || 'fake' );
    } catch(e) {
        set_error('Unable to communicate with our payment provider. Please check your network connection. Contact support if the problem persists. ');
        ibanElements.style.display = 'none';
        cardElements.style.display = 'none';
    }

    const elements = stripe!.elements();

    // custom element style
    const style = {
        base: {
            color: '#32325d',
            fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
            fontSmoothing: 'antialiased',
            fontSize: '16px',
            '::placeholder': {
                color: '#aab7c4'
            }
        },
        invalid: {
            color: '#fa755a',
            iconColor: '#fa755a'
        }
    };

    // Create a card element
    card = elements.create('card', { style: style });
    card.addEventListener('ready', () => updateReadyState('card'));
    card.mount('#card-element');
    card.addEventListener('change', handleChangeError);

    // Create an iban element
    iban = elements.create('iban', { style: style, supportedCountries: ['SEPA'] });
    card.addEventListener('ready', () => updateReadyState('iban'));
    iban.mount('#iban-element');
    iban.addEventListener('change', handleChangeError);

    // handle the changing of the errors
    paymentElement.addEventListener('change', handlePaymentChange);
    handlePaymentChange();

    // handle the form submission
    formElement.addEventListener('submit', handleFormSubmit);
    
    // handle starter form submission
    if (window.allow_go_to_starter && starterButton) {
        starterButton.addEventListener('click', (event: Event) => {
            event.preventDefault();
            
            submitForm(undefined, undefined, true);
        });
    }
})();