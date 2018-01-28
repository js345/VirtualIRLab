/***
	This file handles login and signup
***/


$(document).ready(function(){
	// login
	$("#login-btn").click(function(){
		// prepare data
		var email = $("#login-email").val();
		var password = $("#login-password").val();

		var data = {
			"email" : email,
			"password" : password
		};

		// send data
		$.ajax({
			contentType: "application/json; charset=utf-8",
			type: "POST",
			dataType: "json",
			data: JSON.stringify(data),
			url: "/login"
		})
		.success(function(data){
			if(data.state == "success"){
				console.log("verify sucessfully");
				var url = "/" + data.group;
				window.location = url;
			}
			else{
				alert(data.error);
			}
		});
	});


	// signup
	$("#signup-btn").click(function(){
		// prepare data
		var email = $("#signup-email").val();
		var name = $("#signup-name").val();
		var password = $("#signup-password").val();
		var reenter = $("reenter-password").val();
		var group = $("input[name='group']:checked").val();

		var data = {
			"email" : email,
			"name" : name,
			"password" : password,
			"group" : group
		};

		// send data
		$.ajax({
			type: "POST",
			dataType: 'json',
			url: "/register",
			data: JSON.stringify(data),
			contentType: 'application/json; charset=utf-8'
		})
		.success(function(data){
			console.log(data);
		});
	});
});


// sign up validation
function validation(email, password, reenter){

}