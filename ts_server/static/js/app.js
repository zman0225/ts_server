/* 
* @Author: ziyuanliu
* @Date:   2014-02-23 23:19:59
* @Last Modified by:   ziyuanliu
* @Last Modified time: 2014-02-24 11:43:42
*/

// regex yumminess

var emailRegex = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
var usernameRegex = /^[a-z0-9_-]{5,16}$/; 
var passwordRegex = /^[a-z0-9_-]{5,16}$/; 
var ageRegex = /^([1][3-9]|9[0-9])$/;

var username_valid = false;
var email_valid = false;
var password_valid = false;
var age_valid = false;
var gender_valid = false;

// create account submit button
EnableSubmit = function(val)
{
    enableCreateAccount();
}    

isInputsValid = function(){
	return (username_valid&&email_valid&&password_valid&&age_valid);
}

$('input[type="radio"]').on('select',function(){alert("text")});

enableCreateAccount = function(){
	var sbmt = document.getElementById("create_account");
	// console.log(isInputsValid());
	if(isInputsValid()&&($('#TOS:checked').length>0)&&(typeof($('input[type="radio"]:checked').val())!= "undefined")){
		console.log("valid");
		sbmt.disabled = false;
    }
    else
    {
        sbmt.disabled = true;
    }
}

// validate the inputs
ValidateInput = function(val){
	switch($(val).attr('id')){
		case 'username':
			username_valid = GroupFormValidator(usernameRegex,val);
			break;
		case 'password':
			password_valid = GroupFormValidator(passwordRegex,val);
			break;
		case 'email':
			email_valid = GroupFormValidator(emailRegex,val);
			break;
		case 'user_age':
			age_valid = GroupFormValidator(ageRegex,val);
			break;
	}
	// console.log("this");
	enableCreateAccount();
}

GroupFormValidator = function(regex,val){
	var value = $(val).val();
	if(regex.test(value)){
		if($(val).parent().hasClass('has-error')){
			$(val).siblings('span:first').remove();				
			$(val).parent().removeClass('has-error').removeClass("has-feedback");
		}
		if(!$(val).parent().hasClass('has-success')){
			$(val).parent().append("<span style=\"top: -25px;right:18px;\" class=\"glyphicon glyphicon-ok form-control-feedback\"></span>");
			$(val).parent().addClass('has-success').addClass("has-feedback");
		}
		return true;
	}else{
		if($(val).parent().hasClass('has-success')){
			$(val).siblings('span:first').remove();
			$(val).parent().removeClass('has-success').removeClass("has-feedback");
		}
		if(!$(val).parent().hasClass('has-error')){
			$(val).parent().append("<span style=\"top: -25px;right:18px;\" class=\"glyphicon glyphicon-remove form-control-feedback\"></span>");
			$(val).parent().addClass('has-error').addClass("has-feedback");
		}
		return false;
	}
}

AjaxRequest = function(dataPacket)
{
    request = $.ajax({
	    url: "/",
	    type: "post",
	    data: dataPacket,
	    xhrFields: {
	     withCredentials: true
	    },
	    dataType: 'json'
    });

    request.success(function (response, textStatus, jqXHR){
	    response = JSON.stringify(response);
	    alert(String(response));
	});
}

 $( "#create_account" ).on("click",
 	function() {
 		var packet = {};
        packet.username = $('#username').val();
        packet.password = $('#password').val();
        packet.email = $('#email').val();
        packet.user_age = $('#user_age').val();
        packet.gender = $('input[type="radio"]:checked').val();
        var register={};
        register.register = packet;
        var jsonPacket = JSON.stringify(register);
        console.log(jsonPacket);
    }
);