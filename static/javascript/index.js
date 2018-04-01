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
			url: "/login",
			success: function(data){
                if(data.state == "success"){
                    console.log("verify successfully");
                    var url = "/" + data.role;
                    console.log(url)
                    window.location = url;
                }
                else{
                    console.log(data)
                    alert(data.error);
                }
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
