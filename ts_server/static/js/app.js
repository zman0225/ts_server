/* 
* @Author: ziyuanliu
* @Date:   2014-02-23 23:19:59
* @Last Modified by:   ziyuanliu
* @Last Modified time: 2014-02-28 10:34:30
*/

// regex yumminess
var username = "";
var emailRegex = /^(([^<>()[\]\\.,;:!\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
var usernameRegex = /^[a-z0-9_-]{5,16}$/; 
var passwordRegex = /^[a-z0-9_-]{5,16}$/; 
var ageRegex = /^(1[3-9]|[2-9][0-9])$/;

var username_valid = false;
var email_valid = false;
var password_valid = false;
var age_valid = false;
var gender_valid = false;

var preferences = [];
var meals = 0;
// create account submit button
EnableSubmit = function(val)
{
    enableCreateAccount();
}    

isNumber = function(n) {
  return !isNaN(parseFloat(n)) && isFinite(n);
}

clear_planner = function(){
	$("#description").empty();
	$("#recipe_picture").empty();
}

isInputsValid = function(){
	return (username_valid&&email_valid&&password_valid&&age_valid);
}

$('input[type="radio"]').on('select',function(){alert("text")});

togglePreference = function(con){
	var parent = (con.parentNode);
	var val = parent.value;
	if(isNumber(val)&&val!=0){
		console.log(val);
		(con.parentNode).className = "active"
		var temp = parent.previousSibling;
		meals = val;
		while(temp!=null){
			temp.className = ""
			temp = temp.previousSibling;
		}
		temp = parent.nextSibling;
		while(temp!=null){
			temp.className = ""
			temp = temp.nextSibling;
		}
		return;
	}

	var elem = con.innerHTML;
	// console.log($.inArray(elem,preferences));
	if ($.inArray(elem,preferences)==-1){
		(con.parentNode).className = "active"
		preferences.push(elem);
	}else{
		var index = preferences.indexOf(elem);
		if(index>-1){
			preferences.splice(index,1);
			(con.parentNode).className = ""
		}
	}
	console.log("pref is now "+preferences);
}


preference_callback = function(response){
	if (response["return"]==true){
		$("#preference_container").empty();
    	$.each( response['packet']['categories'], function( index, value ){
    		var li = $('<li></li>');
    		var al = $('<a onclick="togglePreference(this);"></a>');
    		al.html(value);
    		li.append(al);
		    $("#preference_container").append(li);
		});
		// empty the choices
		var tmp = $('#meals_ul')[0];
		var children = tmp.children;
		Array.prototype.slice.call(children).forEach(function(entry) {
		    entry.className="";
		});
		// load the presets
    	var packet = {};
		var placeholder = {};
		$('.main').text(username+"'s Preferences");
		placeholder.values="";
        packet.get_preferences = placeholder;
        var jsonPacket = JSON.stringify(packet);
        AjaxRequest(jsonPacket,get_preferences_callback);
	    }else{
	    	
	    }
}

$('#plannertab').on('click',function(){
	$("html, body").animate({ scrollTop: 0 }, "slow");
	$('#planner-table').hide();
	$('#load_bar_div').show(10);
	$('#load_bar').show();
	$('#planner_panel').height(160);
	clear_planner();
	

	$('#load_bar').animate({ width: "110%" },2500,function() {
	    
        $('#planner_panel').animate({height:600},1000);
        $('#planner-table').show(1500, function(){
        	$('#load_bar_div').hide(1000);
        	$('#planner_panel').animate({height:580},500);
        	$('#load_bar').animate({ width: "0%" });
        	var packet = {};
	packet.generate_menu = {}
    packet.generate_menu.values = "";
    var jsonPacket = JSON.stringify(packet);
    AjaxRequest(jsonPacket,planner_callback);
        });
	  }
		
	  );

});

planner_callback = function(response){
	if (response["return"]==true){
		console.log(response);
		get_recipes(response["packet"]["plan"]);
	    }else{
	    	
	    }
}

get_recipes = function(rid){
	var packet = {};
	var placeholder = {};
	placeholder.rid = rid;
    packet.get_recipes = placeholder;
    var jsonPacket = JSON.stringify(packet);
    AjaxRequest(jsonPacket,recipes_callback);
}

get_image = function(recipe_name){
    var replaced = recipe_name.split(' ').join('+');
    var img = $('<img height="130" width="130" id="dynamic" class="null">');
	img.attr('src', "/image/"+replaced);
	var li = $('<th></th>');
	img.appendTo(li); 
	li.appendTo('#recipe_picture');
}

recipes_callback = function(response){
	if (response["return"]==true){
		console.log(response);
		$.each( response["packet"]["recipes"], function( index, value ){
			console.log(value);
				get_image(value['name']);

				var div = $('<div></div>');
				var h = $('<h4 style="position: relative;margin-top: 0;"></h4>');
				h.text(value['name']);

				var descrip = $('<p align="top"></p>');
				descrip.text(value['description']);
				var li = $('<th></th>');

				h.appendTo(div);
				descrip.appendTo(div);

				div.appendTo(li);
				li.appendTo('#description');
			});
		var packet = {};
		var placeholder = {};
    }else{
	    	
    }
}

preference_set_callback = function(response){
	if (response["return"]==true){
		console.log(response);
		$("#plannertab").trigger('click');
	    }else{
	    	
	    }
}

get_preferences_callback = function(response){
	if (response["return"]==true){
		preferences = [];
			console.log(response["packet"]["preference"]);
			console.log(response["packet"]["meals"]);
			meals = response["packet"]["meals"];
			if(meals!=0)
				$('li[value='+meals+']')[0].className="active"
			$.each( response["packet"]["preference"], function( index, value ){
				var child = $('a:contains("'+value+'")')[0];
				(child.parentNode).className='active';
	    		// $('input[type="button"][value="'+value+'"]').removeClass('btn-primary').addClass('btn-success');
	    		preferences.push(value);
			});
			
	    }else{
	    	
	    }
}

$('#preferencestab').on('click',
	function() {
		var packet = {};
		var placeholder = {};
		placeholder.values = "";
        packet.get_categories = placeholder;
        var jsonPacket = JSON.stringify(packet);
        AjaxRequest(jsonPacket,preference_callback);
});

$('#generate_menu').on('click',function(){
	var packet = {};
	var placeholder = {};
	placeholder.preference = preferences;
	placeholder.meals = meals;
    packet.set_preferences = placeholder;
    var jsonPacket = JSON.stringify(packet);
    // console.log(jsonPacket);
    if(preferences.length>0){
    	AjaxRequest(jsonPacket,preference_set_callback);
    }
});

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

ImageAjaxRequest = function(img_name,callback)
{
    request = $.ajax({
	    url: "/image/"+img_name,
	    type: "get",
	    contentType: "image/jpeg",
	    beforeSend: function(xhr) {
		      xhr.overrideMimeType( "text/plain; charset=x-user-defined" )
		  }
    });

    request.success(function (data){
	    // response = JSON.stringify(response); //{"return":false,"error":"Account already exists"}
	    callback(data);
	    
	});
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
	    	clearAllInputs();
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
	    	clearAllInputs();
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
	username = response["packet"]["display_name"];
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


// Utility functions
clearAllInputs = function(){
	$(':input').val('');
}

$( '#user_password' ).bind('keypress', function(e){
   if ( e.keyCode == 13 ) {
     $('#sign_in').trigger('click');
   }
 });




