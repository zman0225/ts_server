/* 
* @Author: ziyuanliu
* @Date:   2014-02-23 23:19:59
* @Last Modified by:   ziyuanliu
* @Last Modified time: 2014-03-07 00:09:21
*/

// regex yumminess
var username = "";
var emailRegex = /^(([^<>()[\]\\.,;:!\s@\"]+(\.[^<>()[\]\\.,;:!\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
var usernameRegex = /^[A-Za-z0-9_-]{5,10}$/; 
var passwordRegex = /^[A-Za-z0-9!@#$%^&*()_]{6,15}$/;
var ageRegex = /^(1[3-9]|[2-9][0-9])$/;

var username_valid = false;
var email_valid = false;
var password_valid = false;
var age_valid = false;
var gender_valid = false;

var preferences = [];
var meals = 0;
var menu_plan = null;
var needNew= false;
var subscribed = null;
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
	$("#days").empty();
	$('#planner-table').empty();
	$('#recipe-carousel').empty();
}

isInputsValid = function(){
	return (username_valid&&email_valid&&password_valid&&age_valid);
}

$('#subscribe-checkbox').on('switchChange', function (e, data) {
  var $element = $(data.el);
      value = data.value;
      subscribed = value;
      var packet = {};
	packet.set_subscribed = {}
    packet.set_subscribed.values = value;
    var jsonPacket = JSON.stringify(packet);
    AjaxRequest(jsonPacket,function(response){});
		console.log(value);
  		
});

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
		console.log(response);
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
		load_preference();

		$.each( preferences, function( index, value ){
				var child = $('a:contains("'+value+'")')[0];
				(child.parentNode).className='active';
	    		// $('input[type="button"][value="'+value+'"]').removeClass('btn-primary').addClass('btn-success');
	    		preferences.push(value);
			});
	    }else{
	    	
	    }
}

load_preference = function(){
	// load the presets
    	var packet = {};
		var placeholder = {};
		$('.main').text(username+"'s Preferences");
		placeholder.values="";
        packet.get_preferences = placeholder;
        var jsonPacket = JSON.stringify(packet);
        AjaxRequest(jsonPacket,get_preferences_callback);
}

$('#plannertab').on('click',function(){
	clear_planner();
	$("html, body").animate({ scrollTop: 0 }, "slow");
	$('#planner-table').hide();
	$('#generate_grocery').hide();
	$('#load_bar_div').show(10);
	$('#load_bar').show();
	$('#planner_panel').height(160);
	if(menu_plan!=null){
        		console.log(menu_plan.length);
        		clear_planner();
        		add_recipes_to_plan(menu_plan);
        	}else if(needNew==true){
        		menu_plan=null;
        		var packet = {};
				packet.generate_menu = {}
			    packet.generate_menu.values = "";
			    var jsonPacket = JSON.stringify(packet);
			    AjaxRequest(jsonPacket,planner_callback);
        	}else{
	        	var packet = {};
				packet.get_latest_plan = {}
			    packet.get_latest_plan.values = "";
			    var jsonPacket = JSON.stringify(packet);
			    AjaxRequest(jsonPacket,planner_callback);
		    }
	$('#load_bar').animate({ width: "110%" },400,function() {
	    
        $('#planner_panel').animate({height:600},1000);
        $('#planner-table').show(1500, function(){
        	$('#load_bar_div').hide(1000);
        	$('#planner_panel').animate({height:680},500);
        	$('#load_bar').animate({ width: "0%" });
        	$('.carousel').carousel('pause');

        	
		    $('#generate_grocery').show();
        });
	  }
		
	  );

});

planner_callback = function(response){
	if (response["return"]==true){
		get_recipes(response["packet"]["plan"]);
		needNew=false;
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

recipes_callback = function(response){
	if (response["return"]==true){
		menu_plan = response["packet"]["recipes"];
		add_recipes_to_plan(menu_plan);
    }else{
	    	
    }
}



bind_selector = function(sel){
	sel.click(function() {
		var ind = $(this).data("idx");
	    $('#recipe-carousel').children().each(function( index, value ){
	    	if(index==ind){
	    		$(this).addClass('active');
	    	}
	    	else{
	    		$(this).removeClass('active');
	    	}
	    });
	    $('#recipe_modal').modal('show');
	});
}

get_image = function(recipe_name){
    var replaced = recipe_name.split(' ').join('+');
    var img = $('<img id="dynamic">');
	img.attr('src', "/image/"+replaced);
	return img;
}

scroll_clicked = function(){
	console.log(($this));
}

add_recipes_to_plan = function(data){
	var ctr = 1;
	$.each( data, function( index, value ){
		var ul = $('<ul style="margin: 0 auto;"></ul>');
		$.each(value['ingredients'], function(k, v) {
		    //display the key and value pair
		    var li = $('<li style="margin:0!important; padding:0!important;"></li>');
		    li.append($('<p></p>').text(k + ' - ' + v));
		    ul.append(li);
		});

		var instr_ol = $('<ol style="margin: 0 auto;"></ol>');

		for (var i = 0; i < value['instructions'].length; i++){
			var lii = $('<li style="margin:0!important; padding:0!important;"></li>');
		    lii.append($('<p></p>').text(value['instructions'][i]));
		    instr_ol.append(lii);
		    console.log("asdas");
		}

		var day = "Day "+String(ctr);
		var a = get_image(value['name']);
		var name = $('<h4 style="color: #27ae60 !important;" ></h4>');
		name.text(value['name']);

		// will add recipe to the carousel 
		var master_div = $('<div class="item" style="height:500px;"></div>');
		var scroll_container = $('<div data-spy="scroll" data-target="#navbar'+String(ctr)+'" style="height: 100%;overflow-y: scroll;padding-top:12%;"></div>');
		var instruction_div = $('<div></div>');
		var pic_div = $('<div style="margin-left:30px;" align="center" "></div>'); pic_div.attr('id',String(ctr)+"pic");
		var ingr_div = $('<div style="margin-left:30px;"></div>'); ingr_div.attr('id',String(ctr)+"ingr");
		var instr_div = $('<div></div>'); 
		instr_div.attr('id',String(ctr)+"instr");
		var clone_i = a.clone();
		clone_i.attr('height','400');
		clone_i.attr('width','400');
		master_div.append('\
			<nav id="navbar'+String(ctr)+'" class="navbar navbar-default navbar-fixed-top" role="navigation">\
				<div class="container-fluid">\
					<div class="navbar-header">\
			          <a class="navbar-brand" href="#'+String(ctr)+"pic"+'"">'+name.clone().html()+'</a>\
		         	</div>\
	        	</div>\
	        </nav>');
		pic_div.append(clone_i);
		scroll_container.append(pic_div);
		instruction_div.append('<hr>');
		var info = $('<h4>Scroll down for more</h4>');
		scroll_container.append(info);
		ingr_div.append(ul);
		instruction_div.append(ingr_div);
		instruction_div.append('<hr>');
		instr_div.append(instr_ol);
		instruction_div.append(instr_div);
		scroll_container.append(instruction_div)
		master_div.append(scroll_container);
		scroll_container.scroll(function(){
			info.hide();
		});
		$('#recipe-carousel').append(master_div);

		//
		var div = $('<div id="recipe_div" style="height: 450px" ></div>').data("idx", ctr-1);
		bind_selector(div);
		

		var descrip = $('<p style="color: #27ae60 !important;" align="top"></p>');
		descrip.text(value['description']);
		var li = $('<li style="display: table-cell; overflow: hidden; position: relative; width: 150px; "></li>');
		var li1 = $('<h3 width="130px;"></h3>');
		var temp = $('<p style="color: #27ae60 !important;" ></p>');
		temp.text(day);
		// li1.html = temp;
		temp.appendTo(li1);

		li1.appendTo(div);
		div.append('<hr>');
		a.attr('height','130px');
		a.attr('width','130px');
		a.appendTo(div);
		ctr++;
		name.appendTo(div);
		descrip.appendTo(div);

		div.appendTo(li);
		li.appendTo('#planner-table');
	});
}

preference_set_callback = function(response){
	if (response["return"]==true){
		menu_plan=null;
		$("#plannertab").trigger('click');
	    }else{
	    	
	    }
}

get_preferences_callback = function(response){
	if (response["return"]==true){
		preferences = [];
		meals = response["packet"]["meals"];
		var isChecked = $('#subscribe-checkbox').is(':checked');
		subscribed = isChecked;
		if(response["packet"]["subscribed"]==true&&!isChecked){
			$('#subscribe-checkbox').bootstrapSwitch('toggleState');
			subscribed = true;
		}else if(response["packet"]["subscribed"]==false&&isChecked){
			$('#subscribe-checkbox').bootstrapSwitch('toggleState');
			subscribed = false;
		}

		if(meals!=0)
			$('li[value='+meals+']')[0].className="active"
		$.each( response["packet"]["preference"], function( index, value ){
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
    	needNew=true;
    	AjaxRequest(jsonPacket,preference_set_callback);
    }
});

$('#generate_grocery').on('click',function(){
	$('#grocery_list').empty();
	$.each(menu_plan, function(ind, value) {
		$.each(value['ingredients'], function(k,v) {
			var li = $('<li style="margin:0!important; padding:0!important;"></li>');
		    li.append($('<p></p>').text(k + ' - ' + v));
		    $('#grocery_list').append(li);
		});
	});
	// console.log(dict);
	console.log("clicked");
	$("#grocery_modal").modal('show');
	
});

enableCreateAccount = function(){
	var sbmt = $('#create_account');
	// var sbmt = document.getElementById("create_account");
	// console.log(isInputsValid());
	// &&($('#TOS:checked').length>0)&&(typeof($('input[type="radio"]:checked').val())!= "undefined")
	if(isInputsValid()){
		console.log("valid");
		sbmt.prop('disabled', false);
    }
    else
    {
    	console.log("invalid");
        sbmt.prop('disabled', true);
    }
}

clearform = function(){
	$("input[type=text]").val("");
	$("input[type=password]").val("");
	$('#TOS').prop('checked', false);
}

// validate the inputs
ValidateInput = function(val){
	console.log("testing");
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
interested = function(){
	$("html, body").animate({ scrollTop: 0 }, "slow", function(){
		$('#register').modal('show');
	});
}

register_callback = function(response){
	if (response["return"]==true){
	    	console.log("account created - login in now");
    		$('#register').modal('hide');
	    	validate(response);
	    	clearAllInputs();
	    	$('#preferencestab').trigger('click');
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
	$('#front_create').prop('onclick',null);
	$('#front_create').on('click',function(){$('#preferencestab').trigger('click');});
	load_preference();
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
	$('#front_create').attr('onclick',"interested();");
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
 		$('#myTab a[href="#home"]').tab('show');
 		$('#front_create').off('click');
 		$('#front_create').attr('onclick',"interested();");

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

$('#username').tooltip({ /*or use any other selector, class, ID*/
    placement: "top",
    trigger: "focus"
});
$('#email').tooltip({ /*or use any other selector, class, ID*/
    placement: "top",
    trigger: "focus"
});
$('#user_age').tooltip({ /*or use any other selector, class, ID*/
    placement: "top",
    trigger: "focus"
});
$('#password').tooltip({ /*or use any other selector, class, ID*/
    placement: "top",
    trigger: "focus"
});

$('#user_username').tooltip({ /*or use any other selector, class, ID*/
    placement: "top",
    trigger: "focus"
});

$('#user_password').tooltip({ /*or use any other selector, class, ID*/
    placement: "top",
    trigger: "focus"
});

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




