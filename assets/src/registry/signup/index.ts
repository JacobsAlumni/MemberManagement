import SignUpForm from './SignUpForm.vue'

document.addEventListener('DOMContentLoaded', () => {
    new SignUpForm({
        el: '#signupform',
        propsData: {
            'initialValidationResult': JSON.parse(JSON.stringify(window.form_valid)),
        }
    })
});
