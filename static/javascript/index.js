/***
	This file handles login and signup
***/


$(document).ready(function(){
	// login
	$("#login-btn").click(function(){
		var data = {
			"email" : $("#login-email").val(),
			"password" : $("#login-password").val()
		};
		$.ajax({
			contentType: "application/json; charset=utf-8",
			type: "POST",
			data: JSON.stringify(data),
			url: "/login",
			success: function(data){
			    window.location.replace('/' + data['role']);
		    },
		    error: function(data){
		        alert(JSON.parse(data.responseText)['message']);
		    }
		})
	});

	// signup
	$("#signup-btn").click(function(){
		var data = {
			"email" : $("#signup-email").val(),
			"name" : $("#signup-name").val(),
			"password" : $("#signup-password").val(),
			"role" : $("input[name='group']:checked").val()
		};

		$.ajax({
			type: "POST",
			url: "/register",
			data: JSON.stringify(data),
			contentType: 'application/json; charset=utf-8',
			complete: function(data) {
                alert(JSON.parse(data.responseText)['message']);
			}
		})
	});
});
