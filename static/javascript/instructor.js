/**
	
**/
var user;
var classes;
var assignments;


$(document).ready(function(){
	$('[data-toggle="tooltip"]').tooltip(); 

	$("#assignment-deadline").datepicker();

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
			$("#assignment-class").append("<option>" + class_name + "</option>");
		});

	});

	// new assignment
	$("#create-assignment-btn").click(function(){
		// form data
		var name = $("#assignment-name").val();
		var query = $("#assignment-query").val();
		var class_ = $("#assignment-class").val();
		var ds = $('input[name="data_set"]:checked').val();
		var ranker = $("#assignment-ranker").val();
		var deadline = $("#assignment-deadline").val();
		var params = {};

		for(var i = 0; i < search_algorithms[ranker].length; i++){
			var p_id = "#param-" + search_algorithms[ranker][i];
			console.log(p_id);
			params[search_algorithms[ranker][i]] = $(p_id).val();
		}

		var data = {
			"name" : name,
			"query" : query,
			"class" : class_,
			"dataset" : ds,
			"ranker" : ranker,
			"params" : params,
			"deadline" : deadline
		};

		// send data 
		$.ajax({
			type: "POST",
			dataType: "json",
			url: "/assign",
			data: JSON.stringify(data),
			contentType: 'application/json; charset=utf-8'
		})
		.success(function(data){

		});
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
				      <input class='form-control' id='param-" + params[0] + "' type='text' placeholder='" + params[0] + "'> \
				    </div> \
				  </div>"

		for(var i = 1; i < params.length; i++){
			html += "<div class='row'> \
					    <label class='col-sm-2 control-label col-sm-offset-1' style='color:#fff;'>s</label> \
					    <div class='col-sm-8'> \
					      <input class='form-control' id='param-" + params[i] + "' type='text' placeholder='" + params[i] + "'> \
					    </div> \
					  </div>"
		}

		$("#assignment-params").html(html);
	});


	// update assignment
	$(".assignment-update-btn").click(function(){
		var id = $(this).attr("id");

		$.ajax({
			type: "GET",
			dataType: "json",
			url: "/assignment_update",
			data: {'name': id}
		})
		.success(function(data){
			// use the data to update modal
			
		});
	});
});