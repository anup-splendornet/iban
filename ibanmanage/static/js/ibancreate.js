$(function() {

    jQuery.validator.addMethod("validName", function(value, element) {
        re = /^[a-zA-Z'\u00c0-\u017e]*$/;
        return this.optional(element) || re.test(value);
    }," Please enter characters only.");

    existingibanid = $("#existingibanid").val();

    $("form[id='iban_create_form']").validate({
        errorElement: "div",
        errorPlacement: function(error, element) {
            $("span.error.text-danger").hide();
            error.insertAfter(element);
        },
        rules: {
            first_name:{
                required:true,
                minlength:3,
                maxlength:80,
                validName : true,
            },
            last_name:{
                required:true,
                minlength:3,
                maxlength:80,
                validName : true,            
            },
            iban:{
                required:true,
                iban:true,
                minlength:4,
                maxlength:80,
                remote:{
                    url:"/ibanunique/",
                    type:"post",
                    dataType: "json",
                    data:{
                        "csrfmiddlewaretoken":$("input[name='csrfmiddlewaretoken']").val(),
                        "existingibanid":existingibanid
                    }
                }
            },
        },
        messages: {
            first_name:{
                required:"Please Enter First Name.",
                minlength:"Minimum 3 Characters Required.",
                maxlength:"Maximum 80 Characters Allowed.",
                validName:"Please Enter Valid First Name.",            
            },
            last_name:{
                required:"Please Enter Last Name.",
                minlength:"Minimum 3 Characters Required.",
                maxlength:"Maximum 80 Characters Allowed.",
                validName:"Please Enter Valid Last Name.",
            },
            iban:{
                required:"Please Enter Iban number.",
                iban:"Please specify a valid IBAN",
                minlength:"Minimum 4 Characters Required.",
                maxlength:"Maximum 80 Characters Allowed.",
                remote:"Iban already exist in database."
            }
        }
    });
});