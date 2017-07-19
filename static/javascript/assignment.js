// global variable
var assignment;

$(document).ready(function(){
	updateAssignmentView();

	// send annotations
	$("#submit-btn").click(function(){
		var annotations = {};

		// judge if the student finish annotation or not
		var labels = $("tbody").find(".label");
		for(var i = 0; i < labels.length; i++){
			var label = labels[i];
			var id = $(label).attr("id");
			var input_name = "input[name=" + id + "-label-name]:checked";
			if(!$(input_name).val()){
				alert("Please finish assignment");
				break;
			}

			annotations[id+".txt"] = $(input_name).val();
		}


		var data = {
			"assignment" : assignment,
			"annotations" : annotations
		}

		$.ajax({
			type: "POST",
			dataType: "json",
			url: "/annotation",
			data: JSON.stringify(data),
			contentType: 'application/json; charset=utf-8'
		})
		.success(function(data){
			window.location = "/alert/annotator/Submit Successful";
		});
	});
});



function updateAssignmentView(){
	var html = "";

	for(key in assignment.doc_scores){
		var name_with_txt = key + ".txt";
		html += "<tr>" + 
	            "<td>" + 
	              "<a onclick='get_document_detail(this)' class='document-title' data-toggle='modal' data-target='#document-modal'>" + name_with_txt + "</a>" +
	            "</td>" +
	            "<td>" +
	              "<div class='label' id='" + key + "'>" +
	                "<div><input type='radio' name='" + key + "-label-name' value='relevant'> &nbsp;Relevant</div>" +
	                "<div style='margin-left:20px;'><input type='radio' name='" + key + "-label-name' value='irrelevant'> &nbsp;Not Relevant</div>" +
	              "</div>" +
	            "</td>" +
	          "</tr>";
	}

	$("tbody").html(html);
}



function get_document_detail(target){
	var doc_name = $(target).html();

	var data = {
		"assignment" : assignment,
		"document_name" : doc_name
	}

	// send data
	$.ajax({
		type: "POST",
		dataType: "json",
		url: "/document",
		data: JSON.stringify(data),
		contentType: 'application/json; charset=utf-8'
	})
	.success(function(data){
		console.log(data);
		$(".modal-title").html(doc_name);
		$(".modal-body").html(data);
	});
}







