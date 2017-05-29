/**
	
**/
var user;
var classes;
var assignments;


$(document).ready(function(){
	$("#nav-upload-btn").click(function(){
		// set user_name
		window.localStorage.setItem("username", user.name);
		console.log("Sent username to upload page: " + user.name);
		window.location = "/upload";
	});

	// new class
	$("#create-class-btn").click(function(){
		var class_name = $("#class-name").val();
		var password = $("#class-password").val();

		var data = {
			"instructor" : user.name,
			"name" : class_name,
			"password" : password
		};

		$.ajax({
			type: "POST",
			dataType: "json",
			url: "/class",
			data: JSON.stringify(data),
			contentType: 'application/json; charset=utf-8'
		})
		.success(function(data){

		});

	});

	// new assignment
	$("#create-assignment-btn").click(function(){
		// form data
		var query = $("#assignment-query").val();
		var class_ = $("#assignment-class").val();
		var ds = $('input[name="data_set"]:checked').val();
		var instructor = window.localStorage.getItem("username");
		var ranker = $("#assignment-ranker").val();
		var params = {};

		for(var i = 0; i < search_algorithms[ranker].length; i++){
			var p_id = "#param-" + search_algorithms[ranker][i];
			params[search_algorithms[ranker][i]] = $(p_id).val();
		}

		var data = {
			"instructor" : instructor,
			"query" : query,
			"class" : class_,
			"dataset" : ds,
			"ranker" : ranker,
			"params" : params
		};

		// send data 

	});

	// select all clicked 
	$("#assign-select-all").click(function(){
		event.preventDefault();
		$(".ds-checkbox").prop("checked", true);
	});


	// parameter change
	$("#assignment-ranker").change(function(){
		var ranker = $("#assignment-ranker").val();
		var params = search_algorithms[ranker];

		var html = "";

		html += "<div class='row'> \
				    <label class='col-sm-2 control-label col-sm-offset-1'>Params</label> \
				    <div class='col-sm-8'> \
				      <input id='param-" + params[0] + "' type='text' placeholder='" + params[0] + "'> \
				    </div> \
				  </div>"

		for(var i = 1; i < params.length; i++){
			html += "<div class='row'> \
					    <label class='col-sm-2 control-label col-sm-offset-1'> </label> \
					    <div class='col-sm-8'> \
					      <input id='param-" + params[i] + "' type='text' placeholder='" + params[i] + "'> \
					    </div> \
					  </div>"
		}

		$("#assignment-params").html(html);
	});
});