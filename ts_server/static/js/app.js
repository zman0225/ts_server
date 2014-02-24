/* 
* @Author: ziyuanliu
* @Date:   2014-02-23 23:19:59
* @Last Modified by:   ziyuanliu
* @Last Modified time: 2014-02-24 15:17:03
*/

// regex yumminess

var emailRegex = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
var usernameRegex = /^[a-z0-9_-]{5,16}$/; 
var passwordRegex = /^[a-z0-9_-]{5,16}$/; 
var ageRegex = /^(1[3-9]|[2-9][0-9])$/;

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

AjaxRequest = function(dataPacket,callback)
{
    request = $.ajax({
	    url: "/api",
	    type: "post",
	    data: dataPacket,
	    // xhrFields: {
	    //  withCredentials: true
	    // },
	    dataType: 'json'
    });

    request.success(function (response, textStatus, jqXHR){
	    // response = JSON.stringify(response); //{"return":false,"error":"Account already exists"}
	    callback(response);
	    
	});
}



register_callback = function(response){
	if (response["return"]==true){
	    	console.log("account created - login in now");
    		$('#myModal').modal('hide') 
	    	validate(response);
	    }else{
	    	$('#register_warning').text(response["error"]);
        	$("#register_warning").removeClass("hidden");
	    }
}

validation_callback = function(response){
	console.log(response);
	if (response["return"]==true){
    	validate(response);
	}else{
		$('#home').tab('show');
		unvalidate();
    	clear_cookies();
	}
}

login_callback = function(response){
	console.log(response);
	if (response["return"]==true){
	    	validate(response);
	    }else{
	    	$('#login_warning').text(response["error"]);
        	$("#login_warning").removeClass("hidden");
	    }
}


validate = function(response){
	$('.dropdown.open .dropdown-toggle').dropdown('toggle');
	$('#sign-in').addClass('hidden');
	$('#sign-up').addClass('hidden');
	$('#user-bar').removeClass('hidden');
	$('#display_name').text(response["packet"]["display_name"]);
	$('#preferences').removeClass('hidden');
	$('#planner').removeClass('hidden');
	$('#preferencestab').removeClass('hidden');
	$('#plannertab').removeClass('hidden');
}

unvalidate = function(){
	$('#sign-in').removeClass('hidden');
	$('#sign-up').removeClass('hidden');
	$('#user-bar').addClass('hidden');
	$('#preferences').addClass('hidden');
	$('#planner').addClass('hidden');
	$('#preferencestab').addClass('hidden');
	$('#plannertab').addClass('hidden');
	$('#display_name').text("");
}

validate_cookie = function(){
	var packet = {};
    packet.username = $('#user_username').val();
    packet.password = $('#user_password').val();
    var login = {};
    login.validate_cookie = packet;
    var jsonPacket = JSON.stringify(login);
    AjaxRequest(jsonPacket,validation_callback);
}

clear_cookies = function(){
	var cookies = document.cookie.split(";");
	for(var i=0; i < cookies.length; i++) {
	    var equals = cookies[i].indexOf("=");
	    var name = equals > -1 ? cookies[i].substr(0, equals) : cookies[i];
	    document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT";
	}
}

$('#logout').on("click",
 	function() {
 		clear_cookies();
 		unvalidate();
 		$('#myTab a[href="#home"]').tab('show')
    }
);

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
        AjaxRequest(jsonPacket,register_callback);
        
    }
);

$("#sign_in").on("click",
 	function() {
 		var packet = {};
        packet.username = $('#user_username').val();
        packet.password = $('#user_password').val();
        var login = {};
        login.login = packet;
        var jsonPacket = JSON.stringify(login);
        console.log(jsonPacket);
        AjaxRequest(jsonPacket,login_callback);
        
    }
);