/**
 * Activates the stripe integration
 * @param {string} stripe_publishable_key 
 * @param {boolean} allow_go_to_starter 
 */
var stripe_integration_init = function(stripe_publishable_key, allow_go_to_starter) {
    // make some thin wrappers around the stripe api
    // which return faked id's when we do not have a publishable key]
    
    var stripe;

    var create_token = function(data) {
        if (!stripe_publishable_key)
            return Promise.resolve({ token: { id: 'fake-token-id' } });
        
        return stripe.createToken(data);
    }

    var create_source = function(element, data) {
        if (!stripe_publishable_key)
            return Promise.resolve({ source: { id: 'fake-source-id' }});
        
        return stripe.createSource(element, data);
    }


    // create an error elemenet
    var errorElement = document.getElementById('card-errors');
    var set_error = function(message){
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
    set_error();

    // initialize stripe API, either with the real key or an obviously fake one for testing
    // when initializing fails, bail out
    try {
        stripe = Stripe(stripe_publishable_key || 'fake' );
    } catch(e) {
        set_error('Unable to communicate with our payment provider. Please check your network connection. Contact support if the problem persists. ');
        $("#stripe-iban-elements").hide();
        $("#stripe-card-elements").hide();
        return;
    }

    var elements = stripe.elements();

    // custom element style
    var style = {
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

    // function to be called when everything is ready
    var cardReady = false;
    var ibanReady = false;
    var updateReadyState = function(mode) {
        if (mode === 'card') cardReady = true;
        if (mode === 'iban') ibanReady = true;
        if (cardReady && ibanReady) {
            document.getElementById('button_id_presubmit').removeAttribute('disabled');
            if (allow_go_to_starter) {
                starterButton.removeAttribute('disabled');
            }
        }
    }

    
    // Create a card element
    var card = elements.create('card', { style: style });
    card.addEventListener('ready', function() { updateReadyState('card'); });
    card.mount('#card-element');

    // Create an iban element
    var iban = elements.create('iban', { style: style, supportedCountries: ['SEPA'] });
    card.addEventListener('ready', function() { updateReadyState('iban')});
    iban.mount('#iban-element');

    // handle change errors properly
    var handleChangeErrors = function(event) {
        set_error(event.error ? event.error.message : undefined);
    }
    card.addEventListener('change', handleChangeErrors);
    iban.addEventListener('change', handleChangeErrors);

    // handle changing of payment type
    var paymentElement = $('#id_payment_type');
    paymentElement.change(function () {
        // clear out the error
        set_error(undefined);

        // and switch accordingly
        var selected = $(this).find(':selected').val();
        if (selected === 'card') {
            $("#stripe-card-elements").show();
            $("#stripe-iban-elements").hide();
        } else {
            $("#stripe-card-elements").hide();
            $("#stripe-iban-elements").show();
        }
    }).trigger('change');


    // Handle form submission
    var form = document.getElementById('payment-form');
    form.addEventListener('submit', function (event) {
        event.preventDefault();

        // grab the payment type
        ptype = paymentElement.val();
        if (ptype == 'card') {
            submitCard();
        } else if ( ptype == 'sepa' ) {
            submitSepa();
        } else {
            set_error('Something went wrong, please try again later or contact support. ')
        }
    });

    // create a starter button
    var starterButton;
    if (allow_go_to_starter) {
        starterButton = document.getElementById('button_id_starter');
        starterButton.addEventListener('click', function(event){
            event.preventDefault();
            
            submitForm(undefined, undefined, true);
        });
    }

    // handle submitting a card
    var submitCard = function() {
        create_token(card).then(function(result) {
            if (result.error) {
                set_error(result.error.message);
                return;
            }
            
            submitForm(result.token.id, undefined, false);
        });
    };
    
    // handle submitting a sepa token
    var submitSepa = function() {
        create_source(iban, {
            type: 'sepa_debit',
            currency: 'eur',
            owner: {
                name: document.getElementById('name').value
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

    var submitForm = function(card_token, source_id, go_to_starter) {
        // unmount both elements to be sure they do not leak
        // any data to the server
        card.unmount();
        iban.unmount();

        // fill form data
        document.getElementById('id_card_token').value = card_token || '';
        document.getElementById('id_source_id').value = source_id || '';
        document.getElementById('name').value = '';
        if (allow_go_to_starter) {
            document.getElementById('id_go_to_starter').value = go_to_starter ? 'true' : '';
        }

        // and submit the form
        document.getElementById("payment-form").submit();
    }
};