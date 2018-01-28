// global variable
var assignment;
var user;

$(document).ready(function(){
	// new query apply button
	$("#new-query-apply-btn").click(function(){
		var query_content = $("#new-query-input").val();

		if(query_content == ""){
			alert("Query can't be empty");
			return;
		}

		var assignment_id = assignment["_id"]["$oid"];
		var user_id = user["_id"]["$oid"];
		var ds_name = assignment['ds_name']
		var ds_author = assignment['ds_author']

		var search_data = {
			"query" : query_content,
			"ranker" : assignment.ranker,
			"params" : assignment.params,
			"num_results" : 3
		};

		$.ajax({
			type : "POST",
			url : "/search/" + ds_author + "/" + ds_name,
			data: JSON.stringify(search_data),
			contentType: 'application/json; charset=utf-8'
		})
		.success(function(data){
			var doc_scores = {}
			for(var i = 0; i < data.results.length; i++){
				var doc_name = data.results[i].name;
				doc_name = doc_name.substring(0, doc_name.length - 4);
				var doc_score = data.results[i].score;
				doc_scores[doc_name] = doc_score;
			}

			var query_data = {
				"query" : query_content,
				"doc_scores" : doc_scores,
				"assignment_id" : assignment_id,
				"user_id" : user_id
			};

			$.ajax({
				type: "POST",
				dataType: "json",
				url: "/query",
				data: JSON.stringify(query_data),
				contentType: 'application/json; charset=utf-8'
			})
			.success(function(){
				// update view
				var html = "<div class='panel panel-default result-panel'>" + 
			    "<div class='panel-heading'><h4>" + query_content + "</h4></div>" + 
			    "<div class='panel-body' style='padding:0px;'>" +
			     "<table class='table table-striped'><tbody>";

			    for(var doc_name in doc_scores){
			    	html += "<tr>" +
		              "<td><a onclick='get_document_detail(this)' class='document-title' data-toggle='modal' data-target='#document-modal'>" + doc_name + ".txt</a></td>" + 
		              "<td>" + 
		                "<div class='label' id='" + query_content + "-" + doc_name + "'>" + 
		                  "<div><input type='radio' name='" + query_content + "-" + doc_name + "-label-name' value='relevant'> &nbsp;Relevant</div>" + 
		                  "<div style='margin-left:20px;'><input type='radio' name='" + query_content + "-" + doc_name + "-label-name' value='irrelevant'> &nbsp;Not Relevant</div>" + 
		                "</div>" + 
		              "</td>" + 
		            "</tr>";
			    }

			    html += "</tbody></table></div></div>";
			    $("#submit-btn").before(html);
			})

		});

	})


	// send annotations
	$("#submit-btn").click(function(){
		var annotations = {};

		// judge if the student finish annotation or not
		// var labels = $("tbody").find(".label");
		$(".result-panel").each(function(){
			var query_content = $(this).find(".panel-heading h4").html();
			var labels = $(this).find(".label");

			// annotation per query
			var apq = {}

			for(var i = 0; i < labels.length; i++){
				var label = labels[i];
				// console.log(typeof(label));
				var id = $(label).attr("id");
				var input_name = "input[name=" + id + "-label-name]:checked";
				if(!$(input_name).val()){
					alert("Please finish assignment");
					return true;
				}

				doc_name = id.split("-")[1];
				apq[doc_name+".txt"] = $(input_name).val();
			}

			annotations[query_content] = apq;
		});

		var data = {
			"assignment_id" : assignment["_id"]["$oid"],
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







