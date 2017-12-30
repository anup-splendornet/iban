$(document).ready(function(){

    // iban user form validations
    $('#userform').validate({
        rules: {
            first_name: {
                required: true,                
            },
            last_name: {
                required: true,                
            },
            bank_no: {
                required: true,                
            }
        },
        messages: {
            'first_name': {
                required: 'Please Enter First Name.'
            },
            'last_name': {
                required: 'Please Enter Last Name.'
            },
            'bank_no': {
                required: 'Please Enter Bank Number.',
            }
        }
    });
    
    
});