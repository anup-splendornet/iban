$(document).ready(function(){

    // iban user form validations
    $('#userForm').validate({
        rules: {
            first_name: {
                required: true,                
            },
            last_name: {
                required: true,                
            },
            iban_num: {
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
            'iban_num': {
                required: 'Please Enter IBAN Number.',                
            }
        }
    });
    
    
});