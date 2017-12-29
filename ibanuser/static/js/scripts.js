$(document).ready(function(){

    // iban user form validations
    $('#ibanuserform').validate({
        rules: {
            first_name: {
                required: true,
                minlength: 3,
                maxlength: 100
            },
            last_name: {
                required: true,
                minlength: 3,
                maxlength: 100
            },
            iban: {
                required: true,
                iban: true
            }
        },
        messages: {
            'first_name': {
                required: 'Please Enter First Name.',
                minlength: jQuery.validator.format("Please enter atleast {0} characters."),
                maxlength: jQuery.validator.format("Please do not enter more than {0} characters."),
            },
            'last_name': {
                required: 'Please Enter Last Name.',
                minlength: jQuery.validator.format("Please enter atleast {0} characters."),
                maxlength: jQuery.validator.format("Please do not enter more than {0} characters."),
            },
            'iban': {
                required: 'Please Enter IBAN Number.',
                iban:"Please specify a valid IBAN.",
            }
        }
    });
    
});