// global variable
var assignment;

$(document).ready(function(){
	// get the documents
	get_documents();
});


function get_documents(){
	// parse params
	var params = {}
	var t_params = assignment.params;
	t_params = t_params.split(",");
	for(var i = 0; i < t_params.length; i++){
		param = t_params[i];
		param = param.split(":");
		params[param[0]] = param[1]
	}

	// form data
	var data = {
		"query" : assignment.query,
		"ranker" : assignment.ranker,
		"num_results" : 10,
		"params" : params
	};

	// send data
	$.ajax({
		type: "POST",
		dataType: "json",
		url: "/search/" + assignment.instructor_name + "/" + assignment.ds_name,
		data: JSON.stringify(data),
		contentType: 'application/json; charset=utf-8'
	})
	.success(function(data){
		console.log(data.results);
		updateAssignmentView(data.results);
	});
}

function updateAssignmentView(documents){
	var html = "";

	documents.forEach(function(document){
		html += "<tr>" + 
		            "<td>" + 
		              "<a data-toggle='modal' data-target='#document-content'>" + document.name + "</a>" +
		            "</td>" +
		            "<td>" +
		              "<div class='label'>" +
		                "<div><input type='radio' name='label-name'> &nbsp;Relevant</div>" +
		                "<div style='margin-left:20px;'><input type='radio' name='label-name'> &nbsp;Not Relevant</div>" +
		              "</div>" +
		            "</td>" +
		          "</tr>";
	});

	$("tbody").html(html);
}