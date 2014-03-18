/* 
* @Author: ziyuanliu
* @Date:   2014-02-23 23:19:59
* @Last Modified by:   ziyuanliu
* @Last Modified time: 2014-03-18 02:30:01
*/
$(document).ready(function() {

//backbone app initialization 
var app = {}; // create namespace for our app

// the user model - will expand further in the future to accomodate a user page
app.User = Backbone.Model.extend({
  defaults: {
    username: '',
    subscribed: false,
    preferences:[],
    meals:0
  }
});

// the recipe model 
app.Recipe = Backbone.Model.extend({
  defaults: {
    name: '',
    time_required:'',
    description: '',
    ingredients:'',
    instructions:'',
    picture:''
  }
});

app.RecipeList = Backbone.Collection.extend({
  model: app.Recipe,
  localStorage: new Store("backbone-recipe")
});

app.recipeList = new app.RecipeList();


//barebone views
app.RecipeView = Backbone.View.extend({
  // el - stands for element. Every view has a element associate in with HTML 
  //      content will be rendered.
	tagName: 'li',
	className:'col-sm-4 col-md-3',


  template:_.template($('#recipe-template').html()),
  // It's the first function called when this view it's instantiated.
  initialize: function(){
  	this.model.on('change', this.render, this);

    // this.render();
  },
  // $el - it's a cached jQuery object (el), in which you can use jQuery functions 
  //       to push content. Like the Hello World in this case.
  render: function(){
    this.$el.html(this.template(this.model.toJSON()));
    // console.log("render new");
    return this;
  },
  events: {
        'click #glyphchange':'changeRecipe',  
        'click .recipe_container': 'showModal'    },
  showModal: function(){
    var modalView = new Modal({model:this.model});
    $('.app').html(modalView.render().el);
  },
   changeRecipe: function(event){
   		event.stopImmediatePropagation();
   		var packet = {};
		var placeholder = {};
		placeholder.recipe=this.model.get('name');
        packet.get_new_from_category = placeholder;
        var jsonPacket = JSON.stringify(packet);
        AjaxRequest(jsonPacket,this.success, this);
        // console.log(this.model);
   },
  success:function(response, context){
   		if (response["return"]==true){
   			new_recipe = response["packet"]["new_recipe"];
   			// console.log(new_recipe['name']);
   			process_recipe(new_recipe);
   			// console.log(context);
   			context.model.set(new_recipe);
   			context.render();
   			// this.$el.addClass('exchanged');
   		}
   }
   
});

app.RecipeListView = Backbone.View.extend({
  // el - stands for element. Every view has a element associate in with HTML 
  //      content will be rendered.
  el: '#test-table',
  
  initialize: function () {
        app.recipeList.on('add', this.addOne, this);
        app.recipeList.on('reset', this.emptyList, this);
        // app.recipeList.on('reset', this.addAll, this);
        app.recipeList.fetch(); // Loads list from local storage
   },
   emptyList:function(){
   	$('#test-table').empty();
   },
   addOne: function(todo){
        var view = new app.RecipeView({model: todo});
        $('#test-table').append(view.render().el);
      },
  render: function(){
    this.$el.html(this.template(this.model.toJSON()));
  }
});

// Create a modal view class
// this is for the recipe modal
var Modal = Backbone.Modal.extend({
template: _.template($('#modal-template').html()),
cancelEl: '.bbm-button'
});

$('#glyphchange').click(function(event){
    event.stopImmediatePropagation();
});

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

String.prototype.trunc = String.prototype.trunc ||
      function(n){
          return this.length>n ? this.substr(0,n-1)+'&hellip;' : this;
      };

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
		// console.log(value);
  		
});

togglePreference = function(con){
	var parent = (con.parentNode);
	var val = parent.value;
	if(isNumber(val)&&val!=0){
		// console.log(val);
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
	// console.log("pref is now "+preferences);
}

AjaxRequest = function(dataPacket,callback,context)
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
	    if(context!= undefined){
	    	callback(response,context);
	    }else{
	    	callback(response);
	    }
	});
}

preference_callback = function(response){
	if (response["return"]==true){
		$("#preference_container").empty();
		// console.log(response);
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
	app.recipeList.reset();
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
	$('#load_bar').animate({ width: "110%" },1400,function() {
	    
        $('#planner_panel').animate({height:600},1000);
        $('#test-table').show(1500, function(){
        	$('#test-table').removeClass('hidden');
        	$('#load_bar_div').hide(1000);
        	// $('#planner_panel').animate({height:1},500);
        	$('#load_bar').animate({ width: "0%" });        	
		    $('#generate_grocery').show();
        });
	  }
		
	  );

});

planner_callback = function(response){
	if (response["return"]==true){
		// console.log(response["packet"]["plan"]);
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

get_image = function(recipe_name){
    var replaced = recipe_name.split(' ').join('+');
    var img = $('<img id="dynamic">');
	img.attr('src', "/image/"+replaced);
	return img;
}

get_image_name = function(recipe_name){
	var replaced = recipe_name.split(' ').join('+');
	return '/image/'+replaced;
}

scroll_clicked = function(){
	console.log(($this));
}

add_recipes_to_plan = function(data){
	var ctr = 1;
	$.each( data, function( index, value ){
		// console.log(value);
		process_recipe(value);
		var temp = new app.Recipe(value);
		// console.log(value["picture"]);
		app.recipeList.add(temp);
	});
}

process_recipe = function(value){
	value["picture"]= get_image_name(value['name']);
	value["time_required"]["total_time"]=parseInt(value['time_required']['prep time'])+parseInt(value['time_required']['cooking time']);
	value['instructions'].reverse();
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
	// console.log(response);
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

demo_callback = function(response){
	console.log(response);
	if (response["return"]==true){
    	var re = response['packet']['recipe']
    	process_recipe(re)
    	var mod = new app.Recipe(re);
    	var view = new app.RecipeView({model: mod});
    	var htmlEl = view.render().el;
    	var htmlEl = $(htmlEl);
    	htmlEl.addClass('col-md-offset-3');
    	// htmlEl.className = "";
        $('#demo_recipe').prepend(htmlEl);
        var el = $('');
        // $('#demo_recipe').append(el);

	}else{

	}
}
$('#generate_grocery').on('click',function(){
	// $('#grocery_list').empty();
	// app.recipeList.each(function(model){
	// 	  console.log(model); 
	// 	});
	// $.each(menu_plan, function(ind, value) {
	// 	$.each(value['ingredients'], function(k,v) {
	// 		var li = $('<li style="margin:0!important; padding:0!important;"></li>');
	// 	    li.append($('<p></p>').text(k + ' - ' + v));
	// 	    $('#grocery_list').append(li);
	// 	});
	// });
	// // console.log(dict);
	// console.log("clicked");
	$("#grocery_modal").modal('show');
	var packet = {};
	packet.values = '';
	var login = {};
	login.get_grocery_list = packet;

	var jsonPacket = JSON.stringify(login);
	AjaxRequest(jsonPacket,grocery_callback);
});

grocery_callback = function(response){
	if (response["return"]==true){
    	var re = response['packet']['grocery'];
    	console.log(re);
    	var template = _.template(
            $( "#grocery_acc" ).html()
        );
    	$('#grocery_list').html(template( response['packet'] ))
  //   	console.log(re);
  //   	$.each(re, function(k,v) {
		// 	console.log(k);
		// 	console.log(v);
		// });
	}else{

	}
}
// initial app calls
validate_cookie();
clearform();

var packet = {};
packet.values = '';
var login = {};
login.get_sample_recipe = packet;

var jsonPacket = JSON.stringify(login);
AjaxRequest(jsonPacket,demo_callback);
Backbone.history.start();    
var view = new app.RecipeListView();

});

